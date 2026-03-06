"""
GhostPin v5 — Coverage-Guided Fuzzer Orchestrator
Uses Frida Stalker to trace code coverage per fuzz payload, then
mutates payloads that produce new coverage (AFL++ feedback loop design).
"""
import os
import time
import json
import random
import string
import threading
from pathlib import Path
from ghostpin.core.adb import run_cmd, adb_shell

# Built-in seed payload corpus — covers common mobile vuln classes
SEED_PAYLOADS = [
    "",                                    # empty
    "A" * 1024,                            # overflow
    "null",                                # null/none
    "' OR 1=1--",                          # SQLi basic
    "' UNION SELECT NULL--",               # SQLi union
    "../../../etc/passwd",                  # path traversal
    "javascript:alert(1)",                  # XSS via scheme
    "<script>alert(1)</script>",           # XSS tag
    "file:///etc/hosts",                   # file:// scheme
    "content://com.android.contacts/",    # content:// IDOR
    "%00",                                 # null byte injection
    "{}",                                  # empty JSON
    "{\"__proto__\": {\"polluted\": 1}}",  # prototype pollution
    "\x00" * 64,                           # binary null bytes
    "\u202e\u0041",                        # RTL override
]

STALKER_SCRIPT = (
    Path(__file__).parent.parent / 'scripts' / 'fuzzer' / 'stalker_coverage.js'
).read_text(encoding='utf-8')

def _mutate(payload: str) -> str:
    """Simple AFL++-inspired mutation: bit flip, insert, duplicate, trim."""
    strategy = random.choice(['insert', 'flip', 'trim', 'dup', 'splice'])
    
    if strategy == 'insert':
        pos = random.randint(0, len(payload))
        char = random.choice(string.printable)
        return payload[:pos] + char + payload[pos:]
    elif strategy == 'flip' and payload:
        pos = random.randint(0, len(payload) - 1)
        chars = list(payload)
        chars[pos] = chr(random.randint(0, 127))
        return ''.join(chars)
    elif strategy == 'trim' and len(payload) > 1:
        trim = random.randint(1, max(1, len(payload) // 4))
        return payload[:-trim]
    elif strategy == 'dup':
        return payload * 2
    else:  # splice with random seed
        seed = random.choice(SEED_PAYLOADS)
        pos = random.randint(0, len(payload))
        return payload[:pos] + seed
        
    return payload

def run_coverage_fuzzer(
    serial: str,
    package: str,
    component: str,
    action: str = 'android.intent.action.VIEW',
    max_iterations: int = 50,
    progress_cb=None
) -> dict:
    """
    Main coverage-guided fuzzing loop.
    
    For each payload:
      1. Attach Frida and start Stalker.
      2. Fire the Intent via `adb shell am start`.
      3. Collect covered basic blocks via Stalker RPC.
      4. If new blocks were hit, save payload as interesting.
      5. Mutate interesting payloads to generate next generation.
    """
    def log(msg):
        if progress_cb: progress_cb(msg)
        
    try:
        import frida
    except ImportError:
        return {'ok': False, 'error': 'frida-tools not installed. Run: pip install frida-tools'}
        
    log(f'🧬 Coverage-Guided Fuzzer initializing...')
    log(f'Target: {package}/{component}')
    log(f'Iterations: {max_iterations}')
    
    all_coverage = set()       # Global set of ALL blocks ever seen
    interesting = []           # Payloads that produced NEW coverage
    crashes = []               # Payloads that caused the app to crash/timeout
    
    queue = list(SEED_PAYLOADS)  # Start with seeds
    
    iteration = 0
    
    while iteration < max_iterations and queue:
        payload = queue.pop(0)
        iteration += 1
        log(f'[{iteration}/{max_iterations}] Testing payload: {repr(payload[:60])}...')
        
        session = None
        script = None
        this_coverage = set()
        
        try:
            # 1. Attach Frida to target process
            device = frida.get_device(serial)
            
            try:
                session = device.attach(package)
            except frida.ProcessNotFoundError:
                # App not running — launch it first
                adb_shell(serial, f'am start -n {package}/{component}')
                time.sleep(1.5)
                try:
                    session = device.attach(package)
                except Exception as e:
                    log(f'  ⚠️  Could not attach: {e}')
                    continue
                    
            # 2. Inject coverage script
            script = session.create_script(STALKER_SCRIPT)
            cov_data = {}
            done_event = threading.Event()
            
            def on_message(msg, _data):
                if msg.get('type') == 'send':
                    payload_data = msg.get('payload', {})
                    if payload_data.get('type') == 'coverage':
                        for blk in payload_data.get('blocks', []):
                            this_coverage.add(blk)
                        done_event.set()
                        
            script.on('message', on_message)
            script.load()
            
            # 3. Start Stalker
            script.exports_sync.start_stalker()
            
            # 4. Fire the Intent with our payload
            escaped = payload.replace('"', '\\"')
            adb_shell(serial, f'am start -a {action} -n {package}/{component} --es fuzz_data "{escaped}"')
            time.sleep(0.8)  # Let the app process the intent
            
            # 5. Collect coverage
            script.exports_sync.stop_and_report()
            done_event.wait(timeout=3.0)
            
        except frida.TransportError:
            log(f'  ⚠️  Frida transport error — app may have crashed!')
            crashes.append({'payload': payload, 'iteration': iteration})
            continue
        except Exception as e:
            log(f'  ⚠️  Error during run: {e}')
        finally:
            if script:
                try: script.unload()
                except: pass
            if session:
                try: session.detach()
                except: pass
                
        # 6. Evaluate coverage delta
        new_blocks = this_coverage - all_coverage
        if new_blocks:
            log(f'  ✅ NEW COVERAGE: +{len(new_blocks)} blocks (total: {len(all_coverage) + len(new_blocks)})')
            all_coverage |= this_coverage
            interesting.append({'payload': payload, 'new_blocks': len(new_blocks)})
            
            # Generate children mutations — explore the new paths found
            for _ in range(3):
                queue.append(_mutate(payload))
        else:
            log(f'  ·  No new blocks. Coverage: {len(all_coverage)} blocks total.')
            
    log(f'')
    log(f'🏁 Fuzzing complete after {iteration} iterations.')
    log(f'   Total coverage: {len(all_coverage)} unique basic blocks')
    log(f'   Interesting payloads (triggered new paths): {len(interesting)}')
    log(f'   Crashes/hangs detected: {len(crashes)}')
    
    return {
        'ok': True,
        'iterations': iteration,
        'total_blocks': len(all_coverage),
        'interesting': interesting,
        'crashes': crashes,
    }

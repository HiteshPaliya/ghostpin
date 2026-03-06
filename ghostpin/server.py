#!/usr/bin/env python3
"""
GhostPin Enterprise v5.0 — Flask Application
All API routes for existing + new feature pillars.
"""
import os, sys, json, subprocess, threading, time, uuid, zipfile, tempfile, re, queue
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from flask import Flask, jsonify, request, Response, send_file

# ── Data directories ────────────────────────────────────────────
DATA_DIR    = Path.home() / '.ghostpin'
SESSIONS_DIR = DATA_DIR / 'sessions'
SCRIPTS_DIR  = DATA_DIR / 'scripts'
CERTS_DIR    = DATA_DIR / 'certs'
LOGS_DIR     = DATA_DIR / 'logs'
REPORTS_DIR  = DATA_DIR / 'reports'
MONITOR_DIR  = DATA_DIR / 'monitor-logs'

for d in [DATA_DIR, SESSIONS_DIR, SCRIPTS_DIR, CERTS_DIR, LOGS_DIR, REPORTS_DIR, MONITOR_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── In-memory state ─────────────────────────────────────────────
active_sessions  = {}
session_logs     = defaultdict(list)
sse_clients      = defaultdict(list)
monitor_sessions = {}
fuzz_results_store = {}

# ── SSE helper ──────────────────────────────────────────────────
def push_log(session_id, level, msg):
    entry = {'ts': int(time.time()*1000), 'level': level, 'msg': msg, 'session_id': session_id}
    session_logs[session_id].append(entry)
    for q in sse_clients[session_id]:
        try: q.put_nowait(entry)
        except: pass

# ── ADB / tool helpers ──────────────────────────────────────────
def run_cmd(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=isinstance(cmd, str),
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired: return '', 'timeout', -1
    except FileNotFoundError:
        n = cmd[0] if isinstance(cmd, list) else cmd.split()[0]
        return '', f'not found: {n}', -1

def adb(serial, *args):
    out, _, _ = run_cmd(['adb', '-s', serial] + list(args))
    return out

def adb_shell(serial, cmd):
    return adb(serial, 'shell', cmd)

def get_adb_devices():
    out, _, rc = run_cmd(['adb', 'devices', '-l'])
    if rc != 0: return []
    devs = []
    for line in out.split('\n')[1:]:
        line = line.strip()
        if not line or line.startswith('*'): continue
        parts = line.split()
        if len(parts) < 2 or parts[1] != 'device': continue
        m = re.search(r'model:(\S+)', line)
        model = (m.group(1) if m else 'Unknown').replace('_', ' ')
        devs.append({'serial': parts[0], 'status': 'device', 'model': model,
                     'type': 'network' if ':' in parts[0] else 'usb'})
    return devs

def get_device_info(serial):
    info = {}
    for prop, key in [('ro.product.model','model'),('ro.build.version.release','androidVersion'),
                       ('ro.build.version.sdk','apiLevel'),('ro.product.cpu.abi','abi'),
                       ('ro.product.manufacturer','manufacturer'),('ro.build.type','buildType')]:
        info[key] = adb_shell(serial, f'getprop {prop}') or 'unknown'
    id_out = adb_shell(serial, 'su -c id 2>/dev/null || id')
    info['isRooted'] = 'uid=0' in id_out
    ps_out = adb_shell(serial, 'pgrep -f frida-server 2>/dev/null')
    info['fridaRunning'] = bool(ps_out.strip())
    bat = adb_shell(serial, 'dumpsys battery | grep level')
    m = re.search(r'level: (\d+)', bat)
    info['battery'] = int(m.group(1)) if m else None
    info['platform'] = 'android'
    return info

def get_ios_devices():
    out, _, rc = run_cmd(['frida-ls-devices'])
    if rc != 0: return []
    devs = []
    for line in out.split('\n'):
        if '\tusb\t' in line or '\tremote\t' in line:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                devs.append({'serial': parts[0].strip(), 'model': parts[1].strip(),
                             'platform': 'ios', 'type': 'usb', 'isRooted': False, 'fridaRunning': False})
    return devs

TOOLS = ['adb','frida','frida-ps','frida-trace','objection','apktool','jadx',
         'openssl','mitmproxy','mitmweb','ideviceinfo','ios-deploy','apk-mitm','keytool','xz']

def check_tool(name):
    import shutil
    path = shutil.which(name)
    if not path: return {'found': False, 'path': None, 'version': None}
    ver, _, _ = run_cmd(f'{name} --version 2>&1 | head -1')
    return {'found': True, 'path': path, 'version': ver[:60] if ver else ''}

# ── Inline Frida scripts (existing 14) ─────────────────────────
# Stored inline so the server is self-contained (same as v4.1)
INLINE_SCRIPTS = {}  # populated below

def _load_inline_scripts():
    """Load built-in scripts from package scripts/ dir, falling back to minimal stubs."""
    base = Path(__file__).parent / 'scripts' / 'bypass'
    ids = [
        'universal-android-bypass','obfuscation-resilient','root-detection-bypass',
        'frida-evasion','ios-universal','ios-jailbreak-bypass','flutter-android',
        'flutter-ios','native-openssl','grpc-bypass','xamarin-bypass',
        'certificate-transparency','unity-il2cpp','quic-blocker',
        'safetynet-play-integrity','react-native-hermes','anti-cheat-gaming',
    ]
    for sid in ids:
        p = base / f'{sid}.js'
        if p.exists():
            INLINE_SCRIPTS[sid] = p.read_text(encoding='utf-8')
        else:
            INLINE_SCRIPTS[sid] = f'// {sid} — script file not found at {p}\nsend("[GhostPin] {sid} loaded");'

_load_inline_scripts()

SCRIPT_META = [
    {'id':'universal-android-bypass','name':'Universal Android SSL','desc':'OkHttp3, TrustManager, SSLContext, Conscrypt, TrustKit, WebView, NSC','tags':['android','ssl'],'diff':'easy','platform':'android'},
    {'id':'obfuscation-resilient','name':'Obfuscation Resilient','desc':'Method-signature matching — defeats ProGuard/R8/DexGuard','tags':['android','obfusc'],'diff':'medium','platform':'android'},
    {'id':'root-detection-bypass','name':'Root Detection Bypass','desc':'RootBeer, file checks, Build.TAGS, exec() blocking, Magisk/KSU','tags':['android','evasion'],'diff':'easy','platform':'android'},
    {'id':'frida-evasion','name':'Frida Detection Evasion','desc':'/proc/maps filter, port hiding, module cloaking','tags':['android','evasion'],'diff':'medium','platform':'android'},
    {'id':'ios-universal','name':'iOS Universal SSL','desc':'SecTrustEvaluate, NSURLSession, TrustKit, AFNetworking','tags':['ios','ssl'],'diff':'easy','platform':'ios'},
    {'id':'ios-jailbreak-bypass','name':'iOS Jailbreak Bypass','desc':'NSFileManager, canOpenURL, Cydia/Sileo detection evasion','tags':['ios','evasion'],'diff':'medium','platform':'ios'},
    {'id':'flutter-android','name':'Flutter Android','desc':'libflutter.so BoringSSL — pattern scan + ssl_crypto export hook','tags':['android','flutter'],'diff':'hard','platform':'android'},
    {'id':'flutter-ios','name':'Flutter iOS','desc':'Flutter.framework BoringSSL with architecture-aware pattern scan','tags':['ios','flutter'],'diff':'hard','platform':'ios'},
    {'id':'native-openssl','name':'Native OpenSSL/BoringSSL','desc':'SSL_CTX_set_verify, X509_verify_cert, ssl_verify_peer_cert','tags':['android','native'],'diff':'hard','platform':'both'},
    {'id':'grpc-bypass','name':'gRPC / Netty','desc':'NettyChannelBuilder, OkHttp grpc transport, SslHandler','tags':['android','grpc'],'diff':'hard','platform':'android'},
    {'id':'xamarin-bypass','name':'Xamarin / MAUI','desc':'Mono ServicePointMgr, AndroidMessageHandler, HttpClientHandler','tags':['android','ios'],'diff':'medium','platform':'both'},
    {'id':'certificate-transparency','name':'CT Bypass','desc':'CTVerifier, PolicyCompliance, NetworkSecurityConfig CT','tags':['android','ssl'],'diff':'hard','platform':'android'},
    {'id':'unity-il2cpp','name':'Unity / IL2CPP','desc':'Mono runtime + IL2CPP export enum + pattern scan','tags':['android','ios','native'],'diff':'expert','platform':'both'},
    {'id':'quic-blocker','name':'QUIC/HTTP3 Blocker','desc':'Forces HTTP/2 fallback, disables CronetEngine QUIC','tags':['android','grpc'],'diff':'medium','platform':'android'},
    {'id':'safetynet-play-integrity','name':'SafetyNet + Play Integrity','desc':'Bypasses Google attestation, patches JWS, spoofs Build props','tags':['android','evasion'],'diff':'expert','platform':'android','pill':'new'},
    {'id':'react-native-hermes','name':'React Native / Hermes','desc':'Hermes JS engine bypass, Flipper/DevSupport disable, libcurl hook','tags':['android','flutter'],'diff':'hard','platform':'android','pill':'new'},
    {'id':'anti-cheat-gaming','name':'Gaming Anti-Cheat','desc':'Unity IL2CPP SSL enum, EasyAntiCheat, BattlEye, il2cpp_resolve_icall','tags':['android','ios','native'],'diff':'expert','platform':'both','pill':'new'},
]

# ── Flask app factory ────────────────────────────────────────────
def _get_or_create_secret_key() -> bytes:
    """Load the Flask session secret from disk, creating it once if needed.
    Using os.urandom(32) at startup is insecure — every restart invalidates
    all existing user sessions, which is jarring and forces re-authentication."""
    key_file = DATA_DIR / 'secret.key'
    if key_file.exists():
        return key_file.read_bytes()
    key = os.urandom(32)
    key_file.write_bytes(key)
    key_file.chmod(0o600)  # Owner-read only
    return key

def create_app():
    app = Flask(__name__)
    app.secret_key = _get_or_create_secret_key()

    # ── Gzip compression middleware ──────────────────────────────
    # Reduces JSON API response sizes by 60-80%, critical for the
    # large server_html.py HTML payload.
    import gzip as _gzip
    @app.after_request
    def compress_response(response):
        accept = request.headers.get('Accept-Encoding', '')
        if 'gzip' not in accept:
            return response
        if response.status_code < 200 or response.status_code >= 300:
            return response
        if response.content_length and response.content_length < 500:
            return response  # Not worth compressing tiny responses
        if response.direct_passthrough:
            return response

        data = response.get_data()
        compressed = _gzip.compress(data, compresslevel=6)
        if len(compressed) < len(data):
            response.set_data(compressed)
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Length'] = len(compressed)
        return response

    # ── Core routes ─────────────────────────────────────────
    @app.route('/')
    def index():
        try:
            from server_html import HTML
            return HTML
        except ImportError:
            # Try package path
            html_path = Path(__file__).parent.parent / 'server_html.py'
            if html_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location('server_html', html_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod.HTML
            return '<h1>GhostPin v5</h1><p>server_html.py not found</p>', 200

    @app.route('/api/devices')
    def api_devices():
        devs = []
        for d in get_adb_devices():
            devs.append({**d, **get_device_info(d['serial'])})
        devs.extend(get_ios_devices())
        return jsonify(devs)

    @app.route('/api/tools')
    def api_tools():
        return jsonify({t: check_tool(t) for t in TOOLS})

    @app.route('/api/scripts')
    def api_scripts():
        return jsonify(SCRIPT_META)

    @app.route('/api/scripts/<script_id>', methods=['GET'])
    def api_script_get(script_id):
        custom = SCRIPTS_DIR / f'{script_id}.js'
        if custom.exists():
            return jsonify({'content': custom.read_text(), 'custom': True})
        content = INLINE_SCRIPTS.get(script_id)
        if content:
            return jsonify({'content': content, 'custom': False})
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/scripts/<script_id>', methods=['POST'])
    def api_script_save(script_id):
        data = request.json
        (SCRIPTS_DIR / f'{script_id}.js').write_text(data.get('content', ''))
        return jsonify({'ok': True})

    @app.route('/api/processes')
    def api_processes():
        serial = request.args.get('serial')
        platform = request.args.get('platform', 'android')
        if not serial: return jsonify([])
        out, _, _ = run_cmd(['frida-ps', '-U', '-a', '-i'] if platform == 'android' else ['frida-ps', '-U'], timeout=10)
        procs = []
        for line in out.split('\n')[1:]:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                procs.append({'pid': parts[0], 'name': parts[1]})
        return jsonify(procs)

    @app.route('/api/bypass/start', methods=['POST'])
    def api_bypass_start():
        opts = request.json
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        target = opts.get('target', '')
        
        # Handle single serial or multiple for parallel run
        serials = opts.get('serials', [])
        if not serials and opts.get('serial'):
            serials = [opts.get('serial')]
            
        platform = opts.get('platform', 'android')
        script_ids = opts.get('scriptIds', ['universal-android-bypass'])
        spawn_mode = opts.get('spawnMode', False)
        anti = opts.get('antiDetection', {})
        custom_script = opts.get('customScript', '')

        def run_bypass(serial_tgt):
            sid = f"{session_id}_{serial_tgt}"
            push_log(session_id, 'info', f'GhostPin v5 Sub-Session [{serial_tgt}]: {sid}')
            push_log(session_id, 'info', f'Target: {target} | Platform: {platform}')
            push_log(session_id, 'info', f'Scripts: {", ".join(script_ids)}')
            parts = [f'// GhostPin Enterprise v5 — {sid}', f'// {datetime.now().isoformat()}', '']
            for s_id in script_ids:
                custom = SCRIPTS_DIR / f'{s_id}.js'
                parts.append(custom.read_text() if custom.exists() else INLINE_SCRIPTS.get(s_id, f'// Not found: {s_id}'))
            if custom_script.strip():
                parts.append(f'\n// Custom\n{custom_script}')
            combined = '\n\n'.join(parts)
            script_path = Path(tempfile.mktemp(suffix=f'_{serial_tgt}.js', prefix='ghostpin_'))
            script_path.write_text(combined)
            args = ['frida', '-U']
            if serial_tgt:
                args = ['frida', '--device', serial_tgt]
            if spawn_mode: args += ['-f', target, '--no-pause']
            else: args += (['-p', target] if target.isdigit() else ['-n', target])
            args += ['-l', str(script_path)]
            push_log(session_id, 'info', f'Exec [{serial_tgt}]: {" ".join(args)}')
            try:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if session_id not in active_sessions: active_sessions[session_id] = {'procs': [], 'active': True, 'target': target}
                active_sessions[session_id]['procs'].append(proc)
                def read(stream, label):
                    for line in iter(stream.readline, ''):
                        line = line.rstrip()
                        if line:
                            lvl = 'error' if 'error' in line.lower() else 'frida'
                            push_log(session_id, lvl, f'[{label}] {line}')
                t1 = threading.Thread(target=read, args=(proc.stdout, serial_tgt), daemon=True)
                t2 = threading.Thread(target=read, args=(proc.stderr, serial_tgt), daemon=True)
                t1.start(); t2.start(); proc.wait(); t1.join(); t2.join()
                push_log(session_id, 'info', f'Session [{serial_tgt}] ended (rc={proc.returncode})')
            except FileNotFoundError:
                push_log(session_id, 'error', 'frida not found — pip install frida-tools')
            except Exception as e:
                push_log(session_id, 'error', str(e))
            finally:
                try: script_path.unlink()
                except: pass

        def run_all():
            threads = []
            active_sessions[session_id] = {'procs': [], 'active': True, 'target': target}
            for s in serials or ['']: # allow empty string for fallback -U
                t = threading.Thread(target=run_bypass, args=(s,), daemon=True)
                t.start()
                threads.append(t)
            for t in threads: t.join()
            if session_id in active_sessions:
                active_sessions[session_id]['active'] = False

        threading.Thread(target=run_all, daemon=True).start()
        return jsonify({'sessionId': session_id, 'ok': True})
        
    @app.route('/api/objection/start', methods=['POST'])
    def api_objection_start():
        """Launch an objection terminal for the target."""
        data = request.json or {}
        target = data.get('target', '')
        serial = data.get('serial', '')
        if not target: return jsonify({'error': 'target required'}), 400
        
        cmd = ['objection']
        if serial: cmd.extend(['--device', serial])
        cmd.extend(['-g', target, 'explore'])
        
        import platform
        terminal_cmd = ''
        if platform.system() == 'Windows':
            terminal_cmd = f'start cmd /c "title Objection: {target} && {" ".join(cmd)}"'
        elif platform.system() == 'Darwin':
            terminal_cmd = f"osascript -e 'tell app \"Terminal\" to do script \"{' '.join(cmd)}\"'"
        else:
            terminal_cmd = f"gnome-terminal -- bash -c '{' '.join(cmd)}; exec bash'"
            
        subprocess.Popen(terminal_cmd, shell=True)
        return jsonify({'ok': True, 'message': 'Objection terminal launched', 'cmd': cmd})

    @app.route('/api/bypass/stop', methods=['POST'])
    def api_bypass_stop():
        sid = request.json.get('sessionId')
        s = active_sessions.get(sid)
        if s and s.get('proc'): s['proc'].terminate(); s['active'] = False
        return jsonify({'ok': True})

    @app.route('/api/bypass/stream/<session_id>')
    def api_bypass_stream(session_id):
        q = queue.Queue()
        sse_clients[session_id].append(q)
        def generate():
            for entry in session_logs.get(session_id, []):
                yield f"data: {json.dumps(entry)}\n\n"
            try:
                while True:
                    try:
                        entry = q.get(timeout=30)
                        yield f"data: {json.dumps(entry)}\n\n"
                    except queue.Empty:
                        yield ": heartbeat\n\n"
                        s = active_sessions.get(session_id, {})
                        if not s.get('active', True): break
            finally:
                try: sse_clients[session_id].remove(q)
                except: pass
        return Response(generate(), mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

    @app.route('/api/bypass/logs/<session_id>')
    def api_bypass_logs(session_id):
        return jsonify(session_logs.get(session_id, []))

    # ── Sessions ─────────────────────────────────────────────
    @app.route('/api/sessions')
    def api_sessions():
        sessions = []
        for f in sorted(SESSIONS_DIR.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True):
            try: sessions.append(json.loads(f.read_text()))
            except: pass
        return jsonify(sessions)

    @app.route('/api/sessions/save', methods=['POST'])
    def api_sessions_save():
        data = request.json
        sid = data.get('sessionId')
        name = data.get('name', f'Session {datetime.now().strftime("%Y%m%d_%H%M%S")}')
        logs = session_logs.get(sid, [])
        save_data = {'id': sid, 'name': name,
                     'target': active_sessions.get(sid, {}).get('target', ''),
                     'logs': logs, 'savedAt': datetime.now().isoformat(), 'logCount': len(logs)}
        (SESSIONS_DIR / f'{sid}.json').write_text(json.dumps(save_data, indent=2))
        return jsonify({'ok': True})

    # ── ADB / Proxy / Cert (same as v4.1) ────────────────────
    @app.route('/api/adb/shell', methods=['POST'])
    def api_adb_shell():
        data = request.json
        out, err, rc = run_cmd(['adb', '-s', data['serial'], 'shell', data['cmd']], timeout=20)
        return jsonify({'stdout': out, 'stderr': err, 'rc': rc})

    @app.route('/api/adb/forward', methods=['POST'])
    def api_adb_forward():
        data = request.json
        out, err, rc = run_cmd(['adb', '-s', data['serial'], 'forward',
                                 f'tcp:{data.get("localPort",27042)}', f'tcp:{data.get("remotePort",27042)}'])
        return jsonify({'ok': rc == 0, 'out': out, 'err': err})

    @app.route('/api/proxy/set', methods=['POST'])
    def api_proxy_set():
        data = request.json
        out, err, rc = run_cmd(['adb', '-s', data['serial'], 'shell',
                                  f'settings put global http_proxy {data.get("host","127.0.0.1")}:{data.get("port",8080)}'])
        return jsonify({'ok': rc == 0})

    @app.route('/api/proxy/clear', methods=['POST'])
    def api_proxy_clear():
        run_cmd(['adb', '-s', request.json['serial'], 'shell', 'settings put global http_proxy :0'])
        return jsonify({'ok': True})

    @app.route('/api/proxy/blockquic', methods=['POST'])
    def api_block_quic():
        serial = request.json['serial']
        cmds = ['iptables -I OUTPUT -p udp --dport 443 -j REJECT 2>/dev/null',
                'iptables -I OUTPUT -p udp --dport 80 -j REJECT 2>/dev/null',
                'ip6tables -I OUTPUT -p udp --dport 443 -j REJECT 2>/dev/null']
        results = []
        for cmd in cmds:
            out, err, rc = run_cmd(['adb', '-s', serial, 'shell', f'su -c "{cmd}"'])
            results.append({'cmd': cmd, 'ok': rc == 0, 'out': out})
        return jsonify({'ok': True, 'results': results})

    @app.route('/api/frida/push', methods=['POST'])
    def api_frida_push():
        data = request.json
        serial = data.get('serial'); path = data.get('serverPath', '')
        steps = [f'Pushing frida-server to {serial}']
        out, err, rc = run_cmd(['adb', '-s', serial, 'push', path, '/data/local/tmp/frida-server'])
        steps.append(f'Push: {"OK" if rc==0 else "FAILED"} {err[:100]}')
        run_cmd(['adb', '-s', serial, 'shell', 'su -c "chmod +x /data/local/tmp/frida-server"'])
        steps.append('chmod: OK')
        run_cmd(['adb', '-s', serial, 'shell', 'su -c "/data/local/tmp/frida-server &"'])
        time.sleep(1)
        ps = adb_shell(serial, 'pgrep -f frida-server')
        running = bool(ps.strip())
        steps.append(f'Status: {"RUNNING ✓" if running else "NOT RUNNING ✗"}')
        return jsonify({'ok': running, 'steps': steps})

    @app.route('/api/frida/stop', methods=['POST'])
    def api_frida_stop():
        run_cmd(['adb', '-s', request.json['serial'], 'shell', 'su -c "pkill frida-server"'])
        return jsonify({'ok': True})

    @app.route('/api/cert/inject', methods=['POST'])
    def api_cert_inject():
        data = request.json; serial = data.get('serial')
        cert_path = data.get('certPath', ''); platform = data.get('platform', 'android')
        steps = []
        try:
            if platform == 'android':
                api_level = int(adb_shell(serial, 'getprop ro.build.version.sdk').strip() or '0')
                steps.append(f'Android API {api_level}')
                if api_level >= 34:
                    steps.append('Android 14+ — APEX injection')
                    cmds = ['su -c "mount -o remount,rw /apex/com.android.conscrypt/etc/security/cacerts 2>/dev/null"']
                else:
                    steps.append('Standard /system/etc/security/cacerts injection')
                    cmds = ['su -c "mount -o remount,rw /system"']
                for cmd in cmds:
                    out, err, rc = run_cmd(['adb', '-s', serial, 'shell', cmd])
                    steps.append(f'{"✓" if rc==0 else "✗"} {cmd[:60]}')
            return jsonify({'ok': True, 'steps': steps})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e), 'steps': steps})

    # ── NEW: Ultimate UX - 1-Click APK Extractor ─────────────
    @app.route('/api/apk/extract', methods=['POST'])
    def api_apk_extract():
        """Pulls the base.apk (and any split APKs) from the connected Android device."""
        data = request.json or {}
        serial = data.get('serial', '')
        package = data.get('package', '')
        if not serial or not package:
            return jsonify({'ok': False, 'error': 'Serial and package required'}), 400
            
        try:
            # Find the path(s) on the device
            out = adb_shell(serial, f'pm path {package}')
            if not out or 'package:' not in out:
                return jsonify({'ok': False, 'error': f'Package {package} not found on device'})
                
            # `pm path` returns multiple lines for split APKs:
            # package:/data/app/.../base.apk
            # package:/data/app/.../split_config.xxhdpi.apk
            apk_paths = [line.replace('package:', '').strip() for line in out.strip().split('\n') if line.startswith('package:')]
            
            from pathlib import Path
            import tempfile
            import zipfile
            import os
            
            tmp_dir = Path(tempfile.mkdtemp(prefix='gp_pull_'))
            
            if len(apk_paths) == 1:
                # Single APK case
                local_apk = tmp_dir / f"{package}.apk"
                pull_out, err, rc = run_cmd(['adb', '-s', serial, 'pull', apk_paths[0], str(local_apk)], timeout=60)
                if rc != 0 or not local_apk.exists():
                    return jsonify({'ok': False, 'error': f'Failed to pull APK: {err}'})
                return send_file(str(local_apk), as_attachment=True, download_name=f"{package}.apk")
            else:
                # Split APK case — pull all into a folder and ZIP them up
                zip_path = tmp_dir / f"{package}_splits.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for remote_path in apk_paths:
                        filename = os.path.basename(remote_path)
                        local_split_path = tmp_dir / filename
                        # Pull individual split
                        pull_out, err, rc = run_cmd(['adb', '-s', serial, 'pull', remote_path, str(local_split_path)], timeout=60)
                        if rc == 0 and local_split_path.exists():
                            zipf.write(local_split_path, filename)
                
                if not zip_path.exists():
                    return jsonify({'ok': False, 'error': 'Failed to package split APKs.'})
                return send_file(str(zip_path), as_attachment=True, download_name=f"{package}_splits.zip")
                
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    # ── APK Analyzer ─────────────────────────────────────────
    @app.route('/api/apk/analyze', methods=['POST'])
    def api_apk_analyze():
        if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
        f = request.files['file']
        tmp = Path(tempfile.mktemp(suffix=Path(f.filename).suffix))
        f.save(tmp)
        result = _analyze_apk(tmp)
        try: tmp.unlink()
        except: pass
        return jsonify(result)

    def _analyze_apk(apk_path):
        result = {'file': apk_path.name, 'size': apk_path.stat().st_size,
                  'platform': 'ios' if apk_path.suffix == '.ipa' else 'android',
                  'frameworks': [], 'nativeLibs': [], 'hasNSC': False, 'mTLS': False,
                  'obfuscated': False, 'recommendedScripts': [], 'detections': [],
                  'packageName': '', 'versionName': ''}
        try:
            with zipfile.ZipFile(apk_path, 'r') as z:
                names = z.namelist()
                result['nativeLibs'] = [n for n in names if n.endswith('.so')][:20]
                if any('flutter' in n.lower() for n in names):
                    result['frameworks'].append('Flutter')
                    result['recommendedScripts'].append('flutter-android')
                if any('libil2cpp' in n.lower() for n in names):
                    result['frameworks'].append('Unity/IL2CPP')
                    result['recommendedScripts'].append('unity-il2cpp')
                    result['recommendedScripts'].append('anti-cheat-gaming')
                if any('xamarin' in n.lower() or 'mono' in n.lower() for n in names):
                    result['frameworks'].append('Xamarin/Mono')
                    result['recommendedScripts'].append('xamarin-bypass')
                if any('hermes' in n.lower() or 'index.android.bundle' in n for n in names):
                    result['frameworks'].append('React Native / Hermes')
                    result['recommendedScripts'].append('react-native-hermes')
                if 'res/xml/network_security_config.xml' in names:
                    result['hasNSC'] = True
                    nsc = z.read('res/xml/network_security_config.xml').decode('utf-8', errors='ignore')
                    if 'pin-set' in nsc:
                        result['detections'].append({'type':'NSC_PINNING','severity':'high','detail':'NSC pin-set detected'})
                for dex in [n for n in names if n.endswith('.dex')][:3]:
                    d = z.read(dex).decode('utf-8', errors='ignore')
                    if 'CertificatePinner' in d:
                        result['detections'].append({'type':'OKHTTP_PINNING','severity':'high','detail':'OkHttp3 CertificatePinner'})
                        _add_rec(result, 'universal-android-bypass')
                    if 'TrustKit' in d:
                        result['detections'].append({'type':'TRUSTKIT','severity':'high','detail':'TrustKit detected'})
                    if 'RootBeer' in d:
                        result['detections'].append({'type':'ROOT_DETECTION','severity':'medium','detail':'RootBeer detected'})
                        _add_rec(result, 'root-detection-bypass')
                    if 'SafetyNet' in d or 'IntegrityManager' in d:
                        result['detections'].append({'type':'ATTESTATION','severity':'high','detail':'SafetyNet/Play Integrity detected'})
                        _add_rec(result, 'safetynet-play-integrity')
                    if 'frida' in d.lower():
                        result['detections'].append({'type':'FRIDA_DETECTION','severity':'medium','detail':'Frida detection code'})
                        _add_rec(result, 'frida-evasion')
                    if 'grpc' in d.lower() or 'netty' in d.lower():
                        result['frameworks'].append('gRPC/Netty'); _add_rec(result, 'grpc-bypass')
                    if 'DevicePolicyManager' in d or 'isAdminActive' in d:
                        result['detections'].append({'type':'MDM_CODE','severity':'medium','detail':'MDM/DevicePolicy code found'})
                    short = len(re.findall(r'\bL[a-z]{1,2};', d))
                    if short > 200:
                        result['obfuscated'] = True; _add_rec(result, 'obfuscation-resilient')
                cert_exts = ['.p12','.pfx','.bks','.jks','.keystore']
                if any(any(n.endswith(e) for e in cert_exts) for n in names):
                    result['mTLS'] = True
                    result['detections'].append({'type':'MTLS_CERT','severity':'critical','detail':'Client certificate bundle found — mTLS likely'})
        except Exception as e:
            result['error'] = str(e)
        if not result['recommendedScripts']:
            result['recommendedScripts'] = ['universal-android-bypass']
        result['frameworks'] = list(dict.fromkeys(result['frameworks']))
        return result

    def _add_rec(result, sid):
        if sid not in result['recommendedScripts']:
            result['recommendedScripts'].append(sid)

    # ── NEW: Vulnerability Scanner ───────────────────────────
    @app.route('/api/scan/apk', methods=['POST'])
    def api_scan_apk():
        if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
        f = request.files['file']
        tmp = Path(tempfile.mktemp(suffix=Path(f.filename).suffix))
        f.save(tmp)
        try:
            from ghostpin.features.vuln_scanner import scan_apk
        except ImportError:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            try:
                from ghostpin.features.vuln_scanner import scan_apk
            except ImportError:
                return jsonify({'error': 'vuln_scanner module not found'}), 500
        result = scan_apk(tmp)
        try: tmp.unlink()
        except: pass
        return jsonify(result)

    # ── NEW: Intent Fuzzer ───────────────────────────────────


    
    # ── NEW: Apex Tier - Native JADX Decompiler ───────────────
    @app.route('/api/decompile', methods=['POST'])
    def api_decompile_apk():
        """Accepts an APK, runs JADX to decompile it to a temp dir, and returns the workspace ID."""
        if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
        f = request.files['file']
        
        import tempfile
        from pathlib import Path
        import uuid
        
        wid = str(uuid.uuid4())
        workspace_dir = Path(tempfile.gettempdir()) / f"gp_decompile_{wid}"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        tmp_app = workspace_dir / f.filename
        f.save(tmp_app)
        
        try:
            from ghostpin.features.decompiler import decompile_apk
            result = decompile_apk(str(tmp_app), str(workspace_dir))
            
            if result.get('ok'):
                return jsonify({'ok': True, 'workspace_id': wid, 'log': result.get('log')})
            else:
                return jsonify({'ok': False, 'error': result.get('error')}), 500
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    @app.route('/api/decompile/file', methods=['GET'])
    def api_decompile_read_file():
        """Reads a decompiled java file from the specified workspace."""
        wid = request.args.get('workspace_id')
        file_path = request.args.get('file_path')
        
        if not wid or not file_path:
            return jsonify({'error': 'workspace_id and file_path needed'}), 400
            
        import tempfile
        from pathlib import Path
        workspace_dir = Path(tempfile.gettempdir()) / f"gp_decompile_{wid}"
        
        if not workspace_dir.exists():
            return jsonify({'error': 'Workspace expired or invalid'}), 404
            
        try:
            from ghostpin.features.decompiler import read_source_file
            res = read_source_file(str(workspace_dir), file_path)
            return jsonify(res)
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    # ── Apex Tier: Coverage-Guided Fuzzer ────────────────────
    @app.route('/api/fuzzer/coverage', methods=['POST'])
    def api_fuzzer_coverage():
        data = request.json or {}
        serial    = data.get('serial', '')
        package   = data.get('package', '')
        component = data.get('component', '')
        action    = data.get('action', 'android.intent.action.VIEW')
        max_iter  = int(data.get('max_iter', 30))
        
        if not serial or not package or not component:
            return jsonify({'error': 'serial, package, component required'}), 400
            
        scan_id = str(uuid.uuid4())
        
        def run_fuzz():
            from ghostpin.features.coverage_fuzzer import run_coverage_fuzzer
            from ghostpin.features.vuln_scanner import _ScanResults
            logs = []
            res = run_coverage_fuzzer(
                serial, package, component, action, max_iter,
                progress_cb=lambda msg: logs.append(msg)
            )
            res['logs'] = logs
            _ScanResults[f'fuzz_{scan_id}'] = res

        threading.Thread(target=run_fuzz, daemon=True).start()
        return jsonify({'ok': True, 'scan_id': scan_id})
    
    @app.route('/api/fuzzer/coverage/results/<scan_id>')
    def api_fuzzer_coverage_results(scan_id):
        from ghostpin.features.vuln_scanner import _ScanResults
        key = f'fuzz_{scan_id}'
        if key not in _ScanResults:
            return jsonify({'status': 'running'})
        return jsonify({'status': 'done', **_ScanResults[key]})

    @app.route('/api/intent/components')
    def api_intent_components():
        serial = request.args.get('serial')
        package = request.args.get('package')
        if not serial or not package: return jsonify({'error': 'serial and package required'}), 400
        try:
            from ghostpin.features.intent_fuzzer import enumerate_components
        except ImportError:
            return jsonify({'activities':[],'services':[],'receivers':[],'error':'module not found'})
        return jsonify(enumerate_components(serial, package))

    @app.route('/api/apk/patch', methods=['POST'])
    def api_apk_patch():
        """1-Click un-pin and repack APK/IPA using apk-mitm"""
        if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
        f = request.files['file']
        
        # Save to temp
        tmp_dir = Path(tempfile.mkdtemp(prefix='gp_patch_'))
        tmp_app = tmp_dir / f.filename
        f.save(tmp_app)
        
        try:
            from ghostpin.features.auto_patcher import patch_app
            result = patch_app(tmp_app, tmp_dir)
            if result.get('ok'):
                # Return the patched file for download directly
                return send_file(result['path'], as_attachment=True)
            else:
                return jsonify({'error': result.get('error', 'Unknown patcher error')}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Note: The temp dir cleanup is handled asynchronously or lazily in production.
            # We skip immediate unlink here so send_file can stream it.
            pass

    @app.route('/api/intent/fuzz', methods=['POST'])
    def api_intent_fuzz():
        data = request.json
        serial = data.get('serial'); package = data.get('package')
        component = data.get('component'); comp_type = data.get('type', 'activity')
        categories = data.get('categories', ['null','sqli','traversal','uri_schemes'])
        fuzz_id = f"fuzz_{uuid.uuid4().hex[:8]}"
        try:
            from ghostpin.features.intent_fuzzer import fuzz_component
        except ImportError:
            return jsonify({'error': 'module not found'}), 500
        def run_fuzz():
            results = fuzz_component(serial, component, comp_type, categories)
            fuzz_results_store[fuzz_id] = results
        threading.Thread(target=run_fuzz, daemon=True).start()
        return jsonify({'fuzzId': fuzz_id, 'ok': True})

    @app.route('/api/intent/results/<fuzz_id>')
    def api_intent_results(fuzz_id):
        return jsonify(fuzz_results_store.get(fuzz_id, []))

    # ── NEW: API Monitor ─────────────────────────────────────
    @app.route('/api/monitor/start', methods=['POST'])
    def api_monitor_start():
        data = request.json
        session_id = f"mon_{uuid.uuid4().hex[:10]}"
        serial = data.get('serial', '')
        target = data.get('target', '')
        categories = data.get('categories', ['crypto', 'file', 'network'])
        spawn_mode = data.get('spawnMode', False)
        try:
            from ghostpin.features.api_monitor import build_monitor_script
        except ImportError:
            return jsonify({'error': 'api_monitor module not found'}), 500
        script_content = build_monitor_script(categories)
        script_path = Path(tempfile.mktemp(suffix='.js', prefix='gpmon_'))
        script_path.write_text(script_content)
        def run_monitor():
            push_log(session_id, 'info', f'API Monitor started | target={target} | categories={categories}')
            args = ['frida', '-U']
            if spawn_mode: args += ['-f', target, '--no-pause']
            else: args += (['-p', target] if target.isdigit() else ['-n', target])
            args += ['-l', str(script_path)]
            try:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                monitor_sessions[session_id] = {'proc': proc, 'active': True}
                def read(stream):
                    for line in iter(stream.readline, ''):
                        line = line.rstrip()
                        if line: push_log(session_id, 'frida', line)
                t1 = threading.Thread(target=read, args=(proc.stdout,), daemon=True)
                t2 = threading.Thread(target=read, args=(proc.stderr,), daemon=True)
                t1.start(); t2.start(); proc.wait()
                push_log(session_id, 'info', f'Monitor ended')
            except Exception as e:
                push_log(session_id, 'error', str(e))
            finally:
                if session_id in monitor_sessions: monitor_sessions[session_id]['active'] = False
                try: script_path.unlink()
                except: pass
        threading.Thread(target=run_monitor, daemon=True).start()
        return jsonify({'sessionId': session_id, 'ok': True})

    @app.route('/api/monitor/stop', methods=['POST'])
    def api_monitor_stop():
        sid = request.json.get('sessionId')
        s = monitor_sessions.get(sid)
        if s and s.get('proc'): s['proc'].terminate(); s['active'] = False
        return jsonify({'ok': True})

    @app.route('/api/monitor/stream/<session_id>')
    def api_monitor_stream(session_id):
        q = queue.Queue()
        sse_clients[session_id].append(q)
        def generate():
            for entry in session_logs.get(session_id, []):
                yield f"data: {json.dumps(entry)}\n\n"
            try:
                while True:
                    try:
                        entry = q.get(timeout=30)
                        yield f"data: {json.dumps(entry)}\n\n"
                    except queue.Empty:
                        yield ": heartbeat\n\n"
                        s = monitor_sessions.get(session_id, {})
                        if not s.get('active', True): break
            finally:
                try: sse_clients[session_id].remove(q)
                except: pass
        return Response(generate(), mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

    # ── NEW: MDM Profiler ────────────────────────────────────
    @app.route('/api/mdm/profile')
    def api_mdm_profile():
        serial = request.args.get('serial')
        if not serial: return jsonify({'error': 'serial required'}), 400
        try:
            from ghostpin.features.mdm_profiler import profile_device
        except ImportError:
            return jsonify({'error': 'mdm_profiler module not found'}), 500
        return jsonify(profile_device(serial))

    # ── NEW: Class Tracer ────────────────────────────────────
    @app.route('/api/trace/start', methods=['POST'])
    def api_trace_start():
        data = request.json
        session_id = f"trace_{uuid.uuid4().hex[:8]}"
        serial = data.get('serial', '')
        target = data.get('target', '')
        class_filter = data.get('classFilter', '')
        trace_class = data.get('traceClass', '')
        platform = data.get('platform', 'android')
        spawn_mode = data.get('spawnMode', False)
        try:
            from ghostpin.features.class_tracer import build_class_dump_script, build_method_tracer_script
        except ImportError:
            return jsonify({'error': 'class_tracer not found'}), 500
        if trace_class:
            script_content = build_method_tracer_script(trace_class, platform)
        else:
            script_content = build_class_dump_script(class_filter)
        script_path = Path(tempfile.mktemp(suffix='.js', prefix='gptrace_'))
        script_path.write_text(script_content)
        def run_trace():
            push_log(session_id, 'info', f'Class tracer started | target={target}')
            args = ['frida', '-U']
            if spawn_mode: args += ['-f', target, '--no-pause']
            else: args += (['-p', target] if target.isdigit() else ['-n', target])
            args += ['-l', str(script_path)]
            try:
                proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                active_sessions[session_id] = {'proc': proc, 'active': True, 'target': target}
                def read(stream):
                    for line in iter(stream.readline, ''):
                        line = line.rstrip()
                        if line: push_log(session_id, 'frida', line)
                t1 = threading.Thread(target=read, args=(proc.stdout,), daemon=True)
                t2 = threading.Thread(target=read, args=(proc.stderr,), daemon=True)
                t1.start(); t2.start(); proc.wait()
                push_log(session_id, 'info', 'Trace ended')
            except Exception as e:
                push_log(session_id, 'error', str(e))
            finally:
                if session_id in active_sessions: active_sessions[session_id]['active'] = False
                try: script_path.unlink()
                except: pass
        threading.Thread(target=run_trace, daemon=True).start()
        return jsonify({'sessionId': session_id, 'ok': True})

    @app.route('/api/trace/stream/<session_id>')
    def api_trace_stream(session_id):
        q = queue.Queue()
        sse_clients[session_id].append(q)
        def generate():
            for entry in session_logs.get(session_id, []):
                yield f"data: {json.dumps(entry)}\n\n"
            try:
                while True:
                    try: yield f"data: {json.dumps(q.get(timeout=30))}\n\n"
                    except queue.Empty:
                        yield ": heartbeat\n\n"
                        if not active_sessions.get(session_id, {}).get('active', True): break
            finally:
                try: sse_clients[session_id].remove(q)
                except: pass
        return Response(generate(), mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

    # ── NEW: Report Generator ────────────────────────────────
    @app.route('/api/report/generate', methods=['POST'])
    def api_report_generate():
        data = request.json
        report_id = f"report_{uuid.uuid4().hex[:10]}"
        output_path = REPORTS_DIR / f'{report_id}.html'
        session_id = data.get('sessionId', '')
        scan_id = data.get('scanId', '')
        report_data = {
            'app_name': data.get('appName', 'Target Application'),
            'platform': data.get('platform', 'android'),
            'tester': data.get('tester', 'GhostPin Enterprise'),
            'logs': session_logs.get(session_id, []),
            'vuln_findings': data.get('vulnFindings', []),
            'analysis': data.get('analysis', {}),
            'mdm': data.get('mdm', {}),
            'monitor_calls': [e['msg'] for e in session_logs.get(data.get('monitorSessionId',''), [])],
        }
        try:
            from ghostpin.features.reporter import generate_report
        except ImportError:
            return jsonify({'error': 'reporter not found'}), 500
        path = generate_report(report_data, output_path)
        return jsonify({'ok': True, 'reportId': report_id, 'path': path})

    @app.route('/api/report/list')
    def api_report_list():
        reports = []
        for f in sorted(REPORTS_DIR.glob('*.html'), key=lambda x: x.stat().st_mtime, reverse=True):
            reports.append({'id': f.stem, 'name': f.name, 'size': f.stat().st_size,
                            'created': datetime.fromtimestamp(f.stat().st_mtime).isoformat()})
        return jsonify(reports)

    @app.route('/api/report/<report_id>')
    def api_report_get(report_id):
        report_id = report_id.replace('..', '').replace('/', '')
        p = REPORTS_DIR / f'{report_id}.html'
        if p.exists(): return send_file(p, mimetype='text/html')
        return jsonify({'error': 'Report not found'}), 404

    # ── Phase 2: Authentication ──────────────────────────────
    @app.route('/login')
    def login_page():
        from ghostpin.features.auth import LOGIN_HTML, is_auth_enabled
        if not is_auth_enabled():
            return 'redirect:/'
        return LOGIN_HTML

    @app.route('/api/auth/login', methods=['POST'])
    def api_auth_login():
        from ghostpin.features.auth import check_pin, check_token, is_auth_enabled
        if not is_auth_enabled():
            session['authenticated'] = True
            return jsonify({'ok': True})
        data = request.json or {}
        pin = data.get('pin', '')
        token = data.get('token', '')
        if (pin and check_pin(pin)) or (token and check_token(token)):
            session['authenticated'] = True
            return jsonify({'ok': True})
        return jsonify({'ok': False, 'error': 'Invalid credentials'}), 401

    @app.route('/api/auth/logout', methods=['POST'])
    def api_auth_logout():
        session.pop('authenticated', None)
        return jsonify({'ok': True})

    @app.route('/api/frida/start', methods=['POST'])
    def api_frida_start():
        data = request.json
        serial = data.get('serial')
        if not serial: return jsonify({'error': 'No device serial'}), 400
        
        def push_log(msg):
            from ghostpin.core.sessions import active_sessions
            if sid := session.get('sid'):
                if sid in active_sessions:
                    active_sessions[sid]['logs'].append(msg)
                    
        from ghostpin.features.frida_downloader import auto_install_frida
        res = auto_install_frida(serial, push_log_fn=push_log)
        return jsonify(res)

    # ── NEW: Apex Tier - Stealth Evasion Core ────────────────
    @app.route('/api/frida/stealth', methods=['POST'])
    def api_frida_stealth():
        data = request.json
        serial = data.get('serial')
        if not serial: return jsonify({'error': 'No device serial'}), 400
        
        def push_log(msg):
            from ghostpin.core.sessions import active_sessions
            if sid := session.get('sid'):
                if sid in active_sessions:
                    active_sessions[sid]['logs'].append(msg)
                    
        from ghostpin.features.stealth_mgr import auto_install_stealth
        res = auto_install_stealth(serial, progress_cb=push_log)
        return jsonify(res)

    @app.route('/api/auth/status')
    def api_auth_status():
        from ghostpin.features.auth import is_auth_enabled, get_token
        enabled = is_auth_enabled()
        return jsonify({
            'enabled': enabled,
            'authenticated': not enabled or bool(session.get('authenticated')),
            'token': get_token() if enabled else '',
        })

    @app.route('/api/auth/configure', methods=['POST'])
    def api_auth_configure():
        from ghostpin.features.auth import enable_auth, disable_auth
        data = request.json or {}
        if data.get('enable') and data.get('pin'):
            token = enable_auth(data['pin'])
            return jsonify({'ok': True, 'token': token,
                           'message': f'Auth enabled. Save this token for API access.'})
        elif data.get('enable') is False:
            disable_auth()
            return jsonify({'ok': True, 'message': 'Auth disabled'})
        return jsonify({'ok': False, 'error': 'provide enable:true/false and pin'}), 400

    # ── Phase 2: Frida Auto-Downloader ───────────────────────
    @app.route('/api/frida/auto-install', methods=['POST'])
    def api_frida_auto_install():
        data = request.json or {}
        serial = data.get('serial', '')
        session_id = f"fridadl_{uuid.uuid4().hex[:8]}"
        if not serial:
            return jsonify({'ok': False, 'error': 'serial required'}), 400
        from ghostpin.features.frida_downloader import auto_install_frida
        logs = []
        result = auto_install_frida(serial, push_log_fn=lambda m: logs.append(m))
        result['logs'] = logs
        return jsonify(result)

    @app.route('/api/frida/check-release')
    def api_frida_check_release():
        from ghostpin.features.frida_downloader import get_latest_frida_release, get_host_frida_ver
        release = get_latest_frida_release()
        release['host_version'] = get_host_frida_ver()
        return jsonify(release)

    # ── Phase 2: CVE Checker ─────────────────────────────────
    @app.route('/api/cve/check', methods=['POST'])
    def api_cve_check():
        if 'file' not in request.files:
            return jsonify({'error': 'No APK file'}), 400
        f = request.files['file']
        tmp = Path(tempfile.mktemp(suffix=Path(f.filename).suffix))
        f.save(tmp)
        try:
            from ghostpin.features.cve_checker import check_cves
            result = check_cves(tmp, use_osv=True)
        except Exception as e:
            result = {'error': str(e)}
        finally:
            try: tmp.unlink()
            except: pass
        return jsonify(result)

    # ── Phase 2: APK Diff ────────────────────────────────────
    @app.route('/api/diff/apk', methods=['POST'])
    def api_diff_apk():
        if 'file_a' not in request.files or 'file_b' not in request.files:
            return jsonify({'error': 'Both file_a and file_b required'}), 400
        f_a, f_b = request.files['file_a'], request.files['file_b']
        tmp_a = Path(tempfile.mktemp(suffix='.apk'))
        tmp_b = Path(tempfile.mktemp(suffix='.apk'))
        f_a.save(tmp_a); f_b.save(tmp_b)
        try:
            from ghostpin.features.diff_analyzer import diff_apks
            result = diff_apks(tmp_a, tmp_b)
        except Exception as e:
            result = {'error': str(e)}
        finally:
            for t in [tmp_a, tmp_b]:
                try: t.unlink()
                except: pass
        return jsonify(result)

    # ── Phase 2: Workspace ───────────────────────────────────
    @app.route('/api/workspace/list')
    def api_workspace_list():
        from ghostpin.features.workspace import list_workspaces
        return jsonify(list_workspaces())

    @app.route('/api/workspace/<package>')
    def api_workspace_get(package):
        from ghostpin.features.workspace import get_workspace
        return jsonify(get_workspace(package))

    @app.route('/api/workspace/<package>', methods=['POST'])
    def api_workspace_save(package):
        from ghostpin.features.workspace import save_workspace
        return jsonify(save_workspace(package, request.json or {}))

    @app.route('/api/workspace/<package>', methods=['DELETE'])
    def api_workspace_delete(package):
        from ghostpin.features.workspace import delete_workspace
        return jsonify({'ok': delete_workspace(package)})

    # ── Phase 2: Traffic Replay ──────────────────────────────
    traffic_sessions_store = {}

    @app.route('/api/traffic/start', methods=['POST'])
    def api_traffic_start():
        data = request.json or {}
        session_id = f"tr_{uuid.uuid4().hex[:8]}"
        port = data.get('port', 8877)
        from ghostpin.features.traffic_replay import start_capture
        result = start_capture(session_id, listen_port=port)
        if result.get('ok'):
            traffic_sessions_store[session_id] = result
        return jsonify(result)

    @app.route('/api/traffic/stop', methods=['POST'])
    def api_traffic_stop():
        sid = (request.json or {}).get('sessionId', '')
        from ghostpin.features.traffic_replay import stop_capture
        return jsonify({'ok': stop_capture(sid)})

    @app.route('/api/traffic/flows/<session_id>')
    def api_traffic_flows(session_id):
        from ghostpin.features.traffic_replay import list_flows
        return jsonify(list_flows(session_id))

    @app.route('/api/traffic/flow/<session_id>/<int:flow_id>')
    def api_traffic_flow_detail(session_id, flow_id):
        from ghostpin.features.traffic_replay import get_flow_detail
        return jsonify(get_flow_detail(session_id, flow_id))

    @app.route('/api/traffic/replay', methods=['POST'])
    def api_traffic_replay():
        data = request.json or {}
        from ghostpin.features.traffic_replay import replay_flow
        return jsonify(replay_flow(data['sessionId'], data['flowId'], data.get('modifications')))

    # ── Phase 2: SARIF / JSON Export ────────────────────────
    @app.route('/api/export/sarif', methods=['POST'])
    def api_export_sarif():
        data = request.json or {}
        from ghostpin.features.sarif_export import to_sarif, save_sarif
        findings = data.get('findings', [])
        app_name = data.get('appName', 'GhostPin Scan')
        apk_path = data.get('apkPath', '')
        if data.get('save'):
            p = save_sarif(findings, app_name, apk_path)
            return jsonify({'ok': True, 'path': str(p)})
        return jsonify(to_sarif(findings, app_name, apk_path))

    @app.route('/api/export/json', methods=['POST'])
    def api_export_json():
        data = request.json or {}
        from ghostpin.features.sarif_export import to_json_report
        return jsonify(to_json_report(
            data.get('findings', []),
            data.get('appName', 'GhostPin Scan'),
            data.get('meta', {}),
        ))

    # ── Phase 2: Guided Checklist ────────────────────────────
    @app.route('/api/checklist/all')
    def api_checklist_all():
        from ghostpin.features.guided_checklist import all_checklists
        return jsonify(all_checklists())

    @app.route('/api/checklist/<app_type>')
    def api_checklist_get(app_type):
        from ghostpin.features.guided_checklist import get_checklist
        return jsonify(get_checklist(app_type))

    @app.route('/api/checklist/detect', methods=['POST'])
    def api_checklist_detect():
        from ghostpin.features.guided_checklist import detect_app_type, get_checklist
        scan_result = request.json or {}
        app_type = detect_app_type(scan_result)
        return jsonify({'appType': app_type, 'checklist': get_checklist(app_type)})

    # ── Phase 2: Script Version Control ─────────────────────
    @app.route('/api/scripts/<script_id>/reset', methods=['POST'])
    def api_script_reset(script_id):
        """Reset custom script back to built-in default."""
        custom = SCRIPTS_DIR / f'{script_id}.js'
        if custom.exists():
            custom.unlink()
            return jsonify({'ok': True, 'message': 'Script reset to built-in default'})
        return jsonify({'ok': True, 'message': 'Script already at default (no custom version found)'})

    @app.route('/api/scripts/<script_id>/diff')
    def api_script_diff(script_id):
        """Return diff between custom and built-in version."""
        import difflib
        built_in = INLINE_SCRIPTS.get(script_id, '')
        custom_path = SCRIPTS_DIR / f'{script_id}.js'
        custom = custom_path.read_text() if custom_path.exists() else built_in
        diff = list(difflib.unified_diff(
            built_in.splitlines(keepends=True),
            custom.splitlines(keepends=True),
            fromfile=f'{script_id} (built-in)',
            tofile=f'{script_id} (custom)',
        ))
        return jsonify({
            'has_changes': bool(diff),
            'diff': ''.join(diff[:200]),
            'custom_exists': custom_path.exists(),
        })

    # ── Phase 2: HTTPS management ────────────────────────────
    @app.route('/api/tls/info')
    def api_tls_info():
        from ghostpin.features.tls_manager import CERT_FILE, KEY_FILE, cert_fingerprint, generate_self_signed_cert
        try:
            generate_self_signed_cert()
        except Exception:
            pass
        return jsonify({
            'cert_exists': CERT_FILE.exists(),
            'key_exists': KEY_FILE.exists(),
            'cert_path': str(CERT_FILE),
            'fingerprint': cert_fingerprint(),
        })

    # ── Phase 4: AI Analyzer ────────────────────────────────
    @app.route('/api/ai/analyze', methods=['POST'])
    def api_ai_analyze():
        """Pass a finding to the LLM (Gemini) for analysis and remediation code."""
        data = request.json or {}
        title = data.get('title', '')
        details = data.get('details', '')
        context = data.get('context', 'SAST')
        
        try:
            from ghostpin.features.ai_analyzer import analyze_vulnerability
            analysis = analyze_vulnerability(title, details, context)
            return jsonify({'ok': True, 'analysis': analysis})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    # ── Phase 4: API Auto-Discovery ─────────────────────────
    @app.route('/api/discovery/map', methods=['GET'])
    def api_discovery_map():
        """Return the automatically discovered API map from the singleton mapper."""
        try:
            from ghostpin.features.api_mapper import mapper
            return jsonify({'ok': True, 'map': mapper.get_map()})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    @app.route('/api/discovery/extract/static', methods=['POST'])
    def api_discovery_extract_static():
        """Manually trigger AST string extraction for the mapper from a scan result."""
        data = request.json or {}
        strings = data.get('strings', [])
        if not strings: return jsonify({'ok': False, 'error': 'No strings provided'})
        
        try:
            from ghostpin.features.api_mapper import mapper
            mapper.extract_from_static_strings(strings)
            return jsonify({'ok': True, 'endpoint_count': len(mapper.discovered_endpoints)})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    @app.route('/api/discovery/extract/flow', methods=['POST'])
    def api_discovery_extract_flow():
        """Submit a traffic flow to the mapper to dynamically build the map."""
        data = request.json or {}
        try:
            from ghostpin.features.api_mapper import mapper
            mapper.extract_from_dynamic_flow(data)
            return jsonify({'ok': True})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    # ── Phase 4: Export to Postman ──────────────────────────
    @app.route('/api/export/postman', methods=['POST'])
    def api_export_postman():
        """Export discovered endpoints and traffic flows to a Postman Collection v2.1.0."""
        data = request.json or {}
        app_name = data.get('appName', 'GhostPin_Target')
        
        try:
            from ghostpin.features.api_mapper import mapper
            api_map = mapper.get_map()
            
            collection = {
                "info": {
                    "name": f"{app_name} GhostPin API Map",
                    "description": "Auto-generated by GhostPin Enterprise API Discovery module.",
                    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
                },
                "item": []
            }
            
            # Group by host
            hosts = api_map.get('hosts', [])
            for host in hosts:
                folder = {"name": host, "item": []}
                for ep in api_map.get('endpoints', []):
                    if ep['host'] == host:
                        # Build Postman query array
                        query_arr = [{"key": k, "value": "TBD"} for k in ep.get('params', [])]
                        
                        req_item = {
                            "name": ep['path'] or "/",
                            "request": {
                                "method": ep.get('method', 'GET'),
                                "url": {
                                    "raw": ep['url'],
                                    "host": [host],
                                    "path": ep['path'].strip('/').split('/') if ep['path'] else [],
                                    "query": query_arr
                                }
                            }
                        }
                        folder["item"].append(req_item)
                
                if folder["item"]:
                    collection["item"].append(folder)
                    
            report_id = f"postman_{uuid.uuid4().hex[:8]}.json"
            output_path = REPORTS_DIR / report_id
            output_path.write_text(json.dumps(collection, indent=2))
            
            return jsonify({'ok': True, 'path': str(output_path), 'collection': collection})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    return app


# ── Standalone entry point ───────────────────────────────────────
if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('GHOSTPIN_PORT', 7331))
    print(f'\n{"="*60}\n  [*] GhostPin Enterprise v5.0 -- Phantom\n  http://localhost:{port}\n{"="*60}\n')
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

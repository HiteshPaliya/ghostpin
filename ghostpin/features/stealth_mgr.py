"""
GhostPin v5 - Stealth Evasion Core (hluda-server)
Pulls V8-less, randomized hluda-server variants from hzzheyang/strongR-frida-android
to bypass Promon, DexGuard, and kernel-level anti-cheats.
"""
import re, os, time, json, urllib.request
from pathlib import Path
from ghostpin.core.adb import run_cmd, adb_shell
from ghostpin.features.frida_downloader import get_device_abi, FRIDA_CACHE_DIR

HLUDA_RELEASES_API = 'https://api.github.com/repos/hzzheyang/strongR-frida-android/releases/latest'

def auto_install_stealth(serial: str, progress_cb=None) -> dict:
    """Download, push, and execute the stealth hluda-server."""
    
    def log(msg):
        if progress_cb: progress_cb(msg)
        
    log('🛡️ Initializing Stealth Evasion Core deployment...')
    
    abi = get_device_abi(serial)
    log(f'Target Architecture: {abi}')
    
    # 1. Fetch latest hluda release info
    log('Querying latest hluda-server release...')
    try:
        req = urllib.request.Request(
            HLUDA_RELEASES_API,
            headers={'User-Agent': 'GhostPin/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            
        assets = data.get('assets', [])
        hluda_ver = data.get('tag_name')
        if not assets:
            return {'ok': False, 'error': 'No assets found in target release.'}
    except Exception as e:
        log(f'Failed to query hluda releases: {e}')
        return {'ok': False, 'error': str(e)}
        
    # Match ABI to hluda asset naming convention
    # strongR-frida names things like: hluda-server-16.1.4-android-arm64
    target_asset = None
    target_url = None
    
    for a in assets:
        name = a['name'].lower()
        if 'server' in name and 'android' in name and abi.replace('-v8a', '').replace('armeabi-v7a', 'arm') in name:
            target_asset = a['name']
            target_url = a['browser_download_url']
            break
            
    if not target_url:
        return {'ok': False, 'error': f'No stealth binaries found for {abi}'}
        
    log(f'Found Stealth Core: {target_asset}')
    
    # 2. Download and Extract
    FRIDA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = FRIDA_CACHE_DIR / f'hluda-{target_asset.replace(".xz", "")}'
    
    if cache_path.exists():
        log(f'Cache hit: {cache_path}')
    else:
        xz_path = FRIDA_CACHE_DIR / target_asset
        log(f'Downloading {target_asset}...')
        
        def _reporthook(count, block_size, total_size):
            if total_size > 0 and progress_cb:
                pct = min(100, int(count * block_size * 100 / total_size))
                if pct % 20 == 0:  # Prevent flooding
                    progress_cb(f'Download: {pct}%')

        urllib.request.urlretrieve(target_url, xz_path, reporthook=_reporthook)
        log('Decompressing V8-less stealth core...')
        
        try:
            import lzma
            with lzma.open(xz_path, 'rb') as f_in:
                data = f_in.read()
            cache_path.write_bytes(data)
            xz_path.unlink()
        except Exception:
            try:
                import subprocess
                subprocess.run(['xz', '-d', str(xz_path)], check=True)
                decompressed = FRIDA_CACHE_DIR / target_asset.replace('.xz', '')
                decompressed.rename(cache_path)
            except Exception as e:
                return {'ok': False, 'error': f'Decompression failed: {e}'}

    # 3. Randomize binary name on push to evade path checks
    import uuid
    random_bin_name = f"sys_{uuid.uuid4().hex[:8]}"
    remote_path = f"/data/local/tmp/{random_bin_name}"
    
    log(f'Obfuscating binary path: {remote_path}')
    
    # Kill any existing standard frida-server before launching stealth
    adb_shell(serial, 'su -c "pkill frida-server 2>/dev/null"')
    adb_shell(serial, 'su -c "pkill hluda 2>/dev/null"')
    
    log('Pushing stealth core to device...')
    out, err, rc = run_cmd(['adb', '-s', serial, 'push', str(cache_path), remote_path])
    if rc != 0:
        return {'ok': False, 'error': err}
        
    # 4. chmod + start detached
    adb_shell(serial, f'su -c "chmod +x {remote_path}"')
    log('Executing detached stealth core...')
    # hluda usually doesn't need special flags, it randomizes pipe names itself
    adb_shell(serial, f'su -c "{remote_path} &"')
    time.sleep(2)
    
    # 5. Verify it's running
    running = bool(adb_shell(serial, f'pgrep -f {random_bin_name}').strip())
    if running:
        log('🛡️ Stealth Evasion Core actively running and hidden.')
        return {'ok': True, 'binary_name': random_bin_name, 'version': hluda_ver}
    else:
        log('❌ Stealth Core failed to start. Check device root permissions.')
        return {'ok': False, 'error': 'Failed to execute stealth binary.'}

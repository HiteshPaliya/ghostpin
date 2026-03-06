"""
GhostPin v5 Phase 2 — Feature: Frida-Server Auto-Downloader
Detects device ABI, fetches matching frida-server from GitHub releases,
pushes and starts it automatically.
"""
import re, os, tempfile, threading, time
from pathlib import Path

FRIDA_RELEASES_API = 'https://api.github.com/repos/frida/frida/releases/latest'
FRIDA_CACHE_DIR = Path.home() / '.ghostpin' / 'frida-binaries'

# ABI → frida release asset suffix
ABI_MAP = {
    'arm64-v8a':   'frida-server-{ver}-android-arm64.xz',
    'armeabi-v7a': 'frida-server-{ver}-android-arm.xz',
    'x86_64':      'frida-server-{ver}-android-x86_64.xz',
    'x86':         'frida-server-{ver}-android-x86.xz',
}

def get_device_abi(serial: str) -> str:
    from ghostpin.core.adb import adb_shell
    abi = adb_shell(serial, 'getprop ro.product.cpu.abi').strip()
    return abi if abi else 'arm64-v8a'

def get_installed_frida_ver(serial: str) -> str:
    """Get version of frida-server already on device, if any."""
    from ghostpin.core.adb import adb_shell
    out = adb_shell(serial, '/data/local/tmp/frida-server --version 2>/dev/null')
    m = re.search(r'(\d+\.\d+\.\d+)', out)
    return m.group(1) if m else ''

def get_host_frida_ver() -> str:
    """Get frida-tools version installed on the host."""
    try:
        import frida
        return frida.__version__
    except Exception:
        pass
    try:
        import subprocess
        out = subprocess.check_output(['frida', '--version'], text=True).strip()
        m = re.search(r'(\d+\.\d+\.\d+)', out)
        return m.group(1) if m else ''
    except Exception:
        return ''

def get_latest_frida_release() -> dict:
    """Fetch latest frida release info from GitHub API."""
    import urllib.request, json
    try:
        req = urllib.request.Request(
            FRIDA_RELEASES_API,
            headers={'User-Agent': 'GhostPin/5.0', 'Accept': 'application/vnd.github.v3+json'}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        ver = data['tag_name'].lstrip('v')
        assets = {a['name']: a['browser_download_url'] for a in data.get('assets', [])}
        return {'version': ver, 'assets': assets, 'tag': data['tag_name']}
    except Exception as e:
        return {'error': str(e)}

def download_frida_server(ver: str, abi: str, progress_cb=None) -> Path:
    """Download the matching frida-server binary, cache it locally."""
    import urllib.request
    FRIDA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    asset_name = ABI_MAP.get(abi, ABI_MAP['arm64-v8a']).format(ver=ver)
    cache_path = FRIDA_CACHE_DIR / f'frida-server-{ver}-{abi}'
    if cache_path.exists():
        if progress_cb: progress_cb(f'Cache hit: {cache_path}')
        return cache_path

    url = f'https://github.com/frida/frida/releases/download/{ver}/{asset_name}'
    xz_path = FRIDA_CACHE_DIR / asset_name
    if progress_cb: progress_cb(f'Downloading {asset_name} from GitHub...')

    def _reporthook(count, block_size, total_size):
        if total_size > 0 and progress_cb:
            pct = min(100, int(count * block_size * 100 / total_size))
            progress_cb(f'Download: {pct}%')

    urllib.request.urlretrieve(url, xz_path, reporthook=_reporthook)
    if progress_cb: progress_cb('Decompressing...')

    # Decompress .xz
    try:
        import lzma
        with lzma.open(xz_path, 'rb') as f_in:
            data = f_in.read()
        cache_path.write_bytes(data)
        xz_path.unlink()
    except Exception:
        # Try xz command
        import subprocess
        subprocess.run(['xz', '-d', str(xz_path)], check=True)
        decompressed = FRIDA_CACHE_DIR / asset_name.replace('.xz', '')
        decompressed.rename(cache_path)

    if progress_cb: progress_cb(f'Saved: {cache_path}')
    return cache_path

def auto_install_frida(serial: str, push_log_fn=None) -> dict:
    """Full auto-install flow: detect ABI, download, push, start."""
    from ghostpin.core.adb import run_cmd, adb_shell

    def log(msg):
        if push_log_fn: push_log_fn(msg)

    log('Starting Frida auto-install...')

    # 1. Detect ABI
    abi = get_device_abi(serial)
    log(f'Device ABI: {abi}')

    # 2. Get host frida version (must match server)
    host_ver = get_host_frida_ver()
    if not host_ver:
        log('frida-tools not installed on host — pip install frida-tools')
        return {'ok': False, 'error': 'frida-tools not installed'}

    log(f'Host frida version: {host_ver}')

    # 3. Check if device already has matching version
    device_ver = get_installed_frida_ver(serial)
    if device_ver == host_ver:
        log(f'frida-server {host_ver} already on device — starting...')
        adb_shell(serial, 'su -c "pkill frida-server 2>/dev/null; /data/local/tmp/frida-server &"')
        time.sleep(1)
        running = bool(adb_shell(serial, 'pgrep -f frida-server').strip())
        log(f'Status: {"RUNNING" if running else "FAILED TO START"}')
        return {'ok': running, 'version': host_ver, 'cached': True}

    # 4. Download matching frida-server
    try:
        binary = download_frida_server(host_ver, abi, progress_cb=log)
    except Exception as e:
        log(f'Download failed: {e}')
        return {'ok': False, 'error': str(e)}

    # 5. Push to device
    log(f'Pushing to /data/local/tmp/frida-server...')
    out, err, rc = run_cmd(['adb', '-s', serial, 'push', str(binary), '/data/local/tmp/frida-server'])
    if rc != 0:
        log(f'Push failed: {err}')
        return {'ok': False, 'error': err}
    log('Push OK')

    # 6. chmod + start
    adb_shell(serial, 'su -c "chmod +x /data/local/tmp/frida-server"')
    log('chmod +x OK')
    adb_shell(serial, 'su -c "pkill frida-server 2>/dev/null; /data/local/tmp/frida-server &"')
    time.sleep(1.5)

    running = bool(adb_shell(serial, 'pgrep -f frida-server').strip())
    log(f'frida-server {host_ver} {"RUNNING ✓" if running else "NOT RUNNING ✗"}')
    return {'ok': running, 'version': host_ver, 'abi': abi}

"""
GhostPin Enterprise v5.0 — Core: ADB Helpers
"""
import re, subprocess
from typing import Optional

def run_cmd(cmd, timeout=15):
    """Run a shell command, return (stdout, stderr, returncode)."""
    try:
        r = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return '', 'timeout', -1
    except FileNotFoundError:
        name = cmd[0] if isinstance(cmd, list) else cmd.split()[0]
        return '', f'command not found: {name}', -1

def adb(serial: str, *args) -> str:
    out, _, _ = run_cmd(['adb', '-s', serial] + list(args))
    return out

def adb_shell(serial: str, cmd: str) -> str:
    return adb(serial, 'shell', cmd)

def get_adb_devices():
    out, err, rc = run_cmd(['adb', 'devices', '-l'])
    if rc != 0:
        return []
    devices = []
    for line in out.split('\n')[1:]:
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        serial, status = parts[0], parts[1]
        if status != 'device':
            continue
        model_m = re.search(r'model:(\S+)', line)
        model = (model_m.group(1) if model_m else 'Unknown').replace('_', ' ')
        devices.append({
            'serial': serial,
            'status': status,
            'model': model,
            'type': 'network' if ':' in serial else 'usb'
        })
    return devices

def get_device_info(serial: str) -> dict:
    info = {}
    props = {
        'ro.product.model': 'model',
        'ro.build.version.release': 'androidVersion',
        'ro.build.version.sdk': 'apiLevel',
        'ro.product.cpu.abi': 'abi',
        'ro.product.manufacturer': 'manufacturer',
        'ro.build.type': 'buildType',
    }
    for prop, key in props.items():
        info[key] = adb_shell(serial, f'getprop {prop}') or 'unknown'

    id_out = adb_shell(serial, 'su -c id 2>/dev/null || id')
    info['isRooted'] = 'uid=0' in id_out

    ps_out = adb_shell(serial, 'pgrep -f frida-server 2>/dev/null || pgrep -f /data/local/tmp/fs 2>/dev/null')
    info['fridaRunning'] = bool(ps_out.strip())

    bat = adb_shell(serial, 'dumpsys battery | grep level')
    bat_m = re.search(r'level: (\d+)', bat)
    info['battery'] = int(bat_m.group(1)) if bat_m else None
    info['platform'] = 'android'
    return info

def get_ios_devices():
    out, _, rc = run_cmd(['frida-ls-devices'])
    if rc != 0:
        return []
    devices = []
    for line in out.split('\n'):
        if '\tusb\t' in line or '\tremote\t' in line:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                devices.append({
                    'serial': parts[0].strip(),
                    'model': parts[1].strip() if len(parts) > 1 else 'iOS Device',
                    'platform': 'ios', 'type': 'usb',
                    'isRooted': False, 'fridaRunning': False
                })
    return devices

"""
GhostPin v5 Phase 2 — Feature: APK Version Diff
Compare two APK analysis results and highlight security-relevant changes.
"""
import zipfile, re
from pathlib import Path

def _get_apk_fingerprint(apk_path: Path) -> dict:
    """Extract security-relevant attributes from an APK."""
    fp = {
        'file': apk_path.name,
        'permissions': [],
        'exported_components': [],
        'frameworks': [],
        'native_libs': [],
        'has_nsc': False,
        'nsc_pins': [],
        'debuggable': False,
        'backup_enabled': False,
        'cleartext': False,
        'min_sdk': '',
        'target_sdk': '',
        'version_name': '',
        'package': '',
        'cert_fingerprints': [],
    }
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            names = z.namelist()
            fp['native_libs'] = sorted([n for n in names if n.endswith('.so')])

            # Frameworks
            if any('flutter' in n.lower() for n in names): fp['frameworks'].append('Flutter')
            if any('libil2cpp' in n.lower() for n in names): fp['frameworks'].append('Unity/IL2CPP')
            if any('hermes' in n.lower() or 'index.android.bundle' in n for n in names): fp['frameworks'].append('React Native')
            if any('xamarin' in n.lower() for n in names): fp['frameworks'].append('Xamarin')

            # NSC
            if 'res/xml/network_security_config.xml' in names:
                fp['has_nsc'] = True
                nsc = z.read('res/xml/network_security_config.xml').decode('utf-8', errors='ignore')
                for pin in re.findall(r'<pin[^>]*>(.*?)</pin>', nsc, re.DOTALL):
                    fp['nsc_pins'].append(pin.strip())

            # Manifest (binary XML — partial string extraction)
            if 'AndroidManifest.xml' in names:
                manifest = z.read('AndroidManifest.xml').decode('utf-8', errors='ignore')
                if 'debuggable' in manifest: fp['debuggable'] = True
                if 'allowBackup' in manifest: fp['backup_enabled'] = True
                if 'usesCleartextTraffic' in manifest: fp['cleartext'] = True

            # DEX: permissions via strings
            for dex in [n for n in names if n.endswith('.dex')][:3]:
                content = z.read(dex).decode('utf-8', errors='ignore')
                perms = re.findall(r'android\.permission\.\w+', content)
                fp['permissions'].extend(perms)
            fp['permissions'] = sorted(set(fp['permissions']))

    except Exception as e:
        fp['error'] = str(e)
    return fp

def diff_apks(apk_path_a: Path, apk_path_b: Path) -> dict:
    """Compare two APKs and return security-relevant diff."""
    fp_a = _get_apk_fingerprint(apk_path_a)
    fp_b = _get_apk_fingerprint(apk_path_b)

    def list_diff(a, b):
        return {'added': sorted(set(b) - set(a)), 'removed': sorted(set(a) - set(b))}

    perms_diff = list_diff(fp_a['permissions'], fp_b['permissions'])
    libs_diff  = list_diff(fp_a['native_libs'], fp_b['native_libs'])
    fw_diff    = list_diff(fp_a['frameworks'], fp_b['frameworks'])
    pin_diff   = list_diff(fp_a['nsc_pins'],  fp_b['nsc_pins'])

    # Flag security-significant changes
    flags = []
    DANGEROUS_PERMS = {
        'READ_SMS', 'SEND_SMS', 'READ_CONTACTS', 'READ_CALL_LOG',
        'ACCESS_FINE_LOCATION', 'CAMERA', 'RECORD_AUDIO',
        'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE',
        'GET_ACCOUNTS', 'USE_BIOMETRIC', 'USE_FINGERPRINT',
    }
    for p in perms_diff['added']:
        pname = p.split('.')[-1]
        if pname in DANGEROUS_PERMS:
            flags.append({'severity': 'high', 'change': f'Dangerous permission ADDED: {p}'})

    if fp_b['debuggable'] and not fp_a['debuggable']:
        flags.append({'severity': 'critical', 'change': 'debuggable=true ADDED (prod build has debug enabled)'})
    if fp_a['debuggable'] and not fp_b['debuggable']:
        flags.append({'severity': 'info', 'change': 'debuggable=true REMOVED (improvement)'})

    if fp_b['cleartext'] and not fp_a['cleartext']:
        flags.append({'severity': 'high', 'change': 'usesCleartextTraffic ADDED'})

    if pin_diff['removed']:
        flags.append({'severity': 'high', 'change': f'{len(pin_diff["removed"])} certificate pin(s) REMOVED from NSC'})
    if pin_diff['added']:
        flags.append({'severity': 'info', 'change': f'{len(pin_diff["added"])} certificate pin(s) ADDED to NSC'})

    if not fp_b['has_nsc'] and fp_a['has_nsc']:
        flags.append({'severity': 'high', 'change': 'Network Security Config REMOVED entirely'})

    for lib in libs_diff['added']:
        if any(x in lib.lower() for x in ['frida', 'xposed', 'substrate']):
            flags.append({'severity': 'critical', 'change': f'Suspicious library ADDED: {lib}'})

    return {
        'apk_a': fp_a['file'],
        'apk_b': fp_b['file'],
        'permissions': perms_diff,
        'native_libs': libs_diff,
        'frameworks': fw_diff,
        'nsc_pins': pin_diff,
        'security_flags': sorted(flags, key=lambda x: {'critical':0,'high':1,'medium':2,'info':3}.get(x['severity'],4)),
        'security_changes': len(flags),
    }

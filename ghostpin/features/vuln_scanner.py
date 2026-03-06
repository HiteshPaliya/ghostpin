"""
GhostPin Enterprise v5.0 — Feature: Vulnerability Scanner (SAST)
Static analysis of APK/IPA for hardcoded secrets, weak crypto, misconfigurations.
"""
import re
import zipfile
import threading
from pathlib import Path

# ── Secret Pattern Library ────────────────────────────────────────
# Patterns are pre-compiled at module load — not inside the scan loop.
# This eliminates re.compile() overhead on every file scanned (35+ cycles per scan).
_RAW_SECRET_PATTERNS = [
    ('GOOGLE_API_KEY',      r'AIza[0-9A-Za-z\-_]{35}',                                          'critical'),
    ('AWS_ACCESS_KEY',      r'AKIA[0-9A-Z]{16}',                                                 'critical'),
    ('AWS_SECRET_KEY',      r'(?i)aws.{0,20}secret.{0,20}["\']([A-Za-z0-9/+=]{40})["\']',       'critical'),
    ('FIREBASE_URL',        r'https://[a-z0-9-]+\.firebaseio\.com',                              'high'),
    ('FIREBASE_KEY',        r'(?i)firebase.*["\'][A-Za-z0-9_-]{100,}["\']',                     'high'),
    ('STRIPE_KEY',          r'(?i)(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}',                        'critical'),
    ('GITHUB_TOKEN',        r'(?i)github[_\s]token[":\s=]+([a-z0-9_]{35,40})',                  'critical'),
    ('PRIVATE_KEY',         r'-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----',                'critical'),
    ('GENERIC_SECRET',      r'(?i)(secret|password|passwd|api_key|apikey|auth_token|access_token)["\s:=]+["\']([^"\']{8,})["\']', 'high'),
    ('HARDCODED_PASSWORD',  r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']',            'high'),
    ('OAUTH_CLIENT_SECRET', r'(?i)(client_secret|consumer_secret)\s*[=:]\s*["\'][^"\']{10,}["\']', 'critical'),
    ('BASIC_AUTH',          r'(?i)Authorization:\s*Basic\s+[A-Za-z0-9+/]{20,}={0,2}',          'high'),
    ('JWT_TOKEN',           r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', 'medium'),
    ('SLACK_WEBHOOK',       r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+', 'high'),
    ('SENDGRID_KEY',        r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}',                       'high'),
    ('TWILIO_SID',          r'AC[a-z0-9]{32}',                                                  'medium'),
    ('MAPBOX_TOKEN',        r'pk\.eyJ1[A-Za-z0-9._-]{50,}',                                    'medium'),
    ('INTERNAL_IP',         r'(?<!\d)(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3})(?!\d)', 'low'),
]

_RAW_WEAK_CRYPTO = [
    ('WEAK_ALGO_MD5',   r'(?i)(MD5|MessageDigest\.getInstance\("MD5"\)|DigestUtils\.md5)',   'high'),
    ('WEAK_ALGO_SHA1',  r'(?i)(SHA-1|SHA1)',                                                 'medium'),
    ('WEAK_ALGO_DES',   r'(?i)(Cipher\.getInstance\("DES[/"]|DES/ECB)',                     'critical'),
    ('WEAK_ECB_MODE',   r'(?i)(AES/ECB|DES/ECB|Blowfish/ECB)',                              'critical'),
    ('WEAK_RC4',        r'(?i)(ARCFOUR|RC4|RC2)',                                            'high'),
    ('RANDOM_INSECURE', r'(?i)new\s+Random\(',                                              'medium'),
]

_RAW_ANDROID_MISCONFIG = [
    ('DEBUG_ENABLED',        r'android:debuggable="true"',           'high'),
    ('BACKUP_ENABLED',       r'android:allowBackup="true"',          'medium'),
    ('CLEARTEXT_TRAFFIC',    r'android:usesCleartextTraffic="true"', 'high'),
    ('EXPORTED_NO_PERM',     r'android:exported="true"(?![^>]*android:permission)', 'high'),
    ('CUSTOM_SCHEME',        r'android:scheme="(?!https?)[a-z]+[^"]*"', 'medium'),
    ('WEAK_NETWORK_CONFIG',  r'<base-config cleartextTrafficPermitted="true"', 'high'),
]

# Compile once at import time
SECRET_PATTERNS      = [(n, re.compile(p), s) for n, p, s in _RAW_SECRET_PATTERNS]
WEAK_CRYPTO_PATTERNS = [(n, re.compile(p), s) for n, p, s in _RAW_WEAK_CRYPTO]
ANDROID_MISCONFIG    = [(n, re.compile(p), s) for n, p, s in _RAW_ANDROID_MISCONFIG]
CLEARTEXT_HTTP_RE    = re.compile(r'http://[a-zA-Z0-9._/-]{8,}')

# ── Thread-safe scan results store ───────────────────────────────
_ScanResults: dict = {}
_scan_results_lock = threading.Lock()


def _store_result(scan_id: str, result: dict) -> None:
    with _scan_results_lock:
        _ScanResults[scan_id] = result


def get_result(scan_id: str) -> dict | None:
    with _scan_results_lock:
        return _ScanResults.get(scan_id)


def scan_apk(apk_path) -> dict:
    """Run full SAST scan on APK or IPA. Returns structured findings."""
    apk_path = Path(apk_path)
    result = {
        'ok': True,
        'file': apk_path.name,
        'findings': [],
        'summary': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
        'score': 100,
    }
    severity_weight = {'critical': 30, 'high': 15, 'medium': 7, 'low': 2}

    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            names = z.namelist()

            # ── Scan DEX bytecode ──────────────────────────
            dex_files = [n for n in names if n.endswith('.dex')]
            for dex_name in dex_files[:5]:
                content = z.read(dex_name).decode('utf-8', errors='ignore')
                _scan_content(content, dex_name, result, severity_weight,
                              SECRET_PATTERNS + WEAK_CRYPTO_PATTERNS)
                # Cleartext HTTP check
                for url in list({m for m in CLEARTEXT_HTTP_RE.findall(content)})[:10]:
                    if 'localhost' not in url and '127.0' not in url:
                        _add_finding(result, severity_weight, 'CLEARTEXT_HTTP_URL',
                                     'medium', dex_name, f'Cleartext HTTP URL: {url}')

            # ── Scan XML, JSON, assets ─────────────────────
            text_files = [n for n in names
                          if n.endswith(('.xml', '.json')) or n.startswith('assets/')]
            for fname in text_files[:30]:
                try:
                    content = z.read(fname).decode('utf-8', errors='ignore')
                    _scan_content(content, fname, result, severity_weight, SECRET_PATTERNS)
                    if 'AndroidManifest' in fname or 'network_security_config' in fname:
                        _scan_content(content, fname, result, severity_weight, ANDROID_MISCONFIG)
                except Exception:
                    pass  # Corrupt/binary file — skip without crashing

    except zipfile.BadZipFile:
        result['ok'] = False
        result['error'] = 'Invalid APK/IPA — not a valid ZIP archive.'
    except Exception as e:
        result['ok'] = False
        result['error'] = str(e)

    result['score'] = max(0, result['score'])
    result['grade'] = _score_to_grade(result['score'])
    return result


def _scan_content(content: str, filename: str, result: dict,
                  severity_weight: dict, patterns: list) -> None:
    """Scan content against pre-compiled patterns. Called once per file per pattern set."""
    for name, compiled_pattern, severity in patterns:
        matches = compiled_pattern.findall(content)
        if matches:
            samples = list({str(m)[:80] for m in matches})[:3]
            _add_finding(result, severity_weight, name, severity, filename,
                         f'Pattern matched: {samples[0]}', evidence=samples)


def _add_finding(result: dict, severity_weight: dict, vuln_type: str,
                 severity: str, location: str, detail: str,
                 evidence: list | None = None) -> None:
    """Add a finding, deduplicating by (type, location)."""
    for existing in result['findings']:
        if existing['type'] == vuln_type and existing['location'] == location:
            return
    result['findings'].append({
        'type': vuln_type,
        'severity': severity,
        'location': location,
        'detail': detail,
        'evidence': evidence or [],
    })
    result['summary'][severity] = result['summary'].get(severity, 0) + 1
    result['score'] -= severity_weight.get(severity, 0)


def _score_to_grade(score: int) -> str:
    if score >= 90: return 'A'
    if score >= 75: return 'B'
    if score >= 60: return 'C'
    if score >= 40: return 'D'
    result['summary'][severity] = result['summary'].get(severity, 0) + 1
    result['score'] -= severity_weight.get(severity, 0)

def _score_to_grade(score: int) -> str:
    if score >= 90: return 'A'
    if score >= 75: return 'B'
    if score >= 60: return 'C'
    if score >= 40: return 'D'
    return 'F'

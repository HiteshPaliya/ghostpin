"""
GhostPin v5 Phase 2 — Feature: CVE / SDK Vulnerability Checker
Scans APK for library versions and queries OSV.dev for known CVEs.
"""
import re, json, zipfile
from pathlib import Path

# Library version detection patterns in DEX strings
LIBRARY_PATTERNS = [
    ('OkHttp',         r'okhttp/(\d+\.\d+[\.\d]*)',                 'com.squareup.okhttp3:okhttp'),
    ('Retrofit',       r'retrofit/(\d+\.\d+[\.\d]*)',               'com.squareup.retrofit2:retrofit'),
    ('Gson',           r'Gson/(\d+\.\d+[\.\d]*)',                   'com.google.code.gson:gson'),
    ('Firebase',       r'firebase-(\w+)/(\d+\.\d+[\.\d]*)',         'com.google.firebase:firebase-bom'),
    ('Log4j',          r'log4j.(\d+\.\d+[\.\d]*)',                  'org.apache.logging.log4j:log4j-core'),
    ('Apache Commons', r'commons-(\w+)/(\d+\.\d+[\.\d]*)',          'commons-codec:commons-codec'),
    ('Bouncy Castle',  r'bcprov-jdk\d+-(\d+\.\d+[\.\d]*)',          'org.bouncycastle:bcprov-jdk15on'),
    ('ExoPlayer',      r'ExoPlayerLib/(\d+\.\d+[\.\d]*)',           'com.google.android.exoplayer:exoplayer'),
    ('Picasso',        r'Picasso/(\d+\.\d+[\.\d]*)',                'com.squareup.picasso:picasso'),
    ('Glide',          r'Glide/(\d+\.\d+[\.\d]*)',                  'com.github.bumptech.glide:glide'),
    ('Conscrypt',      r'conscrypt/(\d+\.\d+[\.\d]*)',              'org.conscrypt:conscrypt-android'),
    ('PlayCore',       r'play-core/(\d+\.\d+[\.\d]*)',              'com.google.android.play:core'),
]

# Manually known dangerous versions (as fallback when OSV is down)
KNOWN_VULN_VERSIONS = {
    'com.squareup.okhttp3:okhttp': [
        {'version_range': '<3.12.13', 'cve': 'CVE-2021-0341', 'severity': 'HIGH',
         'summary': 'OkHttp hostname verification bypass via wildcard certificates'},
    ],
    'org.apache.logging.log4j:log4j-core': [
        {'version_range': '<2.17.1', 'cve': 'CVE-2021-44228', 'severity': 'CRITICAL',
         'summary': 'Log4Shell — remote code execution via JNDI lookup in log messages'},
        {'version_range': '<2.17.1', 'cve': 'CVE-2021-45046', 'severity': 'CRITICAL',
         'summary': 'Log4j2 JNDI lookup RCE — incomplete fix for Log4Shell'},
    ],
    'org.bouncycastle:bcprov-jdk15on': [
        {'version_range': '<1.70', 'cve': 'CVE-2020-26939', 'severity': 'MEDIUM',
         'summary': 'Bouncy Castle padding oracle in CBC mode decryption'},
    ],
}

def _parse_version(v: str):
    """Parse version string into tuple for comparison."""
    try:
        return tuple(int(x) for x in re.split(r'[._-]', v) if x.isdigit())
    except Exception:
        return (0,)

def _version_lt(v: str, bound: str) -> bool:
    return _parse_version(v) < _parse_version(bound)

def _check_known_vulns(pkg: str, version: str) -> list:
    findings = []
    for vuln in KNOWN_VULN_VERSIONS.get(pkg, []):
        vr = vuln['version_range']
        op = vr[:1]
        bound = vr[1:].strip()
        if op == '<' and version and _version_lt(version, bound):
            findings.append({
                'cve': vuln['cve'],
                'severity': vuln['severity'],
                'summary': vuln['summary'],
                'affected_version': version,
                'fix_version': bound,
            })
    return findings

def _query_osv(package_name: str, version: str, ecosystem: str = 'Maven') -> list:
    """Query OSV.dev API for vulnerabilities."""
    import urllib.request
    try:
        payload = json.dumps({
            'package': {'name': package_name, 'ecosystem': ecosystem},
            'version': version,
        }).encode()
        req = urllib.request.Request(
            'https://api.osv.dev/v1/query',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'GhostPin/5.0'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
        vulns = []
        for v in data.get('vulns', []):
            sev = 'UNKNOWN'
            cvss = None
            for s in v.get('severity', []):
                sev = s.get('score', 'UNKNOWN')
                break
            for db in v.get('database_specific', {}).values():
                if isinstance(db, dict):
                    cvss = db.get('cvss_score')
            vulns.append({
                'cve': v.get('id', ''),
                'severity': sev,
                'summary': v.get('summary', '')[:120],
                'fix_version': _extract_fix_version(v),
                'cvss': cvss,
            })
        return vulns
    except Exception:
        return []

def _extract_fix_version(vuln: dict) -> str:
    for affected in vuln.get('affected', []):
        for rng in affected.get('ranges', []):
            for event in rng.get('events', []):
                if 'fixed' in event:
                    return event['fixed']
    return ''

def detect_libraries(apk_path: Path) -> list:
    """Scan APK DEX files for library version strings."""
    found = []
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            dex_files = [n for n in z.namelist() if n.endswith('.dex')]
            for dex_name in dex_files[:5]:
                try:
                    content = z.read(dex_name).decode('utf-8', errors='ignore')
                    for lib_name, pattern, pkg_id in LIBRARY_PATTERNS:
                        for m in re.finditer(pattern, content):
                            version = m.group(m.lastindex) if m.lastindex else ''
                            if version and not any(f['library'] == lib_name and f['version'] == version for f in found):
                                found.append({'library': lib_name, 'version': version, 'package': pkg_id})
                except Exception:
                    pass
    except Exception:
        pass
    return found

def check_cves(apk_path: Path, use_osv: bool = True) -> dict:
    """Full CVE check: detect libraries, query OSV, return findings."""
    libraries = detect_libraries(apk_path)
    results = {'libraries': libraries, 'vulnerabilities': [], 'scanned': len(libraries)}

    for lib in libraries:
        # Try OSV first
        if use_osv:
            osv_findings = _query_osv(lib['package'], lib['version'])
            for f in osv_findings:
                results['vulnerabilities'].append({**f, 'library': lib['library'], 'version': lib['version']})
        # Apply offline known-vulns
        offline = _check_known_vulns(lib['package'], lib['version'])
        for f in offline:
            if not any(v.get('cve') == f['cve'] for v in results['vulnerabilities']):
                results['vulnerabilities'].append({**f, 'library': lib['library'], 'version': lib['version']})

    # Sort by severity
    sev_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'UNKNOWN': 4}
    results['vulnerabilities'].sort(key=lambda x: sev_order.get(x.get('severity', ''), 4))
    results['critical_count'] = sum(1 for v in results['vulnerabilities'] if v.get('severity') == 'CRITICAL')
    results['high_count'] = sum(1 for v in results['vulnerabilities'] if v.get('severity') == 'HIGH')
    return results

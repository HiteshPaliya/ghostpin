"""
GhostPin v5 Phase 2 — Feature: SARIF + JSON Export
Export scanner findings in SARIF 2.1.0 and JSON formats for CI/CD integration.
"""
import json
from pathlib import Path
from datetime import datetime

SARIF_VERSION = '2.1.0'
SARIF_SCHEMA  = 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json'

RULE_METADATA = {
    'HARDCODED_AWS_KEY':      {'name': 'Hardcoded AWS Key',         'cwe': 'CWE-798', 'severity': 'critical'},
    'HARDCODED_GOOGLE_KEY':   {'name': 'Hardcoded Google API Key',   'cwe': 'CWE-798', 'severity': 'high'},
    'HARDCODED_STRIPE_KEY':   {'name': 'Hardcoded Stripe Live Key',  'cwe': 'CWE-798', 'severity': 'critical'},
    'HARDCODED_FIREBASE_URL': {'name': 'Hardcoded Firebase URL',     'cwe': 'CWE-798', 'severity': 'high'},
    'HARDCODED_PRIVATE_KEY':  {'name': 'Hardcoded Private Key',      'cwe': 'CWE-321', 'severity': 'critical'},
    'HARDCODED_PASSWORD':     {'name': 'Hardcoded Password',         'cwe': 'CWE-259', 'severity': 'high'},
    'WEAK_CRYPTO_MD5':        {'name': 'MD5 in Use',                 'cwe': 'CWE-327', 'severity': 'high'},
    'WEAK_CRYPTO_SHA1':       {'name': 'SHA-1 in Use',               'cwe': 'CWE-327', 'severity': 'medium'},
    'WEAK_CRYPTO_DES':        {'name': 'DES in Use',                 'cwe': 'CWE-327', 'severity': 'high'},
    'WEAK_CRYPTO_ECB':        {'name': 'AES-ECB Mode in Use',        'cwe': 'CWE-327', 'severity': 'high'},
    'WEAK_RANDOM':            {'name': 'Insecure Random',            'cwe': 'CWE-330', 'severity': 'medium'},
    'DEBUGGABLE':             {'name': 'Debuggable Build',           'cwe': 'CWE-489', 'severity': 'high'},
    'ALLOW_BACKUP':           {'name': 'Backup Enabled',             'cwe': 'CWE-312', 'severity': 'medium'},
    'CLEARTEXT_TRAFFIC':      {'name': 'Cleartext HTTP Traffic',     'cwe': 'CWE-319', 'severity': 'high'},
    'EXPORTED_COMPONENT':     {'name': 'Exported Component',         'cwe': 'CWE-926', 'severity': 'medium'},
}

_SARIF_LEVEL = {'critical': 'error', 'high': 'error', 'medium': 'warning', 'low': 'note'}

def to_sarif(findings: list, app_name: str = 'GhostPin Scan', apk_path: str = '') -> dict:
    """Convert scan findings to SARIF 2.1.0 format."""
    # Build unique rules list
    rules_seen = {}
    results = []
    for f in findings:
        rule_id = f.get('type', 'UNKNOWN').upper().replace(' ', '_')
        meta = RULE_METADATA.get(rule_id, {
            'name': f.get('type', rule_id), 'cwe': 'CWE-200', 'severity': f.get('severity', 'medium')
        })
        if rule_id not in rules_seen:
            rules_seen[rule_id] = {
                'id': rule_id,
                'name': meta['name'],
                'shortDescription': {'text': meta['name']},
                'fullDescription': {'text': f.get('detail', meta['name'])},
                'helpUri': f'https://cwe.mitre.org/data/definitions/{meta["cwe"].replace("CWE-","")}.html',
                'properties': {'tags': [meta['cwe'], 'security', meta['severity']]},
                'defaultConfiguration': {'level': _SARIF_LEVEL.get(meta['severity'], 'warning')},
            }
        location = f.get('location', apk_path or app_name)
        evidence = (f.get('evidence') or [''])[0][:100] if f.get('evidence') else ''
        results.append({
            'ruleId': rule_id,
            'level': _SARIF_LEVEL.get(f.get('severity', 'medium'), 'warning'),
            'message': {'text': f'{f.get("detail", "")}' + (f'\n\nEvidence: {evidence}' if evidence else '')},
            'locations': [{
                'physicalLocation': {
                    'artifactLocation': {'uri': location},
                    'region': {'startLine': 1},
                },
            }],
            'properties': {'severity': f.get('severity', 'medium')},
        })

    return {
        '$schema': SARIF_SCHEMA,
        'version': SARIF_VERSION,
        'runs': [{
            'tool': {
                'driver': {
                    'name': 'GhostPin',
                    'version': '5.0.0',
                    'informationUri': 'https://github.com/ghostpin/ghostpin',
                    'rules': list(rules_seen.values()),
                }
            },
            'artifacts': [{'location': {'uri': apk_path}, 'description': {'text': app_name}}] if apk_path else [],
            'results': results,
            'invocations': [{
                'executionSuccessful': True,
                'startTimeUtc': datetime.utcnow().isoformat() + 'Z',
            }],
        }]
    }

def to_json_report(findings: list, app_name: str, scan_meta: dict = None) -> dict:
    """Export in structured JSON format for SIEM/ticketing integrations."""
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for f in findings:
        sev = f.get('severity', 'low')
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    return {
        'schema_version': '1.0',
        'tool': 'GhostPin v5.0',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'target': {
            'app_name': app_name,
            **(scan_meta or {}),
        },
        'summary': {
            **severity_counts,
            'total': len(findings),
        },
        'findings': findings,
    }

def save_sarif(findings: list, app_name: str, apk_path: str = '') -> Path:
    """Save SARIF file to reports dir, return path."""
    reports_dir = Path.home() / '.ghostpin' / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = reports_dir / f'scan_{ts}.sarif'
    out.write_text(json.dumps(to_sarif(findings, app_name, apk_path), indent=2))
    return out

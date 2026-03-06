"""
GhostPin v5.0 — Feature: Intent Fuzzer
Enumerates exported Android components and fires crafted Intents via ADB.
"""

import json
import re
from ghostpin.core.adb import run_cmd, adb_shell

# ── Payload Library ──────────────────────────────────────────────
PAYLOADS = {
    'null':          [''],
    'overflow':      ['A' * 4096, 'A' * 65535],
    'sqli':          ["' OR 1=1--", "'; DROP TABLE users;--", "1 UNION SELECT null,null--"],
    'traversal':     ['../../../etc/passwd', '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
                      'file:///etc/passwd', 'content://com.android.contacts/contacts'],
    'xss':           ['<script>alert(1)</script>', "javascript:alert(1)", '"><img src=x onerror=alert(1)>'],
    'format_str':    ['%s%s%s%s%s', '%x%x%x%x', '%n%n%n%n'],
    'uri_schemes':   ['javascript://', 'file://', 'data:text/html,<script>alert(1)</script>',
                      'intent://evil.host#Intent;scheme=http;end'],
    'deep_link':     ['https://evil.example.com/redirect', 'market://details?id=com.evil'],
}

def enumerate_components(serial: str, package: str) -> dict:
    """Use adb shell dumpsys to get exported activities, services, receivers, providers."""
    out = adb_shell(serial, f'dumpsys package {package}')
    result = {
        'activities': [],
        'services': [],
        'receivers': [],
        'providers': [],
        'intentFilters': {},
    }

    # Parse Activity section
    act_section = False
    for line in out.split('\n'):
        line = line.strip()
        if 'Activity Resolver Table:' in line or 'Activity Aliases:' in line:
            act_section = True
        if act_section and package in line and '/' in line:
            comp_m = re.search(r'([\w.]+/[\w.$]+)', line)
            if comp_m and comp_m.group(1) not in result['activities']:
                result['activities'].append(comp_m.group(1))

    # Parse Services
    out2 = adb_shell(serial, f'pm dump {package}')
    for line in out2.split('\n'):
        line = line.strip()
        if 'Service {' in line and package in line:
            svc_m = re.search(r'([\w.]+/[\w.$]+)', line)
            if svc_m:
                result['services'].append(svc_m.group(1))
        if 'Receiver {' in line and package in line:
            rec_m = re.search(r'([\w.]+/[\w.$]+)', line)
            if rec_m:
                result['receivers'].append(rec_m.group(1))

    # Get intent filters via pm
    result['activities'] = list(set(result['activities']))[:40]
    result['services'] = list(set(result['services']))[:20]
    result['receivers'] = list(set(result['receivers']))[:20]
    return result

def fire_intent(serial: str, component: str, action: str = '',
                data: str = '', extras: dict = None, component_type: str = 'activity') -> dict:
    """Fire an ADB Intent at a component."""
    cmd_parts = ['am']
    if component_type == 'activity':
        cmd_parts += ['start', '-n', component]
    elif component_type == 'service':
        cmd_parts += ['startservice', '-n', component]
    elif component_type == 'broadcast':
        cmd_parts += ['broadcast', '-n', component]

    if action:
        cmd_parts += ['-a', action]
    if data:
        cmd_parts += ['-d', data]
    if extras:
        for k, v in extras.items():
            cmd_parts += ['--es', k, str(v)]

    cmd_str = ' '.join(cmd_parts)
    out, err, rc = run_cmd(['adb', '-s', serial, 'shell', cmd_str], timeout=8)
    return {
        'cmd': cmd_str,
        'stdout': out,
        'stderr': err,
        'rc': rc,
        'interesting': _is_interesting(out + err),
    }

def _is_interesting(output: str) -> bool:
    """Flag results that look like crashes, errors, leaks."""
    bad_patterns = [
        'Exception', 'NullPointerException', 'Fatal exception', 'ANR', 'Crash',
        'file not found', 'Permission denied', 'SecurityException',
        'ClassCastException', 'StackOverflow', 'OutOfMemory',
        'SQL', 'database', 'INTENT_ACTION', 'content://',
    ]
    return any(p.lower() in output.lower() for p in bad_patterns)

def fuzz_component(serial: str, component: str, comp_type: str,
                   payload_categories: list = None) -> list:
    """Fuzz a component across selected payload categories. Returns list of results."""
    if payload_categories is None:
        payload_categories = list(PAYLOADS.keys())

    results = []
    # Null intent first
    results.append(fire_intent(serial, component, component_type=comp_type))

    # Payload fuzzing
    extra_keys = ['id', 'token', 'url', 'username', 'data', 'redirect', 'path', 'cmd']
    for category in payload_categories:
        for payload in PAYLOADS.get(category, [])[:3]:  # limit to 3 per category
            for key in extra_keys[:3]:
                result = fire_intent(
                    serial, component,
                    data=payload if category in ('uri_schemes', 'deep_link', 'traversal') else '',
                    extras={key: payload} if category not in ('uri_schemes', 'traversal') else {},
                    component_type=comp_type
                )
                result['payload_category'] = category
                result['payload_key'] = key
                result['payload_value'] = payload
                results.append(result)

    return results

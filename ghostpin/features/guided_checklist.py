"""
GhostPin v5 Phase 2 — Feature: Guided Testing Checklist
App-type detection → recommended workflow with step-by-step checklist.
"""

# Step definition: id, title, page to navigate to, explanation
CHECKLISTS = {
    'banking': {
        'name': 'Banking / Fintech App',
        'icon': '🏦',
        'risk': 'CRITICAL',
        'steps': [
            {'id':'b1', 'title':'APK Static Analysis',         'page':'scanner',  'why':'Find hardcoded API keys, weak crypto, debuggable=true before touching the device.'},
            {'id':'b2', 'title':'CVE Library Check',           'page':'cve',      'why':'Banking apps use OkHttp, Firebase, BouncyCastle — check all for known CVEs.'},
            {'id':'b3', 'title':'Device Integrity Bypass',     'page':'bypass',   'why':'Enable SafetyNet + Play Integrity script — banks check this first.','scripts':['universal-android-bypass','safetynet-play-integrity']},
            {'id':'b4', 'title':'SSL Pinning Bypass',          'page':'bypass',   'why':'Add certificate pinning bypass — banking apps always pin.'},
            {'id':'b5', 'title':'Start API Monitor (Crypto)',   'page':'monitor',  'why':'Log every Cipher call — find MD5/ECB/weak keys during login + transaction.'},
            {'id':'b6', 'title':'Intent Fuzzer — OAuth flows', 'page':'fuzzer',   'why':'Fuzz exported OAuth redirect activities — open redirect → account takeover.'},
            {'id':'b7', 'title':'Class Tracer — Auth classes', 'page':'tracer',   'why':'Trace the authentication and session management classes live.'},
            {'id':'b8', 'title':'Generate Report',             'page':'reports',  'why':'Compile all findings into a client-ready report.'},
        ]
    },
    'gaming': {
        'name': 'Gaming / Anti-Cheat',
        'icon': '🎮',
        'risk': 'HIGH',
        'steps': [
            {'id':'g1', 'title':'APK Static Analysis',            'page':'scanner', 'why':'Detect Unity/IL2CPP, check for debuggable, exported components.'},
            {'id':'g2', 'title':'Gaming Anti-Cheat Bypass',        'page':'bypass',  'why':'Enable EasyAntiCheat/BattlEye bypass before injection.','scripts':['anti-cheat-gaming','universal-android-bypass']},
            {'id':'g3', 'title':'IL2CPP Class Dump',               'page':'tracer',  'why':'Enumerate all IL2CPP exports — find SSL verification, game state classes.'},
            {'id':'g4', 'title':'API Monitor — Network calls',     'page':'monitor', 'why':'Capture every TCP connection to game servers — look for unencrypted game state.'},
            {'id':'g5', 'title':'Intent Fuzzer — Deep links',      'page':'fuzzer',  'why':'Mobile games often have promotion deep links with SQL/path issues.'},
            {'id':'g6', 'title':'Generate Report',                 'page':'reports', 'why':'Document findings for game studio.'},
        ]
    },
    'enterprise': {
        'name': 'Enterprise / MDM App',
        'icon': '🏢',
        'risk': 'HIGH',
        'steps': [
            {'id':'e1', 'title':'MDM Profile',                    'page':'mdm',     'why':'Identify MDM vendor before attempting any bypass — MDM can block ADB.'},
            {'id':'e2', 'title':'APK Static Analysis',            'page':'scanner', 'why':'Enterprise apps hardcode internal API URLs, LDAP passwords, client certs.'},
            {'id':'e3', 'title':'Device Integrity Bypass',        'page':'bypass',  'why':'Enterprise apps may check for device compliance.','scripts':['safetynet-play-integrity']},
            {'id':'e4', 'title':'SSL Pinning Bypass',             'page':'bypass',  'why':'Enterprise apps often use mutual TLS with client certs.','scripts':['universal-android-bypass']},
            {'id':'e5', 'title':'API Monitor — File I/O',         'page':'monitor', 'why':'Watch file operations — enterprise apps write tokens to insecure locations.'},
            {'id':'e6', 'title':'CVE Library Check',              'page':'cve',     'why':'Enterprise apps may ship outdated SDKs with known CVEs.'},
            {'id':'e7', 'title':'Intent Fuzzer',                  'page':'fuzzer',  'why':'Enterprise workflows often have exported activities for SSO callbacks.'},
            {'id':'e8', 'title':'Generate Report',                'page':'reports', 'why':'Enterprise clients require formal pentest deliverables.'},
        ]
    },
    'react_native': {
        'name': 'React Native / Flutter',
        'icon': '⚛️',
        'risk': 'HIGH',
        'steps': [
            {'id':'r1', 'title':'APK Static Analysis',            'page':'scanner', 'why':'Detect framework, find secrets in JS bundle or Dart snapshot.'},
            {'id':'r2', 'title':'Hermes JS Bundle Extraction',    'page':'scanner', 'why':'Decompile Hermes bytecode to find API endpoints and secrets.'},
            {'id':'r3', 'title':'React Native / Hermes Bypass',  'page':'bypass',  'why':'Standard OkHttp3 bypass is insufficient for Hermes apps.','scripts':['react-native-hermes','universal-android-bypass']},
            {'id':'r4', 'title':'API Monitor — Network',          'page':'monitor', 'why':'Capture native fetch() and XMLHttpRequest calls.'},
            {'id':'r5', 'title':'Class Tracer — Native bridge',   'page':'tracer',  'why':'Trace JSI bridge calls — see JS→native data crossing.'},
            {'id':'r6', 'title':'CVE Library Check',              'page':'cve',     'why':'RN apps ship many npm-turned-native dependencies with CVEs.'},
            {'id':'r7', 'title':'Generate Report',                'page':'reports', 'why':'Summarize all findings.'},
        ]
    },
    'generic': {
        'name': 'Generic / Unknown App',
        'icon': '📱',
        'risk': 'MEDIUM',
        'steps': [
            {'id':'x1', 'title':'APK Static Analysis',            'page':'scanner', 'why':'First step for all assessments — understand the app.'},
            {'id':'x2', 'title':'CVE Library Check',              'page':'cve',     'why':'Check all detected libraries against known CVE databases.'},
            {'id':'x3', 'title':'SSL Pinning Bypass',             'page':'bypass',  'why':'Intercept API traffic.','scripts':['universal-android-bypass']},
            {'id':'x4', 'title':'API Monitor',                    'page':'monitor', 'why':'Observe runtime behavior.'},
            {'id':'x5', 'title':'Intent Fuzzer',                  'page':'fuzzer',  'why':'Test exported component attack surface.'},
            {'id':'x6', 'title':'Generate Report',                'page':'reports', 'why':'Document findings.'},
        ]
    },
}

FRAMEWORK_CHECKLIST_MAP = {
    'React Native':  'react_native',
    'Flutter':       'react_native',
    'Unity/IL2CPP':  'gaming',
    'Xamarin':       'react_native',
}

def detect_app_type(scan_result: dict) -> str:
    """Suggest best checklist based on scan result."""
    frameworks = scan_result.get('frameworks', [])
    for fw in frameworks:
        if fw in FRAMEWORK_CHECKLIST_MAP:
            return FRAMEWORK_CHECKLIST_MAP[fw]
    findings = scan_result.get('findings', [])
    types = [f.get('type', '') for f in findings]
    if any('MDM' in t for t in types): return 'enterprise'
    if any('BANK' in t or 'PAYMENT' in t for t in types): return 'banking'
    return 'generic'

def get_checklist(app_type: str) -> dict:
    return CHECKLISTS.get(app_type, CHECKLISTS['generic'])

def all_checklists() -> dict:
    return CHECKLISTS

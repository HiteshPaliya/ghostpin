"""
GhostPin v5 - iOS Static Analyzer
Unpacks IPAs and analyzes Info.plist for common security misconfigurations.
"""
import os
import zipfile
import plistlib
from pathlib import Path

def analyze_ipa(ipa_path: str) -> dict:
    """Analyze an iOS .ipa file for security misconfigurations."""
    results = {
        'app_name': 'Unknown',
        'bundle_id': 'Unknown',
        'version': 'Unknown',
        'url_schemes': [],
        'ats_misconfigurations': [],
        'permissions': [],
        'findings': [],
        'grade': 'A'  # Start at A, subtract for findings
    }
    
    score_deduction = 0
    
    try:
        with zipfile.ZipFile(ipa_path, 'r') as zf:
            # Find Info.plist
            # It's usually at Payload/AppName.app/Info.plist
            plist_info = None
            for info in zf.infolist():
                if info.filename.startswith('Payload/') and info.filename.endswith('.app/Info.plist'):
                    plist_info = info
                    break
                    
            if not plist_info:
                return {'ok': False, 'error': 'Info.plist not found in IPA. Is this a valid iOS app?'}
                
            with zf.open(plist_info) as f:
                try:
                    # plistlib can read both XML and binary plists in Python 3.4+
                    plist = plistlib.load(f)
                except Exception as parse_e:
                    return {'ok': False, 'error': f'Failed to parse Info.plist: {parse_e}'}
                    
            # 1. Basic Metadata
            results['app_name'] = plist.get('CFBundleDisplayName', plist.get('CFBundleName', 'Unknown'))
            results['bundle_id'] = plist.get('CFBundleIdentifier', 'Unknown')
            results['version'] = plist.get('CFBundleShortVersionString', 'Unknown')
            
            # 2. Extract URL Schemes (High value for fuzzing)
            url_types = plist.get('CFBundleURLTypes', [])
            for ut in url_types:
                schemes = ut.get('CFBundleURLSchemes', [])
                for s in schemes:
                    results['url_schemes'].append(f"{s}://")
            
            if results['url_schemes']:
                results['findings'].append({
                    'title': 'Custom URL Schemes Defined',
                    'severity': 'INFO',
                    'desc': f"Found {len(results['url_schemes'])} custom URI handlers. These should be fuzzed for XSS or Path Traversal.",
                    'evidence': ", ".join(results['url_schemes'])
                })
            
            # 3. App Transport Security (ATS) Misconfigs
            ats = plist.get('NSAppTransportSecurity', {})
            if ats:
                if ats.get('NSAllowsArbitraryLoads', False):
                    results['findings'].append({
                        'title': 'Insecure ATS Configuration (NSAllowsArbitraryLoads)',
                        'severity': 'HIGH',
                        'desc': 'The app completely disables iOS App Transport Security, allowing cleartext HTTP traffic globally.',
                        'evidence': '<key>NSAllowsArbitraryLoads</key><true/>'
                    })
                    score_deduction += 30
                    results['ats_misconfigurations'].append('NSAllowsArbitraryLoads is TRUE')
                    
                exceptions = ats.get('NSExceptionDomains', {})
                for domain, config in exceptions.items():
                    if config.get('NSExceptionAllowsInsecureHTTPLoads', False):
                        results['findings'].append({
                            'title': 'Insecure ATS Domain Exception',
                            'severity': 'MEDIUM',
                            'desc': f'Cleartext HTTP traffic is explicitly allowed for domain: {domain}',
                            'evidence': f"Domain: {domain}"
                        })
                        score_deduction += 10
                        results['ats_misconfigurations'].append(f'{domain} allows insecure loads')
            
            # 4. Sensitive Privacy Permissions
            privacy_keys = [k for k in plist.keys() if k.startswith('NS') and k.endswith('UsageDescription')]
            for k in privacy_keys:
                results['permissions'].append({
                    'key': k,
                    'reason': plist[k]
                })

            # Calculate Grade
            results['grade'] = 'F' if score_deduction >= 50 else \
                               'D' if score_deduction >= 30 else \
                               'C' if score_deduction >= 20 else \
                               'B' if score_deduction >= 10 else 'A'
                               
            results['ok'] = True
            return results
            
    except zipfile.BadZipFile:
        return {'ok': False, 'error': 'Invalid IPA file. Not a valid ZIP archive.'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

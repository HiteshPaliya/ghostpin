"""
GhostPin v5 Phase 2 — Feature: Per-Target Project Workspace
Saves/loads settings, scan results, sessions per target package name.
"""
import json
from pathlib import Path
from datetime import datetime

WORKSPACES_DIR = Path.home() / '.ghostpin' / 'workspaces'

def _ws_path(package: str) -> Path:
    safe = package.replace('/', '_').replace('\\', '_')
    return WORKSPACES_DIR / f'{safe}.json'

def _load(package: str) -> dict:
    p = _ws_path(package)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return {
        'package': package,
        'created': datetime.now().isoformat(),
        'notes': '',
        'preferred_scripts': ['universal-android-bypass'],
        'proxy': {'host': '127.0.0.1', 'port': 8080},
        'serial': '',
        'spawn_mode': False,
        'anti_detection': {},
        'scan_results': None,
        'cve_results': None,
        'mdm_results': None,
        'session_ids': [],
        'tags': [],
        'last_used': '',
    }

def _save(data: dict):
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    data['last_used'] = datetime.now().isoformat()
    _ws_path(data['package']).write_text(json.dumps(data, indent=2))

def get_workspace(package: str) -> dict:
    return _load(package)

def save_workspace(package: str, updates: dict) -> dict:
    ws = _load(package)
    ws.update(updates)
    ws['package'] = package
    _save(ws)
    return ws

def list_workspaces() -> list:
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    result = []
    for f in sorted(WORKSPACES_DIR.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            data = json.loads(f.read_text())
            result.append({
                'package': data.get('package', f.stem),
                'last_used': data.get('last_used', ''),
                'tags': data.get('tags', []),
                'has_scan': data.get('scan_results') is not None,
                'has_cve': data.get('cve_results') is not None,
                'notes': data.get('notes', '')[:60],
            })
        except Exception:
            pass
    return result

def delete_workspace(package: str) -> bool:
    p = _ws_path(package)
    if p.exists():
        p.unlink()
        return True
    return False

def attach_session(package: str, session_id: str):
    ws = _load(package)
    if session_id not in ws['session_ids']:
        ws['session_ids'].append(session_id)
    _save(ws)

def attach_scan(package: str, scan_result: dict):
    ws = _load(package)
    ws['scan_results'] = scan_result
    _save(ws)

def attach_cve(package: str, cve_result: dict):
    ws = _load(package)
    ws['cve_results'] = cve_result
    _save(ws)

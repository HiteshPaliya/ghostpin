"""
GhostPin v5 Phase 2 — Feature: Traffic Intercept & Replay
Real mitmproxy integration: launch as subprocess, capture flows,
enable replay and modification of captured requests.
"""
import json, subprocess, threading, time, os, signal
from pathlib import Path
from datetime import datetime

FLOWS_DIR = Path.home() / '.ghostpin' / 'flows'
MITM_PORT = 8877   # port mitmproxy listens on
MITM_API  = 8878   # mitmproxy's built-in REST API port

_procs: dict = {}   # session_id -> Popen

def start_capture(session_id: str, listen_port: int = MITM_PORT) -> dict:
    """Start mitmproxy in API mode, capture flows to file."""
    FLOWS_DIR.mkdir(parents=True, exist_ok=True)
    flow_file = FLOWS_DIR / f'{session_id}.flow'

    cmd = [
        'mitmdump',
        '--listen-port', str(listen_port),
        '--save-stream-file', str(flow_file),
        '-s', str(Path(__file__).parent / 'mitm_addon.py'),
        '--set', f'api_port={MITM_API}',
        '--set', 'stream_large_bodies=10m',
        '-q',  # quiet
    ]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )
        _procs[session_id] = proc
        time.sleep(1.5)  # let it start
        if proc.poll() is not None:
            err = proc.stderr.read(300)
            return {'ok': False, 'error': f'mitmproxy failed to start: {err}'}
        return {
            'ok': True,
            'session_id': session_id,
            'port': listen_port,
            'flow_file': str(flow_file),
            'pid': proc.pid,
        }
    except FileNotFoundError:
        return {'ok': False, 'error': 'mitmdump not found — pip install mitmproxy'}

def stop_capture(session_id: str) -> bool:
    proc = _procs.pop(session_id, None)
    if proc:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        return True
    return False

def list_flows(session_id: str) -> list:
    """Parse saved .flow file and return request summaries."""
    flow_file = FLOWS_DIR / f'{session_id}.flow'
    if not flow_file.exists():
        return []
    flows = []
    try:
        # Use mitmproxy's flow reader if available
        from mitmproxy.io import FlowReader
        from mitmproxy.net.http import http1
        with open(flow_file, 'rb') as f:
            reader = FlowReader(f)
            for i, flow in enumerate(reader.stream()):
                req = flow.request
                resp = flow.response
                flows.append({
                    'id': i,
                    'method': req.method,
                    'host': req.host,
                    'path': req.path[:80],
                    'status': resp.status_code if resp else None,
                    'content_type': (resp.headers.get('content-type', '') if resp else '')[:40],
                    'size': len(resp.content) if resp and resp.content else 0,
                    'timestamp': datetime.fromtimestamp(req.timestamp_start).isoformat() if req.timestamp_start else '',
                })
    except ImportError:
        flows = [{'error': 'mitmproxy not installed — pip install mitmproxy'}]
    except Exception as e:
        flows = [{'error': str(e)}]
    return flows

def get_flow_detail(session_id: str, flow_id: int) -> dict:
    """Return full request+response detail for a specific flow."""
    flow_file = FLOWS_DIR / f'{session_id}.flow'
    if not flow_file.exists():
        return {}
    try:
        from mitmproxy.io import FlowReader
        with open(flow_file, 'rb') as f:
            reader = FlowReader(f)
            for i, flow in enumerate(reader.stream()):
                if i == flow_id:
                    req = flow.request
                    resp = flow.response
                    return {
                        'request': {
                            'method': req.method,
                            'url': req.pretty_url,
                            'headers': dict(req.headers),
                            'body': req.content.decode('utf-8', errors='replace')[:4096],
                        },
                        'response': {
                            'status': resp.status_code if resp else None,
                            'headers': dict(resp.headers) if resp else {},
                            'body': (resp.content.decode('utf-8', errors='replace')[:4096]) if resp else '',
                        } if resp else None,
                    }
    except Exception as e:
        return {'error': str(e)}
    return {}

def replay_flow(session_id: str, flow_id: int, modifications: dict = None) -> dict:
    """Re-send a captured request, optionally with modifications."""
    detail = get_flow_detail(session_id, flow_id)
    if 'error' in detail or not detail:
        return {'ok': False, 'error': detail.get('error', 'Flow not found')}
    import urllib.request
    req_data = detail['request']
    url = req_data['url']
    headers = req_data['headers']
    body = req_data['body']
    if modifications:
        if 'body' in modifications: body = modifications['body']
        if 'headers' in modifications: headers.update(modifications['headers'])
        if 'url' in modifications: url = modifications['url']
    try:
        data = body.encode() if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=req_data['method'])
        with urllib.request.urlopen(req, timeout=15) as r:
            resp_body = r.read().decode('utf-8', errors='replace')[:4096]
            return {
                'ok': True,
                'status': r.status,
                'headers': dict(r.headers),
                'body': resp_body,
            }
    except Exception as e:
        return {'ok': False, 'error': str(e)}

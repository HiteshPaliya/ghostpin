"""
GhostPin v5 Phase 2 — Feature: Web UI Authentication
Simple PIN/token auth with Flask sessions. Configurable via settings.
"""
import os, hashlib, secrets
from pathlib import Path
from functools import wraps
from flask import session, request, jsonify, redirect

DATA_DIR = Path.home() / '.ghostpin'
AUTH_FILE = DATA_DIR / 'auth.json'

def _load_auth():
    import json
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text())
        except Exception:
            pass
    return {'enabled': False, 'pin_hash': '', 'token': ''}

def _save_auth(data):
    import json
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    AUTH_FILE.write_text(json.dumps(data, indent=2))

def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def is_auth_enabled() -> bool:
    return _load_auth().get('enabled', False)

def check_pin(pin: str) -> bool:
    data = _load_auth()
    return data.get('pin_hash', '') == hash_pin(pin)

def check_token(token: str) -> bool:
    data = _load_auth()
    return data.get('token', '') == token and token != ''

def enable_auth(pin: str) -> str:
    """Enable PIN auth, returns generated API token."""
    token = secrets.token_hex(24)
    _save_auth({'enabled': True, 'pin_hash': hash_pin(pin), 'token': token})
    return token

def disable_auth():
    _save_auth({'enabled': False, 'pin_hash': '', 'token': ''})

def get_token() -> str:
    return _load_auth().get('token', '')

def login_required(f):
    """Flask decorator — skip auth if disabled or already logged in."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_auth_enabled():
            return f(*args, **kwargs)
        # Check session
        if session.get('authenticated'):
            return f(*args, **kwargs)
        # Check Bearer token (for API/CLI usage)
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if check_token(token):
                return f(*args, **kwargs)
        # Check X-GhostPin-Token header
        token = request.headers.get('X-GhostPin-Token', '')
        if token and check_token(token):
            return f(*args, **kwargs)
        # For API routes return 401
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Unauthorized', 'login': '/login'}), 401
        # For UI redirect to login
        return redirect('/login')
    return decorated

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GhostPin — Login</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=JetBrains+Mono&display=swap');
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0a0c14;color:#d8e0f4;font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
  .card{background:#111520;border:1px solid #1d2333;border-radius:16px;padding:48px 40px;width:380px;text-align:center}
  .logo{font-size:48px;margin-bottom:20px}
  h1{font-size:22px;font-weight:800;color:#b8ff47;margin-bottom:6px}
  .sub{font-size:12px;color:#4a5278;margin-bottom:32px}
  input{width:100%;background:#0d1018;border:1px solid #1d2333;border-radius:8px;padding:14px 16px;color:#d8e0f4;font-size:18px;font-family:'JetBrains Mono',monospace;letter-spacing:6px;text-align:center;outline:none;transition:border .2s;margin-bottom:16px}
  input:focus{border-color:#b8ff47}
  button{width:100%;background:#b8ff47;color:#0a0c14;border:none;border-radius:8px;padding:14px;font-size:14px;font-weight:800;cursor:pointer;transition:opacity .15s}
  button:hover{opacity:.85}
  .err{color:#ff4d6a;font-size:12px;margin-top:10px;display:none}
  .token-row{margin-top:24px;padding-top:20px;border-top:1px solid #1d2333;font-size:11px;color:#4a5278}
  .token-row a{color:#3de8ff;cursor:pointer;text-decoration:underline}
</style>
</head>
<body>
<div class="card">
  <div class="logo">🔐</div>
  <h1>GhostPin</h1>
  <div class="sub">v5.0 — Enter your PIN to continue</div>
  <form onsubmit="doLogin(event)">
    <input type="password" id="pin" placeholder="• • • • • •" maxlength="12" autofocus>
    <button type="submit">Unlock</button>
    <div class="err" id="err">Incorrect PIN</div>
  </form>
  <div class="token-row">Using CLI or API? <a onclick="showToken()">Use token auth</a></div>
  <div id="token-form" style="display:none;margin-top:12px">
    <input type="text" id="token-input" placeholder="Paste API token" style="letter-spacing:1px;font-size:12px">
    <button onclick="doTokenLogin()" style="margin-top:0">Submit Token</button>
  </div>
</div>
<script>
async function doLogin(e) {
  e.preventDefault();
  var pin = document.getElementById('pin').value;
  var r = await fetch('/api/auth/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pin})});
  var d = await r.json();
  if (d.ok) location.href = '/';
  else { document.getElementById('err').style.display='block'; document.getElementById('pin').value=''; }
}
async function doTokenLogin() {
  var token = document.getElementById('token-input').value.trim();
  var r = await fetch('/api/auth/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token})});
  var d = await r.json();
  if (d.ok) location.href = '/';
  else document.getElementById('err').style.display='block';
}
function showToken() { document.getElementById('token-form').style.display='block'; }
</script>
</body>
</html>"""

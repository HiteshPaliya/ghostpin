"""
GhostPin Enterprise v5 - Auto-Patcher
Automatically patch APKs and IPAs with apk-mitm for non-rooted network bypass and Frida gadget injection.
"""
import subprocess
from pathlib import Path
import os
import shutil

def patch_app(app_path: Path, output_dir: Path) -> dict:
    """Run apk-mitm to unpack, modify NSC, inject Frida, and repack the app."""
    if not shutil.which('npx'):
        return {'ok': False, 'error': 'Node.js / npx not found. Required for apk-mitm.'}
        
    # The output from apk-mitm is usually named `<original>-patched.apk` in the current working directory
    out_name = f"{app_path.stem}-patched{app_path.suffix}"
    out_target = output_dir / out_name
    
    cmd = [
        'npx', '-y', 'apk-mitm', str(app_path)
    ]
    
    try:
        # Run inside the output_dir so the patched file drops there
        proc = subprocess.run(cmd, cwd=str(output_dir), capture_output=True, text=True, timeout=120)
        
        if out_target.exists():
            return {
                'ok': True,
                'path': str(out_target),
                'log': proc.stdout + '\n' + proc.stderr
            }
        else:
            return {
                'ok': False,
                'error': f"Failed to patch app. apk-mitm output: {proc.stdout}\n{proc.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': 'apk-mitm timed out after 2 minutes.'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

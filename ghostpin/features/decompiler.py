"""
GhostPin v5 - Decompiler Engine
Integrates JADX to decompile Android APKs natively for in-UI source code viewing.
"""
import os
import subprocess
import shutil
from pathlib import Path
from ghostpin.core.errors import DecompileError

def get_jadx_path() -> str | None:
    """Locate jadx in system PATH or common installation directories."""
    jadx_cmd = shutil.which('jadx')
    if jadx_cmd:
        return jadx_cmd

    candidates = [
        Path.home() / 'jadx' / 'bin' / 'jadx',
        Path.home() / 'jadx' / 'build' / 'jadx' / 'bin' / 'jadx',
        Path('/usr/local/bin/jadx'),
        Path('/opt/jadx/bin/jadx'),
    ]
    if os.name == 'nt':
        candidates.extend([
            Path(os.environ.get('LOCALAPPDATA', '')) / 'jadx' / 'bin' / 'jadx.bat',
            Path.home() / 'jadx' / 'bin' / 'jadx.bat',
        ])

    for p in candidates:
        if p.is_file():
            return str(p)
    return None


def decompile_apk(apk_path: str, output_dir: str) -> dict:
    """Run JADX to decompile an APK/IPA to Java source files."""
    jadx_bin = get_jadx_path()
    if not jadx_bin:
        return {'ok': False, 'error': 'JADX not found. Install it from https://github.com/skylot/jadx/releases'}

    cmd = [
        jadx_bin,
        '-d', output_dir,
        '--no-res',          # Skip resources — we only want source code
        '--show-bad-code',   # Show partially decompiled code too
        str(apk_path),
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        sources_dir = Path(output_dir) / 'sources'
        if sources_dir.exists():
            return {'ok': True, 'log': proc.stdout[:2000]}
        return {'ok': False, 'error': f'JADX produced no sources. {proc.stderr[:500]}'}
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': 'Decompilation timed out (5 min limit).'}
    except Exception as e:
        return {'ok': False, 'error': f'Unexpected error: {e}'}


def read_source_file(output_dir: str, file_path: str) -> dict:
    """
    Read a specific decompiled Java/XML file.
    Rigorously prevents path traversal outside the JADX workspace.
    file_path should be relative, e.g. 'com/example/app/MainActivity.java'
    """
    base = (Path(output_dir) / 'sources').resolve()

    # Resolve the target — this collapses any '..' sequences
    safe_path = (base / file_path).resolve()

    # SECURITY: Use is_relative_to() instead of string prefix comparison.
    # str.startswith() is vulnerable to partial-path attacks like
    # '/tmp/gp_abc/../secret' — Path.is_relative_to() is strictly correct.
    try:
        safe_path.relative_to(base)  # raises ValueError if outside base
    except ValueError:
        return {'ok': False, 'error': 'Access denied: path traversal attempt detected.'}

    if not safe_path.exists():
        return {'ok': False, 'error': f'Source file not found: {file_path}'}

    try:
        content = safe_path.read_text(encoding='utf-8', errors='replace')
        return {'ok': True, 'content': content}
    except OSError as e:
        return {'ok': False, 'error': f'Cannot read file: {e}'}

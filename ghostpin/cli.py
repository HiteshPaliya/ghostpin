#!/usr/bin/env python3
"""
GhostPin v5.0 — CLI Entry Point
Click-based CLI: ghostpin start|check|install-frida|version
"""
import os, sys, subprocess
import click

BOLD  = '\033[1m'
LIME  = '\033[38;5;154m'
CYAN  = '\033[38;5;87m'
RED   = '\033[38;5;196m'
AMBER = '\033[38;5;214m'
MINT  = '\033[38;5;84m'
DIM   = '\033[2m'
RESET = '\033[0m'

BANNER = f"""
{LIME}{BOLD}   ___ _  _ ___  ___ _____ ___ ___ _  _ 
  / __| || / _ \/ __|_   _| _ \_ _| \| |
 | (_ | __ | (_) \__ \ | | |  _/| || .` |
  \___|_||_\___/|___/ |_| |_| |___|_|\_|
{RESET}{BOLD}  Enterprise SSL Pinning Bypass & Security Research Platform  {DIM}v5.0.0 Phantom{RESET}
  {DIM}Android + iOS | Frida | ADB | 10 Security Pillars | Educational Mode{RESET}
"""

def banner():
    # Force utf-8 encoding for safe output if needed, or stick to basic chars
    try:
        click.echo(BANNER)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(BANNER.encode('utf-8'))
        sys.stdout.flush()

def check_pip_dep(pkg):
    try:
        __import__(pkg)
        click.echo(f'  {MINT}[OK] {pkg}{RESET}')
        return True
    except ImportError:
        click.echo(f'  {AMBER}[..] {pkg} - installing...{RESET}')
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg, '--quiet'], check=False)
        return False

def check_tool(name):
    import shutil
    found = shutil.which(name) is not None
    status = f'{MINT}[OK]{RESET}' if found else f'{DIM}[--]{RESET}'
    click.echo(f'  {status} {name}')
    return found

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """GhostPin — Mobile Security Testing Platform"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(start)

@cli.command()
@click.option('--port', default=7331, envvar='GHOSTPIN_PORT', show_default=True, help='Web server port')
@click.option('--host', default='0.0.0.0', show_default=True, help='Bind address')
@click.option('--no-browser', is_flag=True, help='Skip auto-opening browser')
@click.option('--debug', is_flag=True, hidden=True)
def start(port, host, no_browser, debug):
    """Start GhostPin web server"""
    banner()
    click.echo(f'{LIME}{BOLD}* Starting GhostPin v5.0{RESET}\n')

    # Ensure Flask is installed
    check_pip_dep('flask')

    click.echo(f'\n{BOLD}  Server:   {CYAN}http://localhost:{port}{RESET}')
    click.echo(f'{BOLD}  Data Dir: {DIM}~/.ghostpin{RESET}')
    click.echo(f'\n  {DIM}Press Ctrl+C to stop{RESET}\n')

    if not no_browser:
        import threading, time, webbrowser
        def _open():
            time.sleep(1.8)
            webbrowser.open(f'http://localhost:{port}')
        threading.Thread(target=_open, daemon=True).start()

    # Import and run the app
    try:
        import sys, os
        # Support running from source dir or installed
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        from ghostpin.server import create_app
        app = create_app()
        click.echo(f'  {DIM}GhostPin listening on http://{host}:{port}{RESET}\n')
        app.run(host=host, port=port, debug=debug, threaded=True)
    except ImportError:
        # Fallback: try running server.py directly from same dir
        import subprocess
        server_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'server.py')
        subprocess.run([sys.executable, server_path])

@cli.command()
def check():
    """Check required toolchain dependencies"""
    banner()
    click.echo(f'{BOLD}{CYAN}* Dependency Check{RESET}\n')

    click.echo(f'{DIM}Python packages:{RESET}')
    check_pip_dep('flask')
    check_pip_dep('click')

    click.echo(f'\n{DIM}Required tools:{RESET}')
    check_tool('adb')
    check_tool('frida')
    check_tool('frida-ps')
    check_tool('objection')

    click.echo(f'\n{DIM}Optional tools:{RESET}')
    for t in ['apktool', 'jadx', 'mitmproxy', 'openssl', 'ideviceinfo', 'apk-mitm']:
        check_tool(t)

@cli.command('install-frida')
def install_frida():
    """Install Frida toolkit (frida-tools, objection, apk-mitm)"""
    banner()
    click.echo(f'{BOLD}{CYAN}* Installing Frida Toolchain{RESET}\n')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'frida-tools', 'objection', 'apk-mitm', '--upgrade'])
    click.echo(f'\n{MINT}[OK] Frida toolchain installed{RESET}')

@cli.command()
def version():
    """Show GhostPin version"""
    from ghostpin import __version__, __codename__
    click.echo(f'GhostPin v{__version__} ({__codename__})')

if __name__ == '__main__':
    cli()

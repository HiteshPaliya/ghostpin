#!/usr/bin/env bash
# ╔═══════════════════════════════════════════════════════════╗
# ║          GhostPin Enterprise — Setup & Launcher           ║
# ║   SSL Pinning Bypass Platform · Enterprise Edition v4.0   ║
# ╚═══════════════════════════════════════════════════════════╝

set -e
BOLD='\033[1m'
LIME='\033[38;5;154m'
CYAN='\033[38;5;87m'
RED='\033[38;5;196m'
AMBER='\033[38;5;214m'
MINT='\033[38;5;84m'
RESET='\033[0m'
DIM='\033[2m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${GHOSTPIN_PORT:-7331}"

banner() {
  echo ""
  echo -e "${LIME}${BOLD}"
  echo "  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██╗███╗   ██╗"
  echo "  ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║"
  echo "  ██║  ███╗███████║██║   ██║███████╗   ██║   ██████╔╝██║██╔██╗ ██║"
  echo "  ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██╔═══╝ ██║██║╚██╗██║"
  echo "  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██║     ██║██║ ╚████║"
  echo "   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝"
  echo ""
  echo -e "${RESET}${BOLD}  Enterprise SSL Pinning Bypass Platform  ${DIM}v4.0.0${RESET}"
  echo -e "  ${DIM}Android + iOS · Frida · ADB · APK Analysis · mTLS${RESET}"
  echo ""
}

check_python() {
  if ! command -v python3 &>/dev/null; then
    echo -e "${RED}✗ Python 3 not found. Install from https://python.org${RESET}"
    exit 1
  fi
  PYVER=$(python3 --version 2>&1 | awk '{print $2}')
  echo -e "${MINT}✓ Python ${PYVER}${RESET}"
}

check_pip_dep() {
  local pkg="$1"
  python3 -c "import ${pkg}" 2>/dev/null && echo -e "${MINT}✓ ${pkg}${RESET}" || {
    echo -e "${AMBER}  Installing ${pkg}...${RESET}"
    pip3 install "${pkg}" --quiet --break-system-packages 2>/dev/null || \
    pip3 install "${pkg}" --quiet 2>/dev/null || \
    pip install "${pkg}" --quiet 2>/dev/null || true
  }
}

check_tool() {
  local tool="$1"
  if command -v "${tool}" &>/dev/null; then
    echo -e "${MINT}✓ ${tool}${RESET}"
  else
    echo -e "${DIM}  ✗ ${tool} — not found (optional)${RESET}"
  fi
}

cmd_check() {
  echo -e "\n${BOLD}${CYAN}◆ Checking Dependencies${RESET}\n"
  check_python

  echo ""
  echo -e "${DIM}Python packages:${RESET}"
  check_pip_dep flask

  echo ""
  echo -e "${DIM}Required tools:${RESET}"
  check_tool adb
  check_tool frida
  check_tool frida-ps
  check_tool objection

  echo ""
  echo -e "${DIM}Optional tools:${RESET}"
  check_tool apktool
  check_tool jadx
  check_tool mitmproxy
  check_tool openssl
  check_tool ideviceinfo
  check_tool apk-mitm
}

cmd_start() {
  banner
  echo -e "${LIME}${BOLD}◆ Starting GhostPin Enterprise${RESET}"
  echo ""

  check_python
  python3 -c "import flask" 2>/dev/null || {
    echo -e "${AMBER}  Flask not found — installing...${RESET}"
    pip3 install flask --quiet --break-system-packages 2>/dev/null || pip3 install flask --quiet
  }

  echo ""
  echo -e "${BOLD}  Server:   ${CYAN}http://localhost:${PORT}${RESET}"
  echo -e "${BOLD}  Data Dir: ${DIM}~/.ghostpin${RESET}"
  echo ""
  echo -e "  ${DIM}Press Ctrl+C to stop${RESET}"
  echo ""

  # Auto-open browser
  case "$(uname -s)" in
    Darwin) (sleep 1.5 && open "http://localhost:${PORT}") & ;;
    Linux)  (sleep 1.5 && xdg-open "http://localhost:${PORT}" 2>/dev/null || true) & ;;
  esac

  cd "${SCRIPT_DIR}"
  FLASK_ENV=production python3 -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from server import app
print('  GhostPin listening on http://0.0.0.0:${PORT}')
app.run(host='0.0.0.0', port=${PORT}, debug=False, threaded=True)
"
}

cmd_install_frida_tools() {
  echo -e "\n${BOLD}${CYAN}◆ Installing Frida Toolchain${RESET}\n"
  pip3 install frida-tools objection apk-mitm --upgrade
  echo -e "${MINT}✓ Frida toolchain installed${RESET}"
}

cmd_help() {
  banner
  echo -e "${BOLD}Usage:${RESET} ./ghostpin.sh [command]\n"
  echo -e "  ${LIME}start${RESET}         Start GhostPin Enterprise server"
  echo -e "  ${LIME}check${RESET}         Check dependencies"
  echo -e "  ${LIME}install-frida${RESET} Install Frida + Objection + apk-mitm"
  echo -e "  ${LIME}help${RESET}          Show this help"
  echo ""
  echo -e "${BOLD}Environment:${RESET}"
  echo -e "  ${DIM}GHOSTPIN_PORT${RESET}  Web server port (default: 7331)"
  echo ""
  echo -e "${BOLD}Quick Start:${RESET}"
  echo -e "  ${DIM}./ghostpin.sh start${RESET}   → Open http://localhost:7331"
  echo ""
}

case "${1:-start}" in
  start)          cmd_start ;;
  check)          cmd_check ;;
  install-frida)  cmd_install_frida_tools ;;
  help|--help|-h) cmd_help ;;
  *)              echo -e "${RED}Unknown command: $1${RESET}"; cmd_help; exit 1 ;;
esac

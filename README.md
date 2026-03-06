# 🔐 GhostPin Enterprise v5.0 — *Phantom*

> **The most complete mobile SSL pinning bypass and security research platform available.**
> Android + iOS · Frida-powered · 17 bypass scripts · 10 security research pillars · Stealth Evasion Core · Coverage-Guided Fuzzing · CLI + Web UI

[![Version](https://img.shields.io/badge/version-5.0.0--Phantom-lime?style=flat-square)](.)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20iOS-blue?style=flat-square)](.)
[![License](https://img.shields.io/badge/license-Enterprise-red?style=flat-square)](.)

---

## ⚡ What Is GhostPin?

GhostPin is an enterprise-grade mobile application security testing platform. It eliminates the #1 barrier to intercepting mobile traffic — **SSL/TLS certificate pinning** — while providing a suite of complementary research tools that stay useful across every stage of a mobile pentest: from reconnaisance to final report.

Whether you're assessing a **banking app** with custom pinning, a **Unity game** with EasyAntiCheat, a **React Native fintech app** on Hermes, or an **MDM-managed enterprise app**, GhostPin has purpose-built tools for every scenario.

---

## 🚀 Quick Start

GhostPin requires zero manual configuration out of the box. A single install script handles the entire ecosystem.

```bash
# 1. Install from source (downloads Flask, click, frida, objection, mitmproxy)
cd ghostpin/
pip install -e .

# 2. Check dependencies
ghostpin check

# 3. Launch the UI
ghostpin start
```

> **Testing on a non-rooted device?** GhostPin features a built-in **1-Click Auto-Patcher**. Open the Analyzer tab, upload your IPA or APK, and GhostPin will automatically inject the Frida gadget and defeat Network Security Configs for you via `apk-mitm`.

> **Need the APK off your physical device?** Don't drop to the CLI to run `adb pull`. Use the **1-Click Device APK Extractor** on the Analyzer page to instantly rip the original APK off of your connected phone directly into your web browser. *(Note: If the app is a modern Android App Bundle, GhostPin will automatically download all the Split APKs and package them into a single `.zip` for you).*

> **Air-gapped network?** The web UI automatically detects if you are offline and swaps the cloud-hosted Monaco editor out for a local, dependencies-free fallback engine so your pentest is never interrupted.

---

## 🛡️ Security Research Pillars (10)

### 1 — 🔗 Deep Link & Intent Fuzzer
**Automated discovery of input-handling vulnerabilities in Android components**

Banking apps, OAuth flows, and enterprise apps all use deep links (`myapp://pay?token=...`) and exported Android Activities. This pillar:
- Enumerates **every exported Activity, Service, and Broadcast Receiver** in the target APK via `adb shell pm dump`
- Fires **crafted Intents** with SQL injection, path traversal, overflow, XSS, and URI scheme payloads as extras and data URIs
- Highlights **interesting responses**: crashes, exceptions, or unexpected data

**Why this matters:** A misconfigured exported Activity can allow any app on the device to launch it with attacker-controlled data — leading to account takeover, CSRF, or data theft.  
→ *See [SECURITY_GUIDE.md](SECURITY_GUIDE.md#intent-fuzzer) for full tutorial.*

---

### 2 — 🔬 Runtime API Monitor & Auto-Discovery
**Live interception of crypto, files, network + Automated API Map generation**

Frida hooks are injected into the app's runtime to record:
| Category | What's hooked |
|----------|--------------|
| 🔐 Crypto | `Cipher`, `MessageDigest`, `KeyStore`, `Mac`, iOS `CCCrypt`, `CryptoKit` |
| 📁 File | `FileInputStream`, `FileOutputStream`, `SharedPreferences`, `SQLiteDatabase`, iOS `NSFileManager` |
| 🌐 Network | OkHttp3, `URL.openConnection`, `Socket`, `InetAddress` (DNS), `NSURLSession`, Retrofit |

**✨ Phase 4 Flagship:** As the monitor observes traffic and the mitmproxy hook intercepts flows (including WebSockets and GraphQL mutations), GhostPin automatically builds an **API Discovery Map**. It groups all backend URLs, extracting paths and query parameters, and allows you to 1-click export the entire map to a **Postman Collection** or Burp Suite project.

**Why this matters:** Seeing *which* encryption algorithm an app uses is essential. Even better is having GhostPin automatically map the attack surface so you can pivot to web assessment instantly.  
→ *See [SECURITY_GUIDE.md](SECURITY_GUIDE.md#api-monitor) for full tutorial.*

---

### 3 — 🔍 Vulnerability Scanner (SAST) & AI Pentester
**Automated static analysis of APKs for 30+ vulnerability patterns + GenAI explanations**

Scans every DEX file, XML, `.ipa` Plist, and asset for:
- **Secret leakage**: Google API keys, AWS keys, Stripe live keys, private keys, OAuth secrets
- **Weak cryptography**: MD5, SHA-1, DES, ECB mode, insecure `Random()`, RC4
- **Android misconfigs**: `debuggable=true`, `allowBackup=true`, cleartext traffic
- **iOS misconfigs**: Custom URL Schemes (`CFBundleURLTypes`), insecure App Transport Security (`NSAllowsArbitraryLoads`)

**✨ Phase 4 Flagship:** Findings from the SAST scanner can be sent to the built-in **AI Pentester** (powered by Gemini/LLMs). The AI explains exactly *why* the finding is vulnerable, the potential business impact, and writes the specific Java, Kotlin, or Swift remediation code needed to fix it.

**✨ Phase 7 Apex:** Total iOS Parity. Uploading an `.ipa` triggers a native Mach-O / `Info.plist` analysis engine that automatically unpacks Apple archives, parsing URL schemes and ATS config vulnerabilities without requiring macOS `otool`.

**Why this matters:** Hard-coded secrets are one of the most common and most impactful mobile findings. GhostPin doesn't just find them; it explains how to exploit them and how to fix them.  
→ *See [SECURITY_GUIDE.md](SECURITY_GUIDE.md#vuln-scanner) for full tutorial.*

---

### 4 — ⚛️ React Native / Hermes Bypass
**Purpose-built hooks for the Hermes JS engine and React Native framework**

Standard OkHttp3 bypass is not enough for RN apps with Hermes. This script:
- Hooks Java-side `OkHttp3.CertificatePinner` (same path)
- Disables `DevSupportManager` and `FlipperClient` debug detection
- Hooks Hermes native SSL exports in `libhermes.so`
- Hooks `libcurl.so` `CURLOPT_SSL_VERIFYPEER` for JSI fetch()

**Why this matters:** React Native is the dominant framework for fintech apps (Revolut, Klarna, etc.). Standard bypass methods often fail silently on Hermes.

---

### 5 — 🏢 MDM & EMM Profiler
**Detect and analyze Mobile Device Management software**

Identifies: **Microsoft Intune, MobileIron/Ivanti, Jamf, VMware Workspace ONE/AirWatch, Samsung Knox, BlackBerry UEM, IBM MaaS360**, and more (15+ vendors).

Analyzes: device admin receivers, work profile status, policy restrictions, Knox version.

Injects Frida hooks for `DevicePolicyManager` to log policy queries at runtime.

**Why this matters:** Enterprise app tests almost always involve MDM. MDM can silently block Frida injection, disable USB debugging, and enforce VPNs. Knowing the MDM vendor and its capabilities is the first step to working around it.  
→ *See [SECURITY_GUIDE.md](SECURITY_GUIDE.md#mdm-profiler) for full tutorial.*

---

### 6 — 🛡️ Binary Fortress (Anti-Tamper / Anti-Debug)
**Defeat integrity checking mechanisms**

| Sub-feature | What it bypasses |
|---|---|
| SafetyNet bypass | `SafetyNetClient.attest()`, JWS payload patching |
| Play Integrity bypass | `IntegrityManager.requestIntegrityToken()` |
| ptrace / anti-debug | `/proc/self/status` TracerPid intercept, native `open()` hook |
| Emulator spoofing | `Build.FINGERPRINT`, `MANUFACTURER`, `MODEL` → Pixel 2 release build |

**Why this matters:** Nearly every fintech and banking app uses SafetyNet or Play Integrity to block testing on rooted/unlocked devices. Without bypassing these, the bypass session cannot even start.

---

### 7 — 🔭 Class Dump & Method Tracer
**Runtime reverse engineering without static analysis**

Two modes:
- **Class Dump**: `Java.enumerateLoadedClasses` with filter keyword → lists all matching loaded classes
- **Method Tracer**: hooks every method on a specified class, logging argument values and return values in real-time

Also supports **iOS ObjC** class dumping and method interception.

**Why this matters:** When you don't have source code and static analysis is blocked by obfuscation, live class dumping reveals the real class names and method signatures at runtime.  
→ *See [SECURITY_GUIDE.md](SECURITY_GUIDE.md#class-tracer) for full tutorial.*

---

### 8 — 📖 Native Source Code Decompiler (JADX)
**Read raw Java source code straight from the browser**

**✨ Phase 7 Apex:** A built-in source code browser powered by JADX. Upload an APK to instantly decompile the Dalvik bytecode back to Java. Navigate the package structure and read the raw source code of any file right in the browser, eliminating the need to have a heavy Java IDE open while pentesting.

**Why this matters:** When the AI Pentester flags a vulnerable line of code, you need to read the surrounding context to confirm exploitability. GhostPin's native decompiler lets you pivot straight to the code.

---

### 9 — 🎮 Gaming & Anti-Cheat Profiler
**SSL bypass for Unity IL2CPP games with anti-cheat detection**

- Unity IL2CPP: enumerates all SSL-related exports in `libil2cpp.so` + BoringSSL pattern scan
- Mono runtime: patches `System.Net.ServicePointManager.ServerCertificateValidationCallback`
- **EasyAntiCheat** (`libeac.so`): hides Frida from `/proc/self/maps` reads
- **BattlEye** (`libBEService.so`): hooks `Initialize`/`Check` exports
- `il2cpp_resolve_icall` tracing for deep SSL inspection

**Why this matters:** Mobile games are increasingly using anti-cheat technology that also performs integrity checks. Assessing game server APIs requires bypassing these protections.

---

### 9 — 📊 Smart Report Generator
**Auto-generate professional HTML pentest reports**

Combines session logs, SAST findings, MDM profile, and API monitor output into a professionally styled HTML report with:
- Executive summary with severity stats
- Security grade (A–F)
- Full findings table with evidence
- Print-friendly layout (works offline)

**Why this matters:** Every engagement needs a deliverable. GhostPin generates a client-ready report in one click.

---

### 10 — 🚦 Traffic Intercept & Replay *(Integration)*
**mitmproxy integration for request capture and replay**

Launches mitmproxy as a subprocess and surfaces captured HTTP flows directly in GhostPin. Combine with SSL bypass to capture, modify, and replay API requests without leaving the tool.

---

## 📦 Existing SSL Bypass Scripts (17 total)

| Script | Target | Difficulty |
|--------|--------|-----------|
| Universal Android Bypass | OkHttp3, TrustManager, SSLContext, NSC, WebView | Easy |
| Obfuscation Resilient | ProGuard/R8/DexGuard protected apps | Medium |
| Root Detection Bypass | RootBeer, Magisk, KSU, exec() checks | Easy |
| Frida Evasion | /proc/maps filtering, port hiding | Medium |
| iOS Universal | SecTrustEvaluate, NSURLSession, AFNetworking | Easy |
| iOS Jailbreak Bypass | NSFileManager, canOpenURL, Cydia/Sileo | Medium |
| Flutter Android | libflutter.so BoringSSL pattern scan | Hard |
| Flutter iOS | Flutter.framework pattern scan | Hard |
| Native OpenSSL/BoringSSL | SSL_CTX_set_verify, X509_verify_cert | Hard |
| gRPC / Netty | NettyChannelBuilder, grpc transport | Hard |
| Xamarin / MAUI | Mono ServicePointManager, HttpClientHandler | Medium |
| Certificate Transparency | CTVerifier, NSC CT enforcement | Hard |
| Unity / IL2CPP | Mono + IL2CPP export enum + pattern scan | Expert |
| QUIC/HTTP3 Blocker | CronetEngine, iptables QUIC block | Medium |
| **SafetyNet + Play Integrity** | Attest JWS patch, integrity token spoof | Expert |
| **React Native / Hermes** | Hermes SSL, libcurl, DevSupport | Hard |
| **Gaming Anti-Cheat** | EasyAntiCheat, BattlEye, IL2CPP | Expert |

---

## 🏗️ Architecture

```text
ghostpin/
├── ghostpin/               ← Python Package
│   ├── __init__.py         (v5.0.0 Phantom)
│   ├── __main__.py         (Module entry point)
│   ├── cli.py              (Click CLI — `ghostpin start|check|version`)
│   ├── server.py           (Flask app factory + gzip compression + 70+ API routes)
│   ├── core/
│   │   ├── adb.py          (ADB & Frida host helpers)
│   │   └── errors.py       (Typed exception hierarchy — DeviceError, FridaError, etc.)
│   ├── features/           ← Security Pillars & Support Modules
│   │   ├── ai_analyzer.py      (Gemini/LLM-powered vuln explanations & remediation)
│   │   ├── api_mapper.py       (Automatic API endpoint discovery & Postman/Burp export)
│   │   ├── api_monitor.py      (Crypto/file/network runtime monitor)
│   │   ├── auth.py             (PIN & token-based auth)
│   │   ├── auto_patcher.py     (1-Click APK patcher via apk-mitm)
│   │   ├── class_tracer.py     (Class dump & method tracer — runtime obfuscation defeat)
│   │   ├── coverage_fuzzer.py  (Apex: AFL++-style coverage-guided Intent fuzzer)
│   │   ├── cve_checker.py      (OSV.dev vulnerability lookup for SDK deps)
│   │   ├── decompiler.py       (Apex: JADX integration — Java source in browser)
│   │   ├── diff_analyzer.py    (APK permission & native lib diffing between versions)
│   │   ├── frida_downloader.py (Auto device provisioning — ABI-aware frida-server download)
│   │   ├── guided_checklist.py (App-type driven assessment wizards)
│   │   ├── intent_fuzzer.py    (Android deep link & IPC fuzzing)
│   │   ├── ios_analyzer.py     (Apex: native IPA/Info.plist analyzer — no macOS needed)
│   │   ├── mdm_profiler.py     (15+ MDM vendor detection & DevicePolicyManager hooks)
│   │   ├── mitm_addon.py       (mitmproxy addon for traffic capture)
│   │   ├── reporter.py         (HTML pentest report generator)
│   │   ├── sarif_export.py     (CI/CD SARIF output)
│   │   ├── stealth_mgr.py      (Apex: hluda-server stealth evasion deployment)
│   │   ├── tls_manager.py      (Self-signed cert generation & CA management)
│   │   ├── traffic_replay.py   (mitmproxy subprocess integration)
│   │   ├── vuln_scanner.py     (SAST — 30+ pre-compiled regex patterns, thread-safe)
│   │   └── workspace.py        (Per-target project configs)
│   └── scripts/
│       ├── bypass/         (17 Core Frida JS Scripts)
│       └── fuzzer/
│           └── stalker_coverage.js  (Apex: Frida Stalker basic block tracer)
├── .gitignore
├── ghostpin.sh             ← Shell launcher
├── requirements.txt
├── setup.py                ← pip install build script
├── GHOSTPIN_DOCUMENTATION.md ← Complete technical guide (8 sections)
├── SECURITY_GUIDE.md       ← Educational companion for beginners
└── README.md               ← This file
```

---

## ⚙️ Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | **3.9+** | Required for `Path.relative_to()` and `str \| None` type hints |
| Flask | 2.0+ | `pip install flask` |
| Click | 8.0+ | `pip install click` |
| frida-tools | latest | `pip install frida-tools` — **must match frida-server version on device** |
| objection | latest | `pip install objection` |
| adb | any | Android SDK Platform Tools |
| frida-server | matching frida-tools | Auto-installed via GhostPin UI |
| mitmproxy | 10.0+ | Optional: Traffic Replay — `pip install mitmproxy` |
| JADX | latest | Optional: Source Decompiler — [GitHub Releases](https://github.com/skylot/jadx/releases) |
| apk-mitm | latest | Optional: 1-Click Auto-Patcher — `npm install -g apk-mitm` |

---

## 🔐 Legal Notice

GhostPin Enterprise is provided for **authorized security testing only**.
Unauthorized use against applications or devices you do not own or have explicit written permission to test is illegal under the Computer Fraud and Abuse Act (CFAA), Computer Misuse Act (CMA), and equivalent laws worldwide.

The authors accept no liability for misuse.

---

## 📖 Documentation

| Document | Audience | Contents |
|---|---|---|
| **[GHOSTPIN_DOCUMENTATION.md](GHOSTPIN_DOCUMENTATION.md)** | Junior & Senior Pentesters | Complete 8-section technical guide: quick start, core concepts, all feature walkthroughs with main/edge cases, 9-phase methodology, 14-issue troubleshooting guide, MASVS mapping, glossary |
| **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** | Beginners to mobile security | Vulnerability-by-vulnerability explanations, real-world breach examples, manual verification commands, business impact & developer remediation |

> **New to mobile security?** Start with `SECURITY_GUIDE.md` — it explains the *why* behind every test.
> **Experienced pentester?** Go straight to `GHOSTPIN_DOCUMENTATION.md` Section 5 (Feature Walkthroughs).

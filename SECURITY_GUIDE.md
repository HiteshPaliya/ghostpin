# 📚 GhostPin Enterprise — Security Guide
### *For people who are just starting to learn mobile application security*

> This guide explains every GhostPin feature from first principles: what the vulnerability is, why it matters, how to test for it, how to confirm findings manually, and what happens to an organization if the vulnerability is real.

---

<a name="toc"></a>
## Table of Contents
1. [SSL Pinning — The Foundation](#ssl-pinning)
2. [Intent Fuzzer](#intent-fuzzer)
3. [Runtime API Monitor](#api-monitor)
4. [Vulnerability Scanner (SAST)](#vuln-scanner)
5. [MDM Profiler](#mdm-profiler)
6. [Binary Fortress (SafetyNet / Play Integrity)](#binary-fortress)
7. [Class Dump & Method Tracer](#class-tracer)
8. [React Native / Hermes Bypass](#react-native)
9. [Gaming & Anti-Cheat Profiler](#gaming)
10. [Smart Report Generator](#reporter)

---

<a name="ssl-pinning"></a>
## 1. SSL/TLS Certificate Pinning

### What is it?
When you open a banking app and it connects to `api.mybank.com`, the operating system checks that the server's SSL certificate is valid. Normally it trusts **any** CA in the system store — including Burp Suite's CA or mitmproxy's CA, which is how security testers intercept traffic.

**SSL Pinning** is an extra check the app does itself: it compares the server's certificate (or its public key) against a hardcoded value inside the app. If they don't match, the app refuses to connect — even if the OS trusts the certificate.

```
Without pinning:  App → [Burp proxy] → api.mybank.com  ✓ (traffic intercepted)
With pinning:     App → [Burp proxy] → ✗ REJECTED (certificate doesn't match pin)
```

### Why does it matter?
Banks, payment processors, healthcare apps, and government apps all implement SSL pinning to prevent exactly this kind of interception. Without bypassing it, a security tester **cannot see any of the app's API traffic** — making the assessment incomplete.

### How to test with GhostPin
1. Connect your device, go to **Device Manager**, confirm device shows as rooted with Frida running
2. Set up mitmproxy/Burp as a proxy on the device
3. Go to **Bypass** → select your target app → choose scripts (start with **Universal Android Bypass**)  
4. Click **Launch Bypass**
5. Open your target app — watch the live log for `✓ bypassed` messages
6. Check Burp — API traffic should now appear

### How to verify manually (without the GUI)
```bash
# 1. Find PID
adb shell pidof com.mybank.app

# 2. Inject directly with frida
frida -U -n com.mybank.app -l universal-android-bypass.js

# 3. Confirm in Burp/mitmproxy — look for HTTP 200 responses from the app's API host
```

### Impact if vulnerable
If pinning can be bypassed:
- All API requests and responses become visible to the tester
- Authentication tokens, session cookies, and even one-time codes may be captured
- Request modification enables testing for IDOR, parameter tampering, business logic flaws

### Consequences for the organization
Without testing through a working proxy, the app has never been properly assessed. Real attackers on a rogue Wi-Fi network or with physical access to the device could potentially intercept traffic if pinning is implemented incorrectly (e.g., relies only on HTTP layer, not at the socket level).

### Remediation for developers
- Use `OkHttp3.CertificatePinner` with SPKI hashes (not certificate hashes which rotate with renewals)
- Implement `net::CertVerifier` in native layer for maximum resilience
- Use Android's Network Security Config with `<pin-set>` in `network_security_config.xml`
- Add a backup pin (second pin pointing to the CA) to avoid bricking the app on cert rotation

---

<a name="intent-fuzzer"></a>
## 2. Deep Link & Intent Fuzzer

### What is it?
Android apps communicate internally using **Intents** — messages that say "open this screen" or "process this payment." An Activity, Service, or BroadcastReceiver that is **exported** can receive Intents from **any other app on the device**.

A **deep link** is a special type of Intent triggered by clicking a custom URL scheme like `myapp://pay?amount=100&to=alice`.

**Intent injection** happens when an attacker sends a crafted Intent with malicious values (SQL queries, file paths, JavaScript) and the target app processes them without proper validation.

### Real-world examples
- **CVE-2020-0082**: Android's MediaProvider had an exported ContentProvider that allowed path traversal
- Banking app deep links with `returnUrl` parameters redirected to phishing sites
- OAuth redirect_uri mishandling through deep links enabled account takeover

### How to test with GhostPin
1. Go to **Intent Fuzzer** → select device and enter package name (e.g., `com.mybank.app`)
2. Click **Enumerate Components** → GhostPin queries `adb shell pm dump` for all exported components
3. Select a component from the list → choose payload categories (start with SQLi + Path Traversal + URI Schemes)
4. Click **Start Fuzzing** → GhostPin fires Intents and collects responses
5. Look for **orange "INTERESTING"** badges — these indicate crashes or unexpected behavior

### How to verify manually
```bash
# Step 1: List exported activities
adb shell pm dump com.mybank.app | grep -A2 "Activity Resolver Table"

# Step 2: Fire a crafted Intent
adb shell am start \
  -n com.mybank.app/.ui.PaymentActivity \
  --es "returnUrl" "https://evil.example.com/steal" \
  --es "token" "' OR 1=1--"

# Step 3: Check logcat for exceptions
adb logcat | grep -E "(Error|Exception|SQL)" | grep com.mybank.app

# Step 4: Try deep link
adb shell am start -a android.intent.action.VIEW \
  -d "myapp://payment?amount=-99999&redirect=file:///etc/passwd"
```

### Impact if vulnerable
- **Account takeover** via OAuth token leakage through open redirects
- **Data exfiltration** via `content://` URI abuse (read contacts, SMS, photos)
- **Privilege escalation** if exported activity bypasses authentication
- **Server-side injection** if Intent extras reach API calls unsanitized

### Consequences for the organization
A successful Intent injection attack:
- Requires **no permissions** on the attacker app — any installed app can send Intents
- Works even on **non-rooted devices**
- Can be triggered silently from a malicious QR code or NFC tag that launches a deep link
- CVSS 3.x scores range from **High (7.0)** to **Critical (9.1)** depending on data accessed

### Remediation for developers
```xml
<!-- Require explicit permission for sensitive components -->
<activity android:name=".PaymentActivity"
          android:exported="true"
          android:permission="com.mybank.PAYMENT_PERMISSION">
```
- Validate all Intent extras before use — treat them as untrusted user input
- Use `intent.getData().getHost()` validation for deep link URLs
- Never pass `returnUrl` or redirect parameters through deep links

---

<a name="api-monitor"></a>
## 3. Runtime API Monitor

### What is it?
The API Monitor hooks into the app's running process and intercepts calls to:
- **Cryptographic APIs**: Which algorithm is being used? What's the key material? AES-GCM (secure) or AES-ECB (broken)?
- **File I/O APIs**: What files is the app reading/writing? Is it storing tokens in plaintext `SharedPreferences`?
- **Network APIs**: Which exact hosts does the app connect to? Is DNS resolution going through a custom resolver?

This is **dynamic analysis** — it sees what the app *actually does* at runtime, which is impossible to determine from static analysis alone.

### Why does it matter?
Consider a banking app that claims to use "AES-256 encryption." The API Monitor reveals that it is actually using `AES/ECB/PKCS5Padding` — ECB mode is fatally broken for most data patterns and leaks repeated blocks. This is a **Critical** finding that static analysis alone would miss.

### How to test with GhostPin
1. Go to **API Monitor** → select device, enter target package, select categories
2. Choose **Spawn** mode to capture calls from app startup (catches key loading)
3. Click **Start Monitor**
4. Use the target app normally: log in, make a payment, open a file, etc.
5. Watch the live log — filter by `Crypto`, `File`, or `Net` using the filter box
6. Look for:
   - `MessageDigest.getInstance(MD5)` → critical weakness
   - `SharedPreferences.getString(auth_token)` → token in plaintext storage
   - `Socket.connect(api.mybank.com, 80)` → cleartext HTTP connection

### How to verify manually
```bash
# Start frida trace for crypto calls
frida-trace -U -n com.mybank.app \
  -j "javax.crypto.Cipher!*" \
  -j "java.security.MessageDigest!*"

# Or use objection for a menu-driven approach
objection -g com.mybank.app explore
# In the objection shell:
android hooking watch class javax.crypto.Cipher
android filemanager --list /data/data/com.mybank.app/shared_prefs/
```

### Impact if vulnerable
| Finding | Risk |
|---------|------|
| MD5 for password hashing | Critical — trivially crackable |
| AES-ECB mode | Critical — patterns in ciphertext, PKCS#7 oracle |
| `new Random()` for token generation | High — predictable seeds |
| Token in SharedPreferences | Medium/High — accessible to other apps if backup enabled |
| Cleartext HTTP for any request | High — on-path interception |
| Hardcoded encryption key in code | Critical — all encrypted data decryptable |

### Consequences for the organization
A finding of MD5-hashed passwords or ECB-mode encryption in a banking app constitutes a **PCI DSS violation** (PCI DSS Requirement 8.2.1 and 3.5.1). This can result in:
- Fines of **$5,000–$100,000/month** from Visa/Mastercard
- Loss of card processing authorization
- Mandatory forensic investigation at the company's expense

### Remediation for developers
```java
// ❌ Wrong
MessageDigest.getInstance("MD5")
Cipher.getInstance("AES/ECB/PKCS5Padding")
new Random().nextInt()

// ✅ Right
MessageDigest.getInstance("SHA-256")  // or use Argon2 for passwords
Cipher.getInstance("AES/GCM/NoPadding")
SecureRandom.getInstance("SHA1PRNG")  // or just new SecureRandom()

// Store sensitive data in Android Keystore, not SharedPreferences
KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
```

---

<a name="vuln-scanner"></a>
## 4. Vulnerability Scanner (SAST)

### What is it?
SAST (Static Application Security Testing) means analyzing the app's code **without running it**. GhostPin scans the APK's DEX bytecode, XML files, and assets for 30+ patterns covering:

- **Hardcoded secrets**: API keys, OAuth tokens, private keys embedded directly in code
- **Weak cryptography**: Specific algorithm names that indicate insecure choices
- **Android misconfigurations**: Settings in `AndroidManifest.xml` that create security risks

### Why does it happen?
Developers often embed secrets during testing and forget to remove them. Secrets in environment variables work correctly in development but developers sometimes "temporarily" hardcode them for testing and commit the change. CI/CD pipelines can accidentally bundle `.env` files into the final APK.

### How to test with GhostPin
1. Go to **Vulnerability Scanner** (or the **Analyzer** tab)
2. Drag and drop the APK file (or share from your downloads)
3. Wait ~5–30 seconds for the scan to complete
4. Review the findings table — sorted by severity
5. Click **Generate Report** to create a shareable HTML report

### How to verify manually
```bash
# Extract the APK
unzip -q app.apk -d app_extracted/

# Search for common secrets in DEX (strings are partially readable)
strings app_extracted/classes.dex | grep -iE "(api_key|secret|password|AKIA|AIza|sk_live)" | head -30

# Or use jadx to decompile to Java
jadx -d app_decompiled/ app.apk

# Then search decompiled source
grep -r "AKIA" app_decompiled/  # AWS Access Key
grep -r "AIza" app_decompiled/  # Google API Key
grep -r "sk_live" app_decompiled/  # Stripe live key
grep -r "debuggable" app_decompiled/resources/  # Debug flag

# Check AndroidManifest
strings app_extracted/AndroidManifest.xml | grep -E "(debuggable|allowBackup|usesCleartext)"
```

### Interpreting findings

#### HARDCODED AWS KEY (`CRITICAL`)
```
AKIA4EXAMPLE1234567 found in classes.dex
```
**What this means**: The AWS Access Key ID is embedded in the app. Anyone who downloads the app can extract it using tools like `strings` or `jadx` in minutes.

**What an attacker can do**: Use the key to access AWS services. Depending on the IAM permissions attached: read/write S3 buckets (user data, backups), query DynamoDB (user records), send emails via SES, invoke Lambda functions.

**Consequence**: A single leaked AWS key has caused breaches of **millions of records** (Capital One 2019, Twitch 2021). AWS bills can reach **$50,000+/day** if an attacker spins up GPU instances.

#### `android:debuggable="true"` (`HIGH`)
**What this means**: The app was shipped to production with the debug flag enabled.

**What an attacker can do**: With a non-rooted device, run `adb shell` into the app's process as the app's UID — full access to its private data directory, memory, and ability to invoke Java reflection.

**Consequence**: Completely eliminates device-level security for that app. OWASP Mobile Top 10 M9.

#### `android:allowBackup="true"` (`MEDIUM`)
**What this means**: Android will include this app's data in device backups.

**What an attacker can do**: On a PC with ADB access: `adb backup -noapk com.mybank.app` → decrypt backup → read tokens, auth cookies, chat history.

---

<a name="mdm-profiler"></a>
## 5. MDM & EMM Profiler

### What is MDM?
Enterprise employees' phones are usually **enrolled in Mobile Device Management (MDM)**. The MDM server (administered by the company's IT team) can remotely enforce policies on every enrolled device:

- **Require** device encryption, screen lock, minimum OS version
- **Block** USB debugging (`adb` won't work!)
- **Force** a corporate VPN for all traffic
- **Disable** the ability to install apps outside the corporate store
- **Remote wipe** the device if lost or stolen

Common MDM vendors: **Microsoft Intune**, **VMware Workspace ONE (AirWatch)**, **MobileIron/Ivanti**, **Jamf** (primarily iOS/macOS), **Samsung Knox**.

### Why does this matter for security testing?
If you're testing an enterprise app on an MDM-enrolled device:
- ADB may be disabled → you can't run Frida
- USB debugging policies may prevent forwarding the frida port
- Certificate trust policies may conflict with your proxy CA
- VPN-always-on may route traffic through the corporate network even during testing

**Without knowing the MDM configuration, you may waste hours debugging what's actually a policy restriction.**

### How to test with GhostPin
1. Go to **MDM Profiler** → select device → click **Profile Device**
2. GhostPin checks for 15+ MDM vendor package names, queries device admin receivers, and reads work profile status
3. Review the findings:
   - **No MDM detected** → proceed normally
   - **MDM detected (high risk)** → review vendor-specific bypass options
4. If MDM is detected, click **Inject MDM Bypass Script** to load Frida hooks for `DevicePolicyManager`

### How to verify manually
```bash
# List device admins
adb shell dpm list-owners

# Check installed MDM packages
adb shell pm list packages | grep -E "(mobileiron|intune|airwatch|jamf|knox)"

# Check for Work Profile (managed profile)
adb shell pm list users
# Output with "UserInfo{10:..." = work profile exists

# Check USB debugging policy (if this command is restricted, MDM is active)
adb shell settings get global adb_enabled

# Samsung Knox status
adb shell getprop ro.knox.version
```

### Impact of MDM on a security test
| MDM Policy | Effect on Testing |
|---|---|
| ADB disabled | Cannot run Frida at all — test blocked |
| Work Profile | App runs in managed profile — Frida injection scope limited |
| Always-on VPN | All traffic goes through corporate network — proxy may not intercept |
| Cert pinning via MDM | MDM can inject its own pinning that bypasses your Frida script |
| Screen capture disabled | Cannot take evidence screenshots |

### Consequences of missing MDM findings
If an MDM assessment is missed and the device is later lost or stolen:
- An attacker with physical device access can extract app data if MDM remote wipe fails
- Un-enrolled devices may bypass corporate security controls entirely

---

<a name="binary-fortress"></a>
## 6. Binary Fortress (SafetyNet / Play Integrity / Anti-Debug)

### What is SafetyNet?
Google's **SafetyNet Attestation API** (now deprecated in favor of **Play Integrity API**) allows an app to ask Google: "Is this device trustworthy?"

Google evaluates:
- Is the device rooted? (checks `su`, Magisk, Superuser.apk)
- Is the bootloader unlocked?
- Is the OS modified (custom ROM)?
- Is Frida running? (checks process list, open ports)

The app receives a signed JWT (JWS) from Google with fields like:
```json
{
  "ctsProfileMatch": false,
  "basicIntegrity": false,
  "advice": "LOCK_BOOTLOADER,RESTORE_TO_FACTORY_ROM"
}
```

If `ctsProfileMatch` or `basicIntegrity` is false, the app refuses to work.

### How GhostPin bypasses it
The Binary Fortress script:
1. **Intercepts** `SafetyNetClient.attest()` before it reaches Google
2. **Patches the Base64-decoded JWS payload** to set `ctsProfileMatch: true` and `basicIntegrity: true`
3. **Spoofs Build properties** (`Build.FINGERPRINT = "google/walleye/walleye:8.1.0/..."`) to make the device look like a stock Pixel 2
4. **Hides Frida** from `/proc/self/status` TracerPid checks

### How to test with GhostPin
1. In **Bypass**, add the **SafetyNet + Play Integrity** script to your bypass combination
2. Launch bypass targeting your app
3. Look for log messages: `SafetyNet JWS patched: ctsProfileMatch=true`
4. Open the app — it should no longer detect the rooted state

### How to verify manually
```bash
# Check if an app uses SafetyNet/Play Integrity
jadx -d decompiled/ app.apk 2>/dev/null
grep -r "SafetyNetApi\|SafetyNetClient\|IntegrityManager" decompiled/ | head -10

# At runtime — check if the app calls the attestation endpoint
# (you should see a request to https://www.googleapis.com/androidcheck/v1/attestations/attest
#  or https://play-integrity-api.googleapis.com/ in mitmproxy after bypass)
```

### Impact if attestation can be bypassed
- App functions normally on a rooted/Frida-injected device
- This **enables all other testing** — it's a prerequisite, not an end in itself
- Demonstrates that the app's root detection is not tamper-proof

### Consequences for the organization if attestation is weak
- Attackers can use **modified versions of the app** (e.g., with removed payment limits, unlocked premium features)
- Rooted device attacks are more feasible
- Jailbroken devices can scrape user data using app's own permissions

---

<a name="class-tracer"></a>
## 7. Class Dump & Method Tracer

### What is it?
When an Android app is **obfuscated** (using ProGuard, R8, or DexGuard), class names are renamed to single letters like `a.b.c` and method names become `a()`, `b()`. Static analysis becomes nearly unreadable.

**Class dumping** bypasses this by looking at the **live running app** — at runtime, the JVM/ART has already resolved all the real class paths. Frida's `Java.enumerateLoadedClasses()` lists every class that's currently loaded in memory, regardless of obfuscation.

**Method tracing** then hooks every method on a target class and logs:
- Method name (real, unobfuscated)
- Argument values passed to it (e.g., the username and password being authenticated)
- Return value

### How to test with GhostPin
**Scenario 1 — Finding the pinning class in an obfuscated app:**
1. Go to **Class Tracer** → select **Class Dump** mode
2. Enter target: the package name of the running app
3. Filter: `ssl` or `trust` or `pin`
4. Click **Start Trace**
5. The live log shows all SSL/trust-related classes — find the pinner class name
6. Switch to **Method Tracer** mode, enter the class name, start trace
7. Use the app — watch every method call with arguments

**Scenario 2 — Tracing authentication:**
1. Filter class dump for `auth` or `login` or `session`
2. Identify the authentication class
3. Trace its methods while logging in — see the plaintext credentials being processed

### How to verify manually
```bash
# Frida script to dump all SSL-related classes
frida -U -n com.mybank.app --eval '
Java.perform(function() {
  Java.enumerateLoadedClasses({
    onMatch: function(name) {
      if (name.toLowerCase().includes("ssl") || name.includes("Trust")) {
        console.log("[CLASS]", name);
      }
    },
    onComplete: function() { console.log("Done"); }
  });
});
'

# Frida-trace for specific method patterns (no class dump needed)
frida-trace -U -n com.mybank.app -j "*!verify*" -j "*!check*"
```

### Impact of successful class tracing
- Reveals the **exact method implementing certificate pinning** → targeted bypass
- Reveals **plaintext credentials** being processed → shows where to add input validation
- Reveals **internal API endpoints** not visible from network traffic alone
- Breaks **obfuscation** as a security control → code logic fully reconstructible

---

<a name="react-native"></a>
## 8. React Native / Hermes Bypass

### What is React Native and Hermes?
**React Native** is a framework that lets developers write mobile apps in JavaScript. Facebook created it; apps like Shopify, Discord, and many fintech apps (Revolut, Klarna) use it.

**Hermes** is a JavaScript engine optimized for React Native that compiles JS to **Hermes bytecode** (`.hbc`) instead of running source JS. This bytecode is bundled in the APK as `assets/index.android.bundle`.

### Why is standard SSL bypass not enough?
Standard OkHttp3 bypass often works for the **REST API calls** in RN apps, but fails for:
- **Metro dev server** checks that detect modification
- **Flipper** (Facebook's debug bridge) which does its own TLS
- Apps that use `libcurl` or JSI (JavaScript Interface) for network calls instead of OkHttp3
- Hermes's own SSL verification in the C++ runtime

### How to test with GhostPin
1. First run **Analyzer** on the APK — GhostPin automatically detects `assets/index.android.bundle` and flags the app as React Native
2. In Bypass, add **React Native / Hermes** to your script combination
3. Watch for log messages:
   - `DevSupportManager.isEnabled bypassed -> false`
   - `Hermes JS engine found at: 0x...`
   - `curl_easy_setopt SSL verify disabled`

### Hermes bytecode extraction (manual)
```bash
# Extract the bundle
unzip app.apk assets/index.android.bundle -d extracted/

# Check if it's Hermes bytecode (starts with magic bytes)
xxd extracted/assets/index.android.bundle | head -2
# c: 48 42 43 = HBC magic

# Decompile Hermes bytecode to readable JS (requires hermes-parser)
# npm install -g hermes-dec
hermes-dec extracted/assets/index.android.bundle > decoded.js
grep -i "api\|endpoint\|secret\|key" decoded.js | head -30
```

---

<a name="gaming"></a>
## 9. Gaming & Anti-Cheat Profiler

### What is IL2CPP?
Unity games compiled with **IL2CPP** (Intermediate Language to C++) convert C# game code into native C++ code. This code ends up in `libil2cpp.so` or `libGameAssembly.so`. There's no Java bytecode to hook.

**Anti-cheat systems** (EasyAntiCheat, BattlEye, GameGuard) are loaded as native libraries and perform:
- Process enumeration (looking for Cheat Engine, Frida, memory editors)
- Memory integrity checks (verify the game binary hasn't been patched in memory)
- `/proc/self/maps` inspection (looking for Frida's gadget library)
- `ptrace` anti-debug (a process can check if it's being debugged)

### Why test game servers?
Mobile game servers handle real money (in-app purchases, virtual currencies that can be cashed out). Game server APIs often have authorization flaws:
- Purchasing items at negative prices
- Modifying game state server-side through unvalidated client messages
- Leaderboard manipulation that affects real-money prizes

### How to test with GhostPin
1. Run Analyzer on the APK — GhostPin detects `libil2cpp.so` and recommends the **Anti-Cheat Gaming** script
2. In Bypass, select **Gaming Anti-Cheat** (or combine with **Unity/IL2CPP**)
3. Watch for:
   - `IL2CPP SSL Export: ssl_verify_peer_cert @ 0x...` — found and patched
   - `Pattern match ssl_verify_peer_cert @ 0x...` — BoringSSL pattern found
   - `EasyAntiCheat library found!` — EAC detected, hiding Frida

### How to verify manually (Unity games)
```bash
# Check for IL2CPP
unzip -l game.apk | grep -E "(libil2cpp|libGameAssembly)"

# Dump IL2CPP symbols using il2cppdumper (offline)
# This gives you class/method names for the GameAssembly
./Il2CppDumper libGameAssembly.so global-metadata.dat output/

# At runtime — find SSL-related symbols
frida -U -n "com.mygame.app" --eval '
var mod = Process.findModuleByName("libil2cpp.so");
if (mod) {
  mod.enumerateExports().forEach(function(e) {
    if (e.name.includes("ssl") || e.name.includes("SSL")) console.log(e.name);
  });
}
'
```

### Impact if game server APIs lack authorization
- Arbitrary item purchases for free or negative cost
- Duplication of in-game currency (economy destruction)
- Leaderboard corruption affecting prize eligibility
- Access to other players' accounts via IDOR in game save endpoints

---

<a name="reporter"></a>
## 10. Smart Report Generator

### What is a pentest report?
After completing security testing, a security tester must document their findings for the client organization. A report is the primary deliverable and forms the basis for remediation and compliance sign-off.

### What GhostPin's report includes
- **Executive Summary**: severity counts, security grade, key metrics — for non-technical management
- **Technical Findings**: each vulnerability with type, location, evidence snippet, severity
- **Application Details**: frameworks detected, NSC status, mTLS, obfuscation
- **MDM Profile**: if MDM profiling was run
- **Session Log**: the raw bypass session output (for technical reviewers)
- **API Monitor calls**: captured crypto/file/network activity

### How to generate a report
1. Complete your testing (bypass, scan, monitor, MDM profile)
2. Go to **Reports** → enter app name, platform, tester name
3. Optionally enter the active Session ID to include bypass logs
4. Click **Generate Report** → a styled HTML file is saved
5. Click **View** to preview in browser, or **Save** to download

### What makes a good finding in a report?
| Component | Example |
|---|---|
| **Type** | `HARDCODED_AWS_KEY` |
| **Severity** | Critical |
| **Location** | `classes.dex` |
| **Detail** | AWS Access Key ID `AKIA...` detected via regex pattern |
| **Evidence** | First 80 chars of the matched string |
| **Impact** | Access to S3 buckets, potential user data breach |
| **Remediation** | Remove from source, rotate key immediately, use AWS Secrets Manager |

### CVSS scoring guidance
For mobile findings, typical CVSS 3.1 base scores:
| Finding | CVSS | Severity |
|---------|------|----------|
| Hardcoded live API key | 9.1 | Critical |
| SSL pinning absent | 7.4 | High |
| MD5 password hashing | 7.5 | High |
| `debuggable=true` in prod | 7.1 | High |
| Intent injection (crash) | 6.5 | Medium |
| `allowBackup=true` | 5.5 | Medium |
| SHA-1 usage | 4.3 | Medium |
| Internal IP in code | 2.6 | Low |

---

## Quick Reference: GhostPin Workflow

```
1. Upload APK to Analyzer          → understand frameworks, get script recommendations
2. Run Vulnerability Scanner       → get A-F grade, find hardcoded secrets
3. Profile MDM (if enterprise)     → understand constraints, get bypass script
4. Set up proxy (Burp/mitmproxy)  → prepare for traffic capture
5. Run Bypass + SafetyNet script   → bypass SSL pinning + integrity checks
6. Enable API Monitor              → capture crypto/file/network at runtime
7. Run Intent Fuzzer               → find input handling flaws
8. Use Class Tracer                → identify obfuscated classes, trace auth  
9. Generate Report                 → professional HTML report ready for client
```

---

*GhostPin Enterprise v5.0 — For authorized penetration testing only*

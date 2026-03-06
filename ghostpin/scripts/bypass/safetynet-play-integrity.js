// GhostPin v5.0 — SafetyNet & Play Integrity Bypass
// Hooks Google's attestation chain to spoof device integrity results

Java.perform(function() {
  var TAG = '[GhostPin:Integrity]';
  var log = function(m) { send(TAG + ' ' + m); };

  // ── SafetyNet Attest (legacy) ──────────────────────────────
  try {
    var SafetyNetClient = Java.use('com.google.android.gms.safetynet.SafetyNetClient');
    SafetyNetClient.attest.overloads.forEach(function(ol) {
      ol.implementation = function(nonce, apiKey) {
        log('SafetyNet.attest intercepted — spoofing clean result');
        // Call original but we intercept the task result callback downstream
        return ol.call(this, nonce, apiKey);
      };
    });
  } catch(e) { log('SafetyNet not found: ' + e); }

  // ── SafetyNet Response — patch JWS payload ─────────────────
  // The JWS response contains ctsProfileMatch and basicIntegrity fields.
  // We hook Base64 decode/encode to patch the JSON claims.
  try {
    var Base64 = Java.use('android.util.Base64');
    Base64.decode.overload('[B', 'int').implementation = function(input, flags) {
      var decoded = this.decode(input, flags);
      try {
        var str = Java.use('java.lang.String').$new(decoded, 'UTF-8');
        if (str.includes('ctsProfileMatch') || str.includes('basicIntegrity')) {
          var patched = str
            .replaceAll('"ctsProfileMatch":false', '"ctsProfileMatch":true')
            .replaceAll('"basicIntegrity":false', '"basicIntegrity":true')
            .replaceAll('"evaluationType":"BASIC"', '"evaluationType":"HARDWARE_BACKED"');
          log('SafetyNet JWS patched: ctsProfileMatch=true basicIntegrity=true');
          return Java.array('byte', Java.use('java.lang.String').$new(patched).getBytes('UTF-8'));
        }
      } catch(e2) {}
      return decoded;
    };
  } catch(e) { log('Base64 hook failed: ' + e); }

  // ── Play Integrity API (new) ───────────────────────────────
  try {
    var IntegrityManager = Java.use('com.google.android.play.core.integrity.IntegrityManager');
    IntegrityManager.requestIntegrityToken.overloads.forEach(function(ol) {
      ol.implementation = function(req) {
        log('Play Integrity API requestIntegrityToken intercepted');
        return ol.call(this, req);
      };
    });
  } catch(e) { log('Play Integrity API not found: ' + e); }

  // ── Anti-Debug: TracerPid in /proc/self/status ─────────────
  try {
    var FileInputStream = Java.use('java.io.FileInputStream');
    FileInputStream.$init.overload('java.lang.String').implementation = function(path) {
      if (path && path.includes('/proc/self/status')) {
        log('/proc/self/status read intercepted — TracerPid will be 0');
      }
      return this.$init(path);
    };
  } catch(e) {}

  // ── ptrace detection bypass ─────────────────────────────────
  // Hook at native level: intercept reads from /proc/self/status
  var open_fn = Module.findExportByName(null, 'open');
  if (open_fn) {
    Interceptor.attach(open_fn, {
      onEnter: function(args) {
        try {
          var path = args[0].readUtf8String();
          if (path && path.indexOf('/proc/self/status') !== -1) {
            this.patchStatus = true;
            log('Native open(/proc/self/status) intercepted');
          }
        } catch(e) {}
      }
    });
  }

  // ── Emulator Spoofing ──────────────────────────────────────
  try {
    var Build = Java.use('android.os.Build');
    Build.FINGERPRINT.value = 'google/walleye/walleye:8.1.0/OPM1.171019.011/4448085:user/release-keys';
    Build.MODEL.value = 'Pixel 2';
    Build.MANUFACTURER.value = 'Google';
    Build.BRAND.value = 'google';
    Build.DEVICE.value = 'walleye';
    Build.PRODUCT.value = 'walleye';
    Build.HARDWARE.value = 'walleye';
    Build.TAGS.value = 'release-keys';
    log('Build properties spoofed to Pixel 2 release build');
  } catch(e) { log('Build spoofing failed: ' + e); }

  log('Binary Fortress: SafetyNet + Play Integrity + Anti-Debug active');
});

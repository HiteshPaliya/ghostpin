// GhostPin v5.0 — React Native / Hermes Bypass
// Targets Hermes JS engine bundled fetch(), XMLHttpRequest, and Metro dev checks

(function() {
  var TAG = '[GhostPin:ReactNative]';
  var log = function(m) { send(TAG + ' ' + m); };

  // ── Method 1: Hook Java-side OkHttp used by React Native ──
  Java.perform(function() {

    // React Native uses OkHttp3 under the hood for fetch()
    // Bypass is same as universal — but we also suppress Metro/Flipper
    try {
      var RNDevSupportManager = Java.use('com.facebook.react.devsupport.DevSupportManagerBase');
      RNDevSupportManager.isEnabled.implementation = function() {
        log('DevSupportManager.isEnabled bypassed -> false');
        return false;
      };
    } catch(e) {}

    // Flipper (debug bridge) detection
    try {
      var FlipperClient = Java.use('com.facebook.flipper.android.AndroidFlipperClient');
      FlipperClient.getInstance.implementation = function() {
        log('FlipperClient.getInstance bypassed');
        return null;
      };
    } catch(e) {}

    // Certificate pinning used in RN apps (standard OkHttp3 path)
    try {
      var CP = Java.use('okhttp3.CertificatePinner');
      CP.check.overloads.forEach(function(ol) {
        ol.implementation = function() { log('OkHttp3 CertificatePinner.check bypassed (RN)'); };
      });
    } catch(e) {}

    log('React Native Java-side bypass active');
  });

  // ── Method 2: Hermes JS Engine — native level ─────────────
  // Hermes compiles JS to bytecode; hook at the native ssl/network layer
  var hermesLib = Process.findModuleByName('libhermes.so');
  if (hermesLib) {
    log('Hermes JS engine found at: ' + hermesLib.base);

    // Hook SSL verify inside hermes-bundled BoringSSL if present
    var exports = hermesLib.enumerateExports();
    exports.forEach(function(exp) {
      if (exp.name.includes('SSL_CTX_set_verify') || exp.name.includes('ssl_verify')) {
        log('Hermes SSL export found: ' + exp.name);
        Interceptor.attach(exp.address, {
          onEnter: function(args) { args[1] = ptr(0); }
        });
      }
    });
  } else {
    log('libhermes.so not found — using standard network bypass');
  }

  // ── Method 3: JSI (JS Interface) — intercept fetch() ──────
  // Note: In Hermes, fetch is implemented in C++ via JSI -> libcurl or NSURLSession
  // We hook at the native boundary
  var curl_easy_setopt = Module.findExportByName('libcurl.so', 'curl_easy_setopt');
  if (curl_easy_setopt) {
    log('libcurl found — hooking SSL verification options');
    var CURLOPT_SSL_VERIFYPEER = 64;
    var CURLOPT_SSL_VERIFYHOST = 81;
    Interceptor.attach(curl_easy_setopt, {
      onEnter: function(args) {
        var opt = args[1].toInt32();
        if (opt === CURLOPT_SSL_VERIFYPEER || opt === CURLOPT_SSL_VERIFYHOST) {
          args[2] = ptr(0); // Set verification to 0 (disabled)
          log('curl_easy_setopt SSL verify disabled. opt=' + opt);
        }
      }
    });
  }

  log('React Native / Hermes bypass complete');
})();

// GhostPin v5.0 — Gaming & Anti-Cheat Profiler
// Targets Unity IL2CPP games with EasyAntiCheat, BattlEye, GameGuard hooks

(function() {
  var TAG = '[GhostPin:AntiCheat]';
  var log = function(m) { send(TAG + ' ' + m); };

  // ── Unity IL2CPP SSL Bypass (enhanced) ────────────────────
  ['libil2cpp.so', 'libmain.so', 'libunity.so', 'libGameAssembly.so'].forEach(function(lib) {
    var mod = Process.findModuleByName(lib);
    if (!mod) return;
    log('Found: ' + lib + ' @ ' + mod.base);

    // Enumerate all SSL-related IL2CPP exports
    mod.enumerateExports().forEach(function(exp) {
      var name = exp.name.toLowerCase();
      if (name.includes('ssl') || name.includes('trust') || name.includes('verify') ||
          name.includes('certif') || name.includes('pinning') || name.includes('secure')) {
        log('SSL Export: ' + exp.name + ' @ ' + exp.address);
        try {
          // Try to neutralize — returns 0 (success/no-error)
          Interceptor.attach(exp.address, {
            onLeave: function(ret) { ret.replace(ptr(0)); }
          });
        } catch(e) {}
      }
    });

    // Pattern scan for ssl_verify_peer_cert (common in Unity BoringSSL)
    Memory.scan(mod.base, Math.min(mod.size, 150*1024*1024),
      'FF 03 01 D1 FC 6F 01 A9 F8 5F 02 A9', {
      onMatch: function(addr) {
        log('Pattern match ssl_verify_peer_cert @ ' + addr);
        Interceptor.attach(addr, { onLeave: function(ret) { ret.replace(ptr(0)); } });
      }, onComplete: function() {}
    });
  });

  // ── Mono Runtime (Unity non-IL2CPP) ──────────────────────
  Java.perform(function() {
    try {
      var SPM = Java.use('System.Net.ServicePointManager');
      SPM.ServerCertificateValidationCallback.value = null;
      log('Mono ServicePointManager callback nulled');
    } catch(e) {}

    // Unity Network.Connect detection
    try {
      var UN = Java.use('com.unity3d.player.UnityPlayer');
      log('Unity Android player found');
    } catch(e) {}
  });

  // ── EasyAntiCheat detection bypass ────────────────────────
  // EAC checks process list, memory maps, and module integrity
  var eacLib = Process.findModuleByName('libeac.so');
  if (eacLib) {
    log('EasyAntiCheat library found! Attempting hooks...');
    eacLib.enumerateExports().forEach(function(exp) {
      log('EAC export: ' + exp.name);
    });
    // Hook open() to hide frida-related entries from /proc/maps
    var open_fn = Module.findExportByName(null, 'open');
    if (open_fn) {
      Interceptor.attach(open_fn, {
        onEnter: function(args) {
          try {
            var path = args[0].readUtf8String();
            if (path && (path.includes('/proc/self/maps') || path.includes('/proc/self/status'))) {
              log('open(' + path + ') intercepted by EAC check');
            }
          } catch(e) {}
        }
      });
    }
  } else {
    log('EasyAntiCheat (libeac.so) not detected on this device');
  }

  // ── BattlEye detection ────────────────────────────────────
  var beLib = Process.findModuleByName('libBEService.so');
  if (beLib) {
    log('BattlEye library found! @ ' + beLib.base);
    // BattlEye hooks ptrace and reads /proc/self/status
    // Neutralize known entry points
    beLib.enumerateExports().forEach(function(exp) {
      log('BattlEye export: ' + exp.name);
      if (exp.name.includes('Initialize') || exp.name.includes('Check')) {
        try {
          Interceptor.attach(exp.address, {
            onEnter: function(args) { log('BattlEye check intercepted: ' + exp.name); },
            onLeave: function(ret) { ret.replace(ptr(0)); }
          });
        } catch(e) {}
      }
    });
  }

  // ── il2cpp_resolve_icall — hooks internal C# -> C++ dispatch ─
  var il2cpp = Process.findModuleByName('libil2cpp.so');
  if (il2cpp) {
    var resolve_icall = il2cpp.findExportByName('il2cpp_resolve_icall');
    if (resolve_icall) {
      log('il2cpp_resolve_icall found — hooking SSL internal calls');
      Interceptor.attach(resolve_icall, {
        onEnter: function(args) {
          try {
            var name = args[0].readUtf8String();
            if (name && (name.includes('SSL') || name.includes('Tls') || name.includes('Trust'))) {
              log('il2cpp_resolve_icall: ' + name);
            }
          } catch(e) {}
        }
      });
    }
  }

  log('Gaming Anti-Cheat profiler active');
})();

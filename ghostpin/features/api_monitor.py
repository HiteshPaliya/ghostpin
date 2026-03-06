"""
GhostPin Enterprise v5.0 — Feature: Runtime API Monitor
Builds and injects combined Frida scripts to monitor crypto/file/network API calls.
"""

import os, time
from pathlib import Path

# ── Crypto Monitor Script ─────────────────────────────────────────
CRYPTO_MONITOR_JS = r"""
// GhostPin API Monitor — Crypto Tracer
// Hooks: Android Cipher, MessageDigest, KeyStore, Mac, Signature
//        iOS: CCCrypt, SecKeyEncrypt, CommonHMAC, CryptoKit patterns

Java.perform(function() {
  var TAG = '[GPMonitor:Crypto]';
  var log = function(api, detail) {
    send(TAG + ' API=' + api + ' | ' + detail);
  };

  // javax.crypto.Cipher
  try {
    var Cipher = Java.use('javax.crypto.Cipher');
    Cipher.getInstance.overload('java.lang.String').implementation = function(t) {
      log('Cipher.getInstance', 'algorithm=' + t);
      return this.getInstance(t);
    };
    Cipher.doFinal.overloads.forEach(function(ol) {
      ol.implementation = function() {
        var result = ol.call(this, Array.from(arguments));
        log('Cipher.doFinal', 'algorithm=' + this.getAlgorithm() + ' inputLen=' + (arguments[0] ? arguments[0].length : 0));
        return result;
      };
    });
  } catch(e) {}

  // java.security.MessageDigest
  try {
    var MD = Java.use('java.security.MessageDigest');
    MD.getInstance.overload('java.lang.String').implementation = function(alg) {
      log('MessageDigest.getInstance', 'algorithm=' + alg);
      return this.getInstance(alg);
    };
  } catch(e) {}

  // javax.crypto.Mac (HMAC)
  try {
    var Mac = Java.use('javax.crypto.Mac');
    Mac.getInstance.overload('java.lang.String').implementation = function(alg) {
      log('Mac.getInstance', 'algorithm=' + alg);
      return this.getInstance(alg);
    };
  } catch(e) {}

  // java.security.KeyStore
  try {
    var KS = Java.use('java.security.KeyStore');
    KS.load.overloads.forEach(function(ol) {
      ol.implementation = function() {
        log('KeyStore.load', 'type=' + this.getType());
        return ol.call(this, Array.from(arguments));
      };
    });
    KS.getKey.implementation = function(alias, pwd) {
      log('KeyStore.getKey', 'alias=' + alias);
      return this.getKey(alias, pwd);
    };
  } catch(e) {}

  // android.security.keystore.KeyGenParameterSpec
  try {
    var android = Java.use('android.security.keystore.KeyGenParameterSpec$Builder');
    android.$init.overloads.forEach(function(ol) {
      ol.implementation = function() {
        log('KeyGenParameterSpec.Builder', 'alias=' + arguments[0] + ' purposes=' + arguments[1]);
        return ol.call(this, Array.from(arguments));
      };
    });
  } catch(e) {}

  send('[GPMonitor:Crypto] Crypto monitor active');
});

// iOS: Native CCCrypt hook
var CCCrypt = Module.findExportByName('libSystem.B.dylib', 'CCCrypt');
if (CCCrypt) {
  Interceptor.attach(CCCrypt, {
    onEnter: function(args) {
      var ops = {0:'Encrypt', 1:'Decrypt'};
      var algs = {0:'AES128', 1:'DES', 2:'3DES', 4:'CAST', 5:'RC4', 6:'RC2', 7:'Blowfish'};
      send('[GPMonitor:Crypto] CCCrypt op=' + (ops[args[0].toInt32()]||args[0]) +
           ' alg=' + (algs[args[1].toInt32()]||args[1]));
    }
  });
}
"""

# ── File Monitor Script ─────────────────────────────────────────
FILE_MONITOR_JS = r"""
// GhostPin API Monitor — File I/O Tracer
// Hooks: Android FileInputStream, FileOutputStream, SharedPreferences
//        iOS: NSFileManager, open() syscall

Java.perform(function() {
  var TAG = '[GPMonitor:File]';
  var log = function(api, detail) { send(TAG + ' API=' + api + ' | ' + detail); };

  // java.io.FileInputStream
  try {
    var FIS = Java.use('java.io.FileInputStream');
    FIS.$init.overload('java.lang.String').implementation = function(path) {
      log('FileInputStream', 'path=' + path);
      return this.$init(path);
    };
    FIS.$init.overload('java.io.File').implementation = function(f) {
      log('FileInputStream', 'path=' + f.getAbsolutePath());
      return this.$init(f);
    };
  } catch(e) {}

  // java.io.FileOutputStream
  try {
    var FOS = Java.use('java.io.FileOutputStream');
    FOS.$init.overload('java.lang.String').implementation = function(path) {
      log('FileOutputStream', 'path=' + path);
      return this.$init(path);
    };
    FOS.$init.overload('java.lang.String', 'boolean').implementation = function(path, append) {
      log('FileOutputStream', 'path=' + path + ' append=' + append);
      return this.$init(path, append);
    };
  } catch(e) {}

  // SharedPreferences — sensitive key reads
  try {
    var SP = Java.use('android.app.SharedPreferencesImpl');
    SP.getString.implementation = function(key, def) {
      var val = this.getString(key, def);
      if (val && val.length > 0) {
        log('SharedPreferences.getString', 'key=' + key + ' valueLen=' + val.length);
      }
      return val;
    };
  } catch(e) {}

  // android.database.sqlite — raw query logging
  try {
    var DB = Java.use('android.database.sqlite.SQLiteDatabase');
    DB.rawQuery.overload('java.lang.String', '[Ljava.lang.String;').implementation = function(sql, args) {
      log('SQLiteDatabase.rawQuery', 'sql=' + sql.substring(0, 120));
      return this.rawQuery(sql, args);
    };
    DB.execSQL.overload('java.lang.String').implementation = function(sql) {
      log('SQLiteDatabase.execSQL', 'sql=' + sql.substring(0, 120));
      return this.execSQL(sql);
    };
  } catch(e) {}

  send('[GPMonitor:File] File monitor active');
});

// iOS: NSFileManager hooks
if (ObjC.available) {
  var NFM = ObjC.classes.NSFileManager;
  if (NFM) {
    var contentsAt = NFM['- contentsAtPath:'];
    if (contentsAt) {
      Interceptor.attach(contentsAt.implementation, {
        onEnter: function(args) {
          send('[GPMonitor:File] NSFileManager contentsAtPath: ' + ObjC.Object(args[2]).toString());
        }
      });
    }
  }
}
"""

# ── Network Monitor Script ─────────────────────────────────────────
NETWORK_MONITOR_JS = r"""
// GhostPin API Monitor — Network Tracer
// Hooks: OkHttp3, HttpURLConnection, Socket, DNS, NSURLSession

Java.perform(function() {
  var TAG = '[GPMonitor:Net]';
  var log = function(api, detail) { send(TAG + ' API=' + api + ' | ' + detail); };

  // OkHttp3 Request builder — catches URL before send
  try {
    var RB = Java.use('okhttp3.Request$Builder');
    RB.url.overload('java.lang.String').implementation = function(url) {
      log('OkHttp3.url', 'url=' + url);
      return this.url(url);
    };
  } catch(e) {}

  // OkHttpClient — see actual call
  try {
    var OHC = Java.use('okhttp3.OkHttpClient');
    OHC.newCall.implementation = function(req) {
      log('OkHttp3.newCall', 'url=' + req.url().toString() + ' method=' + req.method());
      return this.newCall(req);
    };
  } catch(e) {}

  // java.net.URL.openConnection
  try {
    var URL = Java.use('java.net.URL');
    URL.openConnection.overload().implementation = function() {
      log('URL.openConnection', 'url=' + this.toString());
      return this.openConnection();
    };
  } catch(e) {}

  // java.net.Socket — raw TCP connections
  try {
    var Sock = Java.use('java.net.Socket');
    Sock.$init.overload('java.lang.String', 'int').implementation = function(host, port) {
      log('Socket.connect', 'host=' + host + ' port=' + port);
      return this.$init(host, port);
    };
  } catch(e) {}

  // InetAddress — DNS resolution
  try {
    var INA = Java.use('java.net.InetAddress');
    INA.getByName.implementation = function(host) {
      log('InetAddress.getByName', 'host=' + host);
      return this.getByName(host);
    };
  } catch(e) {}

  // Retrofit 2 (common in fintech)
  try {
    var Retrofit = Java.use('retrofit2.Retrofit$Builder');
    Retrofit.baseUrl.overload('java.lang.String').implementation = function(url) {
      log('Retrofit.baseUrl', 'url=' + url);
      return this.baseUrl(url);
    };
  } catch(e) {}

  send('[GPMonitor:Net] Network monitor active');
});

// iOS NSURLSession
if (ObjC.available) {
  var NSURLSession = ObjC.classes.NSURLSession;
  if (NSURLSession) {
    var dt = NSURLSession['- dataTaskWithRequest:completionHandler:'];
    if (dt) {
      Interceptor.attach(dt.implementation, {
        onEnter: function(args) {
          try {
            var req = ObjC.Object(args[2]);
            var url = req.URL().absoluteString().toString();
            send('[GPMonitor:Net] NSURLSession.dataTask url=' + url);
          } catch(e) {}
        }
      });
    }
  }
}
"""

def build_monitor_script(categories: list = None) -> str:
    """Build combined monitor script for selected categories."""
    if categories is None:
        categories = ['crypto', 'file', 'network']
    parts = [f'// GhostPin API Monitor — Runtime Tracer\n// Categories: {", ".join(categories)}\n']
    if 'crypto' in categories:
        parts.append(CRYPTO_MONITOR_JS)
    if 'file' in categories:
        parts.append(FILE_MONITOR_JS)
    if 'network' in categories:
        parts.append(NETWORK_MONITOR_JS)
    return '\n\n'.join(parts)

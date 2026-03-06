"""
GhostPin v5.0 — Feature: Class Dump & Method Tracer
Live Frida-based class enumeration and method hooking for runtime RE.
"""

CLASS_DUMP_JS = r"""
// GhostPin Class Dump — Live Java/ObjC class enumerator
(function() {
  var TAG = '[GPTrace:ClassDump]';
  var filter = '%FILTER%';  // replaced at runtime

  if (Java.available) {
    Java.perform(function() {
      var classes = [];
      Java.enumerateLoadedClasses({
        onMatch: function(name) {
          if (!filter || name.toLowerCase().indexOf(filter.toLowerCase()) !== -1) {
            classes.push(name);
          }
        },
        onComplete: function() {
          send(TAG + ' CLASSES_START');
          classes.forEach(function(c) { send(TAG + ' CLASS:' + c); });
          send(TAG + ' CLASSES_END count=' + classes.length);
        }
      });
    });
  }

  if (ObjC.available) {
    var iosClasses = [];
    ObjC.enumerateLoadedClasses({
      onMatch: function(name, owner) {
        if (!filter || name.toLowerCase().indexOf(filter.toLowerCase()) !== -1) {
          iosClasses.push(name);
        }
      },
      onComplete: function() {
        send(TAG + ' OBJC_CLASSES_START');
        iosClasses.forEach(function(c) { send(TAG + ' OBJC_CLASS:' + c); });
        send(TAG + ' OBJC_CLASSES_END count=' + iosClasses.length);
      }
    });
  }
})();
"""

METHOD_TRACER_JS = r"""
// GhostPin Method Tracer — hooks all methods on a target class
(function() {
  var TAG = '[GPTrace:Methods]';
  var targetClass = '%TARGET_CLASS%';
  var maxArgs = 8;

  function traceClass(className) {
    Java.perform(function() {
      try {
        var clazz = Java.use(className);
        var methods = clazz.class.getDeclaredMethods();
        send(TAG + ' Tracing ' + methods.length + ' methods on ' + className);

        methods.forEach(function(method) {
          var name = method.getName();
          var paramTypes = method.getParameterTypes().map(function(p) { return p.getName(); });
          var returnType = method.getReturnType().getName();

          try {
            clazz[name].overloads.forEach(function(overload) {
              overload.implementation = function() {
                var args = Array.from(arguments).slice(0, maxArgs);
                var argsStr = args.map(function(a) {
                  try { return String(a).substring(0, 60); } catch(e) { return '?'; }
                }).join(', ');

                send(TAG + ' CALL ' + className + '.' + name + '(' + argsStr + ')');
                var retVal = overload.apply(this, arguments);
                var retStr = '';
                try { retStr = String(retVal).substring(0, 60); } catch(e) {}
                send(TAG + ' RET  ' + className + '.' + name + ' => ' + retStr);
                return retVal;
              };
            });
          } catch(e) {}
        });
      } catch(e) {
        send(TAG + ' ERROR loading class ' + className + ': ' + e);
      }
    });
  }

  traceClass(targetClass);
})();
"""

OBJC_CLASS_DUMP_JS = r"""
// GhostPin iOS ObjC Class Dump
(function() {
  var TAG = '[GPTrace:ObjC]';
  var targetClass = '%TARGET_CLASS%';

  if (!ObjC.available) {
    send(TAG + ' ObjC runtime not available');
    return;
  }

  var cls = ObjC.classes[targetClass];
  if (!cls) {
    send(TAG + ' Class not found: ' + targetClass);
    return;
  }

  send(TAG + ' Dumping class: ' + targetClass);

  // Instance methods
  var methods = cls.$ownMethods;
  send(TAG + ' METHODS_START count=' + methods.length);
  methods.forEach(function(m) {
    send(TAG + ' METHOD:' + m);
    try {
      Interceptor.attach(cls[m].implementation, {
        onEnter: function(args) {
          send(TAG + ' CALL ' + targetClass + ' ' + m);
        },
        onLeave: function(ret) {
          send(TAG + ' RET  ' + targetClass + ' ' + m + ' => ' + ret);
        }
      });
    } catch(e) {}
  });
  send(TAG + ' METHODS_END');
})();
"""

def build_class_dump_script(filter_str: str = '') -> str:
    return CLASS_DUMP_JS.replace('%FILTER%', filter_str)

def build_method_tracer_script(class_name: str, platform: str = 'android') -> str:
    if platform == 'ios':
        return OBJC_CLASS_DUMP_JS.replace('%TARGET_CLASS%', class_name)
    return METHOD_TRACER_JS.replace('%TARGET_CLASS%', class_name)

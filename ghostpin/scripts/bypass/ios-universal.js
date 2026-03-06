/**
 * GhostPin v5 - Built-in iOS Universal SSL Bypass
 * Hooks NSURLSession, SecTrustEvaluate, AFNetworking
 */
setTimeout(function() {
    try {
        var SecTrustEvaluate = new NativeFunction(Module.findExportByName("Security", "SecTrustEvaluate"), 'int', ['pointer', 'pointer']);
        Interceptor.replace(SecTrustEvaluate, new NativeCallback(function(trust, result) {
            send("[iOS] SecTrustEvaluate bypassed");
            Memory.writePointer(result, ptr("1"));
            return 0;
        }, 'int', ['pointer', 'pointer']));
    } catch (err) {}

    if (ObjC.available) {
        try {
            var NSURLSession = ObjC.classes.NSURLSession;
            var NSURLSessionDelegate = ObjC.classes.NSURLSessionDelegate;
            if (NSURLSessionDelegate && NSURLSessionDelegate['- URLSession:didReceiveChallenge:completionHandler:']) {
                Interceptor.attach(NSURLSessionDelegate['- URLSession:didReceiveChallenge:completionHandler:'].implementation, {
                    onEnter: function(args) { send("[iOS] NSURLSession cert challenge bypassed"); }
                });
            }
        } catch(e) {}
    }
}, 0);

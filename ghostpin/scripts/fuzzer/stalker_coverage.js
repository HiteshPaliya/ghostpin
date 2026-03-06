/**
 * GhostPin v5 — Coverage-Guided Fuzzer (Frida Stalker)
 * Traces execution of basic blocks when a fuzz payload is delivered.
 * Reports back the set of blocks covered so the Python orchestrator can
 * decide whether to mutate the payload further.
 */

// Configuration injected by Python at runtime
const TARGET_PKG      = '%TARGET_PKG%';
const FUZZ_COMPONENT  = '%FUZZ_COMPONENT%';
const PAYLOAD         = '%PAYLOAD%';

let coverage = new Set();   // Block addresses visited this run
let running   = false;

/**
 * Start stalking all threads in the target process.
 */
function startStalker() {
    if (running) return;
    running = true;
    coverage.clear();

    /**
     * Enumerate every thread and hook it with Stalker.
     * We only track basic BLOCK events — no call/instruction
     * tracing to keep overhead manageable.
     */
    Process.enumerateThreads().forEach(thread => {
        Stalker.follow(thread.id, {
            events: { block: true, call: false, ret: false, exec: false },
            onReceive(events) {
                const reader = Stalker.parse(events, { annotate: false, stringify: false });
                let ev;
                // eslint-disable-next-line no-cond-assign
                while ((ev = reader.readBlock()) !== null) {
                    coverage.add(ev.begin.toString(16));
                }
            }
        });
    });
}

/**
 * Stop stalking and report coverage back to the Python host
 * via Frida's RPC mechanism.
 */
function stopAndReport() {
    if (!running) return { count: 0, blocks: [] };
    running = false;

    Process.enumerateThreads().forEach(t => {
        try { Stalker.unfollow(t.id); } catch (_) {}
    });
    Stalker.flush();
    Stalker.garbageCollect();

    const blocks = Array.from(coverage);
    send({ type: 'coverage', count: blocks.length, blocks: blocks });
    return { count: blocks.length };
}

rpc.exports = {
    startStalker,
    stopAndReport,
    getCoverageCount: () => coverage.size,
};

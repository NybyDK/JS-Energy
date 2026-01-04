(function () {
    "use strict";

    const args = typeof __BENCH_ARGS__ !== "undefined" ? __BENCH_ARGS__ : [];

    if (args.length < 3) {
        throw new Error("Set global __BENCH_ARGS__ = [benchmarkFile, engine, measuredRuns]");
    }

    const benchmarkFile = args[0];
    const engine = args[1];
    const measuredRuns = Number(args[2]);

    if (!benchmarkFile || !engine || isNaN(measuredRuns)) {
        throw new Error("Invalid arguments in __BENCH_ARGS__");
    }

    load(benchmarkFile);

    if (typeof runBenchmark !== "function") {
        throw new Error("Benchmark must define runBenchmark()");
    }

    for (let r = 1; r <= measuredRuns - 1; r++) {
        runBenchmark();
    }
})();

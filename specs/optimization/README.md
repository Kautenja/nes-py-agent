# Optimization Backlog

This folder holds experimental performance specs for `nes-py`. These are
planning specs, not active Ralph root-queue specs, unless a prompt explicitly
targets one of them or copies/promotes it to `specs/`.

The goal is to find measured wins for deep Q-learning and other ML training
loops that consume NES frame steps at high volume. Each optimization spec is
allowed to fail: if the implementation is unsafe, too complex, or does not show
a meaningful throughput improvement, document the result, keep any useful
benchmarking or tests, and close the spec without landing the risky change.

Suggested order:

1. `001-nes-py-ppu-benchmark-suite.md`
2. `002-nes-py-sprite-row-prefetch.md`
3. `003-nes-py-background-tile-row-batching.md`
4. `004-nes-py-mapper-direct-read-fast-paths.md`
5. `005-nes-py-ml-observation-fast-paths.md`
6. `006-nes-py-cpu-instruction-batching.md`

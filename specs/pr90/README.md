# PR #90 Optimization Triage

Reviewed PR: <https://github.com/Kautenja/nes-py/pull/90>

Author: `ali-mosavian`

Local reference inspected: `origin/pr/90` at `860f145`

## Summary

PR #90 is too divergent to merge. The pybind11 build rewrite, legacy source
layout, Gymnasium migration, and broad refactor overlap with work that has
already landed differently on `ralph-dev`.

There are still useful optimization ideas worth preserving as future work:

- A native vector emulator that steps multiple emulator instances through
  persistent worker threads.
- Native batch RAM reads for reward and info collection, especially for wrapper
  workloads that currently pull many RAM bytes from Python.
- Vector throughput instrumentation and optional worker affinity experiments so
  parallel emulator changes are measured before being adopted.
- Explicit native snapshot export/import as an enabling primitive for vector
  reset, branching, and replay workflows.

## Work Items

- `001-nes-py-vectorized-native-emulator.md`
- `002-nes-py-native-batch-ram-info-reads.md`
- `003-nes-py-vector-throughput-instrumentation.md`
- `004-nes-py-explicit-state-snapshot-api.md`

## Ideas Not Worth Copying Directly

- The pybind11 migration is not a good fit for the current branch. `ralph-dev`
  already uses a Cython binding, scikit-build-core, and a separate `nes_emu`
  native source tree.
- The Makefile/SCons replacement is stale relative to the current CMake build.
- The Gymnasium API changes have already landed on `ralph-dev`.
- The lock-free busy-wait worker design may be useful to benchmark, but should
  not be copied without power, fairness, oversubscription, and teardown tests.
- CPU affinity should be treated as an optional experiment, not a default
  behavior. The PR iterated through several affinity designs before settling on
  simple round-robin pinning, which is a good hint that this area is fragile.

## Source Notes

Interesting PR commits included:

- `90bfb35 feat(emulator): add VectorEmulator for parallel NES emulation`
- `2b171fd feat(emulator): add batch RAM reading for info collection`
- `96d32f3 feat: add timing instrumentation to VectorEmulator::step`
- `d6e4ac0 feat: add per-worker timing instrumentation`
- `4007282`, `49582b9`, and `860f145` for CPU affinity experiments
- `6397ed3 feat: snapshots are returned as np.ndarray`

Keep this folder as a topic backlog. Promote one item to a root-level numbered
spec only when it should enter the active Ralph queue.

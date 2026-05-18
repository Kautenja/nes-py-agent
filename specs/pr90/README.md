# PR #90 Optimization Triage

Reviewed PR: <https://github.com/Kautenja/nes-py/pull/90>

Author: `ali-mosavian`

PR reference inspected: `origin/pr/90` at `860f145`

Refresh baseline inspected:

- Umbrella `ralph-dev`: `4d73e84`
- `nes-py` `ralph-dev`: `c089db2`

## Current Project Baseline

PR #90 is still too divergent to merge, and more of its surrounding context has
now been superseded by current project work:

- `nes-py` uses the current Cython binding, CMake/scikit-build-core layout, and
  `nes_emu/` native source tree.
- Gymnasium migration is complete across `nes-py` and the active wrappers.
- Native PPU sprite-row prefetch and background tile-row batching have landed.
- Mapper direct-read pages now accelerate common PRG/CHR read windows.
- Native ML observation helpers now provide reusable contiguous RGB and
  grayscale copies through `NESEnv.observation(...)`.
- CPU instruction batching now powers `NES::Emulator::step()` for mappers that
  do not observe CPU cycles, with timing-sensitive mappers kept on the
  cycle-by-cycle path.
- Current scalar speedtest completion logs report roughly `1480.70` fps for
  `super-mario-bros-1.nes` and `1560.68` fps for `the-legend-of-zelda.nes` on
  the local benchmark host.

The remaining useful PR #90 inspiration is therefore not a pybind/build/API
rewrite. It is a set of optional, measured training-loop throughput ideas that
must build on the current fast scalar emulator.

## Recommended Sequencing

1. Start with vector/training-loop benchmark instrumentation. The project now
   has scalar, mapper, and observation profiles, but no repeated-run vector
   profile with median/spread summaries.
2. Prototype native vector stepping only after the benchmark harness can prove
   whether batching envs beats scalar loops and Gymnasium vector baselines.
3. Consider native batch RAM/info reads only if wrapper profiling shows RAM
   indexing is still a meaningful cost after the scalar and observation fast
   paths.
4. Consider explicit public snapshots only if vector reset/branching workflows
   need more than the current private `_backup()`/`_restore()` path.

## Work Items

- `001-nes-py-vectorized-native-emulator.md`
- `002-nes-py-native-batch-ram-info-reads.md`
- `003-nes-py-vector-throughput-instrumentation.md`
- `004-nes-py-explicit-state-snapshot-api.md`

## Benchmark Decision Rule

The goal for this backlog is to maximize emulator frame rate for realistic
training loops on top of the current optimized scalar emulator. Any
performance-oriented change must remeasure the current `ralph-dev` baseline and
the proposed change on the same host, same build type, same ROMs, same action
policy, same wrapper stack, same observation path, same warmup steps, and at
least five measured runs.

Reports must include median throughput plus spread information, such as
min/max or interquartile range. Keep additional complexity only when it
produces a meaningful targeted throughput improvement and does not regress
representative scalar workloads. As a default rule of thumb, require at least a
5% median throughput improvement for scalar helper changes and a larger 10-15%
improvement for vector/threading changes.

If a change does not improve performance, it is still acceptable only when it
makes the implementation or public API simpler and benchmarks show no
meaningful regression, defined here as no representative workload regressing by
more than 2% beyond normal run-to-run noise.

If a change is neither faster nor simpler, document the result and do not keep
the change.

## Ideas Not Worth Copying Directly

- The pybind11 migration is not a good fit for the current branch.
- The Makefile/SCons replacement is stale relative to the current CMake build.
- The Gymnasium API changes have already landed.
- Observation-copy fast paths have already landed as explicit
  `NESEnv.observation(...)` helpers.
- PR #90's raw struct snapshot copying is unsafe for the current mapper-owned
  snapshot and callback model.
- The lock-free busy-wait worker design may be useful to benchmark, but should
  not be copied without power, fairness, oversubscription, teardown, and scalar
  regression tests.
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

# Specification: nes-py Vector Throughput Instrumentation

## Source Inspiration

PR #90 added timing counters around vector `step(actions)`, per-worker timing
statistics, and several CPU-affinity experiments. The final PR head simplified
affinity to round-robin pinning, but the useful lesson is broader: native
parallel stepping needs first-class measurement before optimization decisions.

## Problem

Vector emulator work can look faster while merely moving cost into worker
startup, synchronization, RAM collection, Python conversion, or CPU spinning.
Without structured timings, it is hard to tell whether a design improves
training throughput or just consumes more cores.

## Scope

- Add or extend benchmark-only instrumentation for future native vector
  emulator prototypes.
- Measure at least setup, controller/action transfer, native stepping,
  synchronization wait, RAM/info readback, observation access, and teardown.
- Include per-worker step time and wait time when worker threads exist.
- Keep instrumentation opt-in, benchmark-oriented, and cheap to disable.
- Treat CPU affinity as an experiment controlled by configuration, not default
  runtime behavior.
- Document platform differences for macOS, Linux, and Windows when relevant.
- Ensure the instrumentation can prove whether later vector changes improve
  frame rate significantly or merely shift time into synchronization overhead.

## Non-Goals

- Do not add always-on production logging.
- Do not make performance numbers CI pass/fail thresholds.
- Do not tune CPU affinity without evidence from the instrumentation.

## Benchmark Decision Rule

Instrumentation may land without increasing frame rate only if it is opt-in,
clearly simplifies performance diagnosis, and has no measurable cost when
disabled. Disabled instrumentation overhead must remain within 1% median
throughput of the baseline on scalar and representative vector benchmarks.

Any affinity, busy-wait, or synchronization tuning added under this spec must
meet the performance rule from the vector emulator spec: at least a 10% median
throughput gain for targeted vector workloads, or a documented simplification
with no representative regression. Otherwise keep the measurement capability
but reject the tuning change.

## Acceptance Criteria

- [ ] Benchmarks emit structured timing output that separates Python overhead,
  native frame stepping, synchronization, and RAM/info readback.
- [ ] Per-worker stats are available for threaded prototypes without data races
  or false sharing regressions.
- [ ] CPU affinity experiments can be enabled and disabled explicitly.
- [ ] Benchmark documentation explains how to interpret CPU usage and scaling
  across env counts.
- [ ] Benchmark reports include release build configuration, warmups, at least
  five measured runs, median throughput, min/max or IQR, percent change, and
  instrumentation-enabled versus instrumentation-disabled overhead.
- [ ] Any kept affinity or synchronization optimization has benchmark evidence
  showing significant frame-rate improvement, or is documented as a simpler
  no-regression implementation.
- [ ] Existing scalar emulator benchmarks remain available and unchanged.
- [ ] No generated benchmark artifacts are committed.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_speedtest
cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
git diff --check
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 0 -->

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

## Non-Goals

- Do not add always-on production logging.
- Do not make performance numbers CI pass/fail thresholds.
- Do not tune CPU affinity without evidence from the instrumentation.

## Acceptance Criteria

- [ ] Benchmarks emit structured timing output that separates Python overhead,
  native frame stepping, synchronization, and RAM/info readback.
- [ ] Per-worker stats are available for threaded prototypes without data races
  or false sharing regressions.
- [ ] CPU affinity experiments can be enabled and disabled explicitly.
- [ ] Benchmark documentation explains how to interpret CPU usage and scaling
  across env counts.
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

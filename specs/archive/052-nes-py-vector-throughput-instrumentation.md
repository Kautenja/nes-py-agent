# Specification: nes-py Vector Throughput Instrumentation

## Status: COMPLETE

## Source Inspiration

PR #90 added timing counters around vector `step(actions)`, per-worker timing
statistics, and several CPU-affinity experiments. The final PR head simplified
affinity to round-robin pinning, but the useful lesson is broader: native
parallel stepping needs first-class measurement before optimization decisions.

## Current Baseline

The project now has useful measurement pieces:

- `nes_py.speedtest` measures scalar stepping, render-heavy loops,
  backup/restore intervals, mapper profiles, and observation-consumption
  profiles.
- Native Catch2 benchmarks measure CPU, bus, mapper, and PPU hot paths.
- Recent scalar optimizations were accepted or rejected based on benchmark
  evidence, including an abandoned background palette-array experiment.

What is missing is a repeated-run vector/training-loop harness that reports
median and spread for scalar loops, Gymnasium vector baselines, possible native
vector implementations, observation copy modes, RAM/info collection, and worker
overheads.

## Problem

Vector emulator work can look faster while merely moving cost into worker
startup, synchronization, RAM collection, Python conversion, observation copy,
or CPU spinning. Without structured timings and repeated runs, it is hard to
tell whether a design improves total training throughput or just consumes more
cores.

## Scope

- Extend the existing benchmark tooling rather than creating an unrelated
  script when practical.
- Add repeated-run summaries for current scalar benchmarks and future vector
  profiles, including median and spread.
- Measure at least setup, controller/action transfer, native stepping,
  synchronization wait, RAM/info readback, observation access, Python wrapper
  overhead, and teardown for vector prototypes.
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
- Do not duplicate native Catch2 benchmarks that already isolate CPU, bus,
  mapper, and PPU hot paths.

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

- [ ] Benchmark tooling can run at least five repeated measurements and emit
  median, min/max or IQR, percent change, host metadata, build configuration,
  ROM, action policy, observation mode, wrapper/profile mode, warmup count, and
  measured step count.
- [ ] Benchmarks emit structured timing output that separates Python overhead,
  native frame stepping, synchronization, observation access, and RAM/info
  readback for vector prototypes.
- [ ] Per-worker stats are available for threaded prototypes without data races
  or false sharing regressions.
- [ ] CPU affinity experiments can be enabled and disabled explicitly.
- [ ] Benchmark documentation explains how to interpret CPU usage, power risk,
  oversubscription, and scaling across env counts.
- [ ] Benchmark reports include instrumentation-enabled versus
  instrumentation-disabled overhead.
- [ ] Any kept affinity or synchronization optimization has benchmark evidence
  showing significant frame-rate improvement, or is documented as a simpler
  no-regression implementation.
- [ ] Existing scalar, mapper, observation, and native benchmark entry points
  remain available and backward compatible.
- [ ] No generated benchmark artifacts are committed.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress
git diff --check
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 1 -->

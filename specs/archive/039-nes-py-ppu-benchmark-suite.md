# Specification: nes-py PPU Benchmark Suite

## Problem

The latest optimization round moved headless Mario stepping from roughly
`850` fps to roughly `1250-1300` fps, while synthetic render-disabled probes
showed the core can already exceed `2000` fps when the PPU does not compose a
visible frame. Further optimization needs a benchmark suite that isolates PPU
rendering modes before changing renderer internals.

The target is not a machine-specific pass/fail threshold. The target is a
repeatable profiler and report that can tell whether each experiment helps the
ML-training use case enough to keep.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Add native benchmark coverage under `nes_emu/benchmark/nes_emu/` or an
  equivalent native-only benchmark location.
- Keep public Python package APIs focused on supported `NESEnv` benchmarking;
  do not reintroduce C++ benchmark helpers through Cython.
- Create synthetic benchmark ROM/profile coverage for:
  - render-off stepping
  - background-only rendering
  - sprite-heavy rendering
  - mapper direct-read / CHR read stress
  - full-frame representative ROM profiles
- Include representative ROMs for mapper 0, mapper 1, mapper 2, and mapper 3
  when local fixtures are available.
- Document baseline results and how to run the benchmark suite.

## Non-Goals

- Do not optimize PPU, mapper, CPU, or observation code in this spec except for
  tiny benchmark-support fixes.
- Do not add or redistribute external ROM assets.
- Do not set hard fps thresholds that will fail on slower CI machines.

## Experiment Rule

This is a tooling spec. If a benchmark profile proves unstable or misleading,
remove or replace it before marking the spec complete. The deliverable is a
trustworthy baseline, not a favorable number.

## Acceptance Criteria

- [x] A native benchmark suite builds through the existing CMake benchmark
  target or a clearly documented equivalent target.
- [x] The suite includes render-off, background-only, sprite-heavy, mapper
  direct-read / CHR read stress, and full-frame ROM profiles.
- [x] The profiles are deterministic enough for before/after comparison on one
  machine.
- [x] The benchmark output includes enough labels to identify mapper, ROM or
  synthetic scenario, render mode, and measured throughput or elapsed time.
- [x] Baseline results are recorded in a developer note under `nes-py/docs/`.
- [x] The note includes current public `nes_py.speedtest` numbers for at least
  Mario and Zelda for comparison with the native profiles.
- [x] No generated benchmark output, build tree, cache, wheel, virtualenv, or
  profiling dump is committed.

## Status: COMPLETE

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress
git diff --check
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-ppu-benchmark-suite.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 1 -->

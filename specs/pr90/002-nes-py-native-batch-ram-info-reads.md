# Specification: nes-py Native Batch RAM Info Reads

## Source Inspiration

PR #90 added `configure_ram_reads` and `ram_values` to its `VectorEmulator`.
The intent was to read reward/info RAM addresses for all environments in C++
after each step rather than indexing RAM one byte at a time from Python.

## Current Baseline

The current branch already exposes `env.ram` as a zero-copy NumPy view and has
native observation-copy helpers for RGB and grayscale training loops. Wrapper
projects are now Gymnasium-compatible and should keep game-specific reward,
termination, and info logic in wrapper repositories.

Batch RAM reads are therefore useful only if profiling shows Python RAM
indexing is still a meaningful cost in representative wrapper-style loops after
the current scalar and observation fast paths.

## Problem

Game wrappers often compute rewards, termination, and info dictionaries from
multiple RAM addresses. Even with a zero-copy RAM buffer, Python can still
perform many small indexing operations per step and per environment. That cost
may become visible in vectorized training loops once frame stepping and
observation handling are fast enough.

## Scope

- Start with profiling before adding API surface.
- Work inside `nes-py` only for generic helpers; game-specific address lists
  and reward logic stay in the wrapper repos.
- Add a generic opt-in batch RAM read helper for one scalar emulator, a future
  vector emulator, or both only after profiling justifies it.
- Support simple byte reads and a minimal multi-byte encoding useful to wrappers
  such as BCD-style digit reads.
- Provide an optional reusable output buffer if the helper returns an array.
- Validate address ranges, read sizes, dtype, output shape, and behavior after
  reset/restore/close.
- Benchmark both isolated RAM-read loops and full `step + info` style loops so
  improvements are tied to frame-rate-relevant workloads.

## Non-Goals

- Do not move Super Mario Bros., Tetris, or Zelda reward logic into `nes-py`.
- Do not change the public `env.ram` zero-copy buffer.
- Do not add a complex expression language for reward computation.
- Do not replace the already-landed `NESEnv.observation(...)` copy helpers.
- Do not add native RAM reads if wrapper profiling shows RAM indexing is not a
  material bottleneck.

## Benchmark Decision Rule

The primary success metric is frames per second or steps per second in
wrapper-style loops that read multiple RAM addresses after each step. Keep a
native batch-read implementation only if it improves the targeted `step + info`
benchmark by at least 5% median throughput with no representative workload
regressing by more than 2%.

If the performance result is neutral, the change may still land only when it
substantially simplifies wrapper code or provides a clearer shared primitive
without measurable regression. If it adds API surface without speed or
simplicity, document the attempt and do not keep it.

## Acceptance Criteria

- [ ] Profiling first identifies at least one representative wrapper-style loop
  where RAM indexing or info collection is a measurable cost worth optimizing.
- [ ] A small API proposal documents how batch RAM reads are configured, how
  values are returned for scalar and vector use cases, and how game-specific
  wrappers should own address lists.
- [ ] Unit tests cover byte reads, multi-byte digit reads, invalid addresses,
  invalid sizes, empty specs, output reuse, reset behavior, restore behavior if
  applicable, and close behavior.
- [ ] Benchmarks compare current Python indexing, NumPy vectorized indexing
  where practical, and native batch reads for representative wrapper-style
  address sets.
- [ ] Benchmark reports include warmup count, measured iterations, at least
  five runs, median throughput, min/max or IQR, percent change, ROM, action
  policy, wrapper or synthetic address set, and observation mode used.
- [ ] The completion note explicitly states whether the implementation was kept
  for significant frame-rate improvement, kept for simplicity with no
  regression, or rejected.
- [ ] The implementation avoids extra copies in the steady-state path unless a
  copy is explicitly documented.
- [ ] Existing `NESEnv.ram`, `NESEnv.observation`, backup, restore, and scalar
  step behavior remains unchanged.
- [ ] Existing Python environment, wrapper, mapper, and speedtest tests pass.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress
git diff --check
```

If native C++ helpers are added, also run the native test target. If wrapper
repos consume the helper, run the focused wrapper tests and record them in the
completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 0 -->

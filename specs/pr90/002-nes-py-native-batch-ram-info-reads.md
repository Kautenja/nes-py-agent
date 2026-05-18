# Specification: nes-py Native Batch RAM Info Reads

## Source Inspiration

PR #90 added `configure_ram_reads` and `ram_values` to its `VectorEmulator`.
The intent was to read reward/info RAM addresses for all environments in C++
after each step rather than indexing RAM one byte at a time from Python.

## Problem

Game wrappers often compute rewards, termination, and info dictionaries from
multiple RAM addresses. Even though the current RAM buffer is zero-copy, Python
still performs many small indexing operations per step and per environment.
That overhead can matter in vectorized training loops once native frame stepping
gets faster.

## Scope

- Work inside `nes-py` first; wrapper integration is optional and should happen
  only after generic API value is proven.
- Add a generic opt-in batch RAM read helper for one scalar emulator, a future
  vector emulator, or both.
- Support simple byte reads and a minimal multi-byte encoding useful to wrappers
  such as BCD-style digit reads.
- Validate address ranges, read sizes, dtype, output shape, and behavior after
  reset/restore/close.
- Keep game-specific address lists outside of `nes-py` unless they are test
  fixtures.
- Benchmark Python RAM indexing loops against native batch reads.
- Benchmark both isolated RAM-read loops and full `step + info` style loops so
  improvements are tied to frame-rate-relevant workloads.

## Non-Goals

- Do not move Super Mario Bros., Tetris, or Zelda reward logic into `nes-py`.
- Do not change the public `env.ram` zero-copy buffer.
- Do not add a complex expression language for reward computation.

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

- [ ] A small API proposal documents how batch RAM reads are configured and how
  values are returned for scalar and vector use cases.
- [ ] Unit tests cover byte reads, multi-byte digit reads, invalid addresses,
  invalid sizes, empty specs, reset behavior, restore behavior if applicable,
  and close behavior.
- [ ] Benchmarks compare current Python indexing with native batch reads for
  representative wrapper-style address sets.
- [ ] Benchmark reports include warmup count, measured iterations, at least
  five runs, median throughput, min/max or IQR, percent change, ROM, action
  policy, and the RAM address set used.
- [ ] The completion note explicitly states whether the implementation was kept
  for significant frame-rate improvement, kept for simplicity with no
  regression, or rejected.
- [ ] The implementation avoids extra copies in the steady-state path unless a
  copy is explicitly documented.
- [ ] Existing `NESEnv.ram` behavior remains unchanged.
- [ ] Existing Python environment, wrapper, mapper, and speedtest tests pass.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
git diff --check
```

If native C++ helpers are added, also run the native test target. Record exact
benchmark commands and before/after results in a developer note or completion
log before closing the spec.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 0 -->

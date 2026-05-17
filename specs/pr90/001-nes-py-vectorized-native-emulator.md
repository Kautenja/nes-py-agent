# Specification: nes-py Vectorized Native Emulator

## Source Inspiration

PR #90 added a `VectorEmulator` pybind11 class that owns multiple emulator
instances, persistent worker threads, zero-copy screen/RAM views, parallel
`step(actions)`, single-env reset/step helpers, and GIL release during native
stepping.

The code cannot be merged as-is because the current branch uses the Cython
binding in `nes_py/_native.pyx`, the `nes_emu/` native layout, CMake, and a
newer mapper ownership model. The architecture is still worth exploring.

## Problem

RL training often runs many NES environments at once. The current `NESEnv`
API is optimized for one environment per Python object, so multi-env training
typically pays Python dispatch, wrapper, RAM inspection, and scheduler overhead
per environment.

A current-branch native vector stepping API may improve throughput by batching
controller writes and native frame advances while preserving zero-copy
observations.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Design against the current `nes_emu` C++ layout and Cython binding, not the
  pybind11 implementation from PR #90.
- Prototype an opt-in native vector emulator that owns N emulator instances for
  the same ROM.
- Provide an explicit Python API for batched `reset`, `reset_one`,
  `step(actions)`, screen buffers, RAM buffers, and close/teardown.
- Preserve the existing scalar `NESEnv` API and behavior.
- Release the GIL while native workers step.
- Benchmark against a Python loop of N `NESEnv` instances and at least one
  Gymnasium vector environment baseline.

## Non-Goals

- Do not rewrite all wrappers to use the vector API in this spec.
- Do not make busy-wait synchronization or CPU affinity the default without
  evidence.
- Do not expose game-specific reward or info logic from `nes-py`.

## Acceptance Criteria

- [ ] A design note explains the chosen native/Cython ownership model, buffer
  lifetime rules, worker teardown semantics, and interaction with mapper
  snapshots.
- [ ] Prototype tests cover vector construction, close, reset all, reset one,
  step with per-env actions, invalid action array shape/type, invalid env
  index, and buffer lifetime after close.
- [ ] Determinism tests show a vector env stepped with fixed actions matches N
  scalar `NESEnv` instances for screen and RAM state on supported mapper
  fixtures.
- [ ] Benchmarks report throughput for scalar Python loops, Gymnasium vector
  baselines, and the native vector prototype across at least 1, 2, 4, 8, and
  16 envs where hardware allows.
- [ ] Any kept synchronization strategy has documented CPU usage and scaling
  behavior.
- [ ] Existing scalar Python environment, mapper, native, and speedtest tests
  pass.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
cmake --build build/nes-emu-release --config Release --target nes_emu_tests
build/nes-emu-release/nes_emu_tests
git diff --check
```

If the vector API adds new benchmark commands, record the exact commands and
results in a developer note before closing the spec.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 0 -->

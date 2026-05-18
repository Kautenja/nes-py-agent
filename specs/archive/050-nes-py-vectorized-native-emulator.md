# Specification: nes-py Vectorized Native Emulator

## Status: COMPLETE

## Source Inspiration

PR #90 added a `VectorEmulator` pybind11 class that owns multiple emulator
instances, persistent worker threads, zero-copy screen/RAM views, parallel
`step(actions)`, single-env reset/step helpers, and GIL release during native
stepping.

The code cannot be merged as-is because the current branch uses the Cython
binding in `nes_py/_native.pyx`, the `nes_emu/` native layout, CMake, current
mapper ownership, mapper direct-read caches, native observation helpers, and
instruction-batched scalar stepping.

## Current Baseline

Recent project updates changed what a useful vector emulator must prove:

- `NES::Emulator::step()` is already instruction-batched for mappers without
  CPU-cycle hooks.
- PPU sprite/background caches and mapper direct-read pages have already lifted
  scalar frame rates substantially.
- `NESEnv.observation("rgb_array_contiguous")` and
  `NESEnv.observation("grayscale")` already provide reusable native copy paths.
- `nes_py.speedtest` now has scalar, mapper, and observation benchmark profiles,
  but not a repeated-run vector profile.

The vector API must therefore beat current scalar loops and Gymnasium vector
baselines, not the older PR #90-era scalar implementation.

## Problem

RL training often runs many NES environments at once. The current `NESEnv` API
is optimized for one environment per Python object, so multi-env training may
still pay Python dispatch, wrapper, observation selection, RAM inspection, and
scheduler overhead per environment.

A current-branch native vector stepping API may improve total frames per second
by batching controller writes, native frame advances, observation copies, and
possibly wrapper-facing RAM collection while preserving deterministic scalar
emulator behavior.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Design against the current `nes_emu` C++ layout and Cython binding, not the
  pybind11 implementation from PR #90.
- Prototype an opt-in native vector emulator that owns N emulator instances for
  the same ROM.
- Reuse the current `NES::Emulator` stepping path so instruction batching,
  mapper CPU-cycle hook gating, PPU caches, mapper direct-read caches, backup,
  restore, and screen/RAM buffers stay consistent with scalar `NESEnv`.
- Provide an explicit Python API for batched `reset`, `reset_one`,
  `step(actions)`, close/teardown, screen views, RAM views, and current
  observation copy modes where useful.
- Preserve the existing scalar `NESEnv` API and behavior.
- Release the GIL while native workers step.
- Benchmark against a Python loop of N `NESEnv` instances, Gymnasium
  `SyncVectorEnv`, Gymnasium `AsyncVectorEnv` when available, and the native
  vector prototype.
- Benchmark release builds with warmups and at least five measured runs per env
  count so medians and run-to-run spread are visible.

## Non-Goals

- Do not rewrite all wrappers to use the vector API in this spec.
- Do not duplicate the already-landed scalar observation-copy helpers.
- Do not make busy-wait synchronization or CPU affinity the default without
  evidence.
- Do not expose game-specific reward or info logic from `nes-py`.
- Do not change scalar `NESEnv.step`, `render`, `observation`, `_backup`, or
  `_restore` semantics.

## Benchmark Decision Rule

The primary success metric is total frames per second across all environments
for realistic training loops on the current optimized scalar baseline. A vector
implementation should be kept only if it shows at least a 10% median
throughput improvement at 4 or more environments, or at least a 15% improvement
at the highest tested env count, while avoiding more than a 2% median
regression for 1-env scalar-style use.

If the throughput difference is within noise, the work may still land only when
the final code is simpler than the existing multi-env approach for users and
the benchmark report shows no meaningful representative regression. Otherwise,
leave the prototype documented and do not keep the implementation.

## Acceptance Criteria

- [ ] A design note explains the chosen native/Cython ownership model, buffer
  lifetime rules, worker teardown semantics, mapper snapshot interaction,
  observation-mode handling, and whether workers are persistent or pooled.
- [ ] Prototype tests cover vector construction, close, reset all, reset one,
  step with per-env actions, invalid action array shape/type, invalid env
  index, buffer lifetime after close, and exceptions during construction.
- [ ] Determinism tests show vector envs stepped with fixed actions match N
  scalar `NESEnv` instances for screen and RAM state across representative
  mapper fixtures, including mappers with CPU-cycle hooks that must keep the
  scalar cycle-by-cycle path.
- [ ] Benchmarks report throughput for scalar Python loops, Gymnasium vector
  baselines, and the native vector prototype across at least 1, 2, 4, 8, and
  16 envs where hardware allows.
- [ ] Benchmarks include step-only, native contiguous RGB observation,
  native grayscale observation, and wrapper-like RAM/info consumption profiles.
- [ ] Benchmarks include median, min/max or IQR, build configuration, ROM,
  action policy, warmup count, measured step count, env counts, and CPU usage
  notes for any worker-thread implementation.
- [ ] The completion note explicitly states whether the implementation was kept
  because it significantly improved frame rate, because it simplified the API
  without regression, or because it was rejected.
- [ ] Any kept synchronization strategy has documented CPU usage,
  oversubscription behavior, fairness, and teardown behavior.
- [ ] Existing scalar Python environment, observation, mapper, native, and
  speedtest tests pass.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks
build/nes-emu-release/nes_emu_tests
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress
git diff --check
```

If the vector API adds new benchmark commands, record the exact commands and
results in a developer note before closing the spec. Include the baseline and
changed medians, spread, percent change, and the decision under the benchmark
rule above.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required completion log.
- Output `DONE` only after verification passes.

<!-- NR_OF_TRIES: 1 -->

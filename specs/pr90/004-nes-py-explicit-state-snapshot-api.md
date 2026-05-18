# Specification: nes-py Explicit State Snapshot API

## Source Inspiration

PR #90 exposed `dump_state()` and `load_state(snapshot)` returning snapshots as
NumPy arrays, and used snapshots to support restore flows outside a single
internal backup slot.

## Current Baseline

The current branch already has native backup/restore support built around
mapper-owned clones, explicit `MainBus` and `PictureBus` state, `CPU` copies,
and `PPU::Snapshot`. CPU instruction batching also added native CPU snapshot
coverage for deterministic old/new frame comparisons.

That means PR #90's raw `Core` struct copying is not safe or appropriate for
the current architecture. A new snapshot API should exist only if it improves
vector reset/branching workflows, simplifies state management, or measurably
improves backup/restore-heavy throughput.

## Problem

An explicit snapshot API could help vectorized training workflows, branching
rollouts, reset-to-checkpoint loops, and debugging. It may also make native
vector reset and per-env restore semantics easier to express without exposing
private backup slots.

The current mapper model uses owned mapper snapshots and callback rewiring, so
any exported snapshot representation must be opaque and architecture-aware.

## Scope

- Design a current-branch snapshot representation that respects mapper
  ownership, callback rewiring, PPU state, bus state, CPU state, CHR RAM, PRG
  RAM, direct-read cache refresh, instruction-batching state, and screen buffer
  state.
- Decide whether snapshots are public API, private vector-emulator plumbing, or
  both. Prefer private plumbing unless a public use case is compelling.
- Prefer an opaque Python object or bytes-like container over exposing native
  pointers, raw implementation structs, or NumPy views of native internals.
- Preserve existing `_backup()` and `_restore()` behavior.
- Test snapshots across the currently supported mapper set.
- Benchmark snapshot creation, restore, and backup/restore-heavy frame loops
  against the current private backup path.

## Non-Goals

- Do not serialize snapshots as a stable cross-version save-state format unless
  that is explicitly accepted as API scope.
- Do not expose raw native pointers to Python.
- Do not make snapshots game-wrapper-specific.
- Do not replace `_backup()` and `_restore()` unless the replacement is simpler
  and benchmark-neutral or faster.
- Do not add public snapshot API solely because PR #90 had one.

## Benchmark Decision Rule

Snapshot work should maximize frame rate for reset, restore, branching, and
vector rollout workflows. A new public or native snapshot path should be kept
as a performance optimization only if backup/restore-heavy frame-loop
benchmarks improve by at least 5% median throughput, or if snapshot create and
restore latency improves by at least 10% without slowing normal `step` loops by
more than 2%.

If performance is neutral, the change may still land only when it clearly
simplifies state management, vector reset plumbing, or user-facing checkpoint
semantics while benchmark results show no meaningful regression. Raw struct
copying or extra API complexity should not be kept without one of those
benefits.

## Acceptance Criteria

- [ ] A design note documents snapshot lifetime, compatibility guarantees,
  mapper state handling, callback rewiring, direct-read cache refresh, and
  whether the API is public or private.
- [ ] Tests show snapshot round-trips restore screen, RAM, controller-relevant
  state, CPU/PPU progress, mapper PRG/CHR bank state, mirroring state, and
  instruction-batching continuation behavior.
- [ ] Tests cover at least mappers 0, 1, 2, 3, 4, 5, 7, 9, and 69 using the
  existing fixture strategy.
- [ ] Invalid snapshot inputs raise clear Python exceptions if any public or
  Python-visible API is added.
- [ ] Existing `_backup()` and `_restore()` tests continue to pass.
- [ ] Benchmarks measure normal step-only throughput, current private
  backup/restore throughput, snapshot creation latency, restore latency,
  backup/restore-heavy loop throughput, warmups, at least five measured runs,
  median, min/max or IQR, and percent change.
- [ ] The completion note explicitly states whether the snapshot API was kept
  for significant performance improvement, kept for simpler state management
  with no regression, kept only as private vector plumbing, or rejected.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_mappers
.venv/bin/python -m unittest discover .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks
build/nes-emu-release/nes_emu_tests
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --backup-interval 50 --restore-interval 70 --json --no-progress
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

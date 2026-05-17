# Specification: nes-py Explicit State Snapshot API

## Source Inspiration

PR #90 exposed `dump_state()` and `load_state(snapshot)` returning snapshots as
NumPy arrays, and used snapshots to support restore flows outside a single
internal backup slot.

The current branch already has native backup/restore support with mapper-owned
state, but it does not expose a portable public snapshot object.

## Problem

An explicit snapshot API could help vectorized training workflows, branching
rollouts, reset-to-checkpoint loops, and debugging. It may also make native
vector reset and per-env restore semantics easier to express without exposing
private backup slots.

The current mapper model uses owned mapper snapshots and callbacks, so raw
struct copying from PR #90 is not safe to copy directly.

## Scope

- Design a current-branch snapshot representation that respects mapper
  ownership, callback rewiring, PPU state, bus state, CPU state, CHR RAM, PRG
  RAM, and screen buffer state.
- Decide whether snapshots are public API, private vector-emulator plumbing, or
  both.
- Prefer an opaque Python object or bytes-like container over exposing native
  pointers or raw implementation structs.
- Preserve existing `_backup()` and `_restore()` behavior.
- Test snapshots across the currently supported mapper set.

## Non-Goals

- Do not serialize snapshots as a stable cross-version save-state format unless
  that is explicitly accepted as API scope.
- Do not expose raw native pointers to Python.
- Do not make snapshots game-wrapper-specific.

## Acceptance Criteria

- [ ] A design note documents snapshot lifetime, compatibility guarantees,
  mapper state handling, and callback rewiring.
- [ ] Tests show snapshot round-trips restore screen, RAM, controller-relevant
  state, CPU/PPU progress, mapper PRG/CHR bank state, and mirroring state.
- [ ] Tests cover at least mappers 0, 1, 2, 3, 4, 5, 7, 9, and 69 using the
  existing fixture strategy.
- [ ] Invalid snapshot inputs raise clear Python exceptions.
- [ ] Existing `_backup()` and `_restore()` tests continue to pass.
- [ ] Benchmarks measure snapshot creation and restore overhead against the
  current private backup path.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.mappers
.venv/bin/python -m unittest discover .
cmake --build build/nes-emu-release --config Release --target nes_emu_tests
build/nes-emu-release/nes_emu_tests
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

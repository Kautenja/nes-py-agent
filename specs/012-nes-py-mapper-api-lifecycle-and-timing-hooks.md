# Specification: nes-py Mapper API Lifecycle and Timing Hooks

## Problem

The current native mapper API is not ready for the mapper specs. Many planned mappers need timing-sensitive callbacks, IRQ signaling, PPU read side effects, expansion register routing, nametable banking, and stateful backup/restore. The emulator also allocates mappers with raw pointers and copies buses that hold mapper pointers, so mapper lifetime and snapshot behavior are fragile.

This spec prepares the native emulator architecture for mapper implementations without landing a large batch of new mappers at the same time.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Refactor mapper ownership so the emulator owns the active mapper safely.
- Ensure backup/restore captures mapper state and restores bus/picture-bus mapper references correctly.
- Separate mutable emulator state from fixed device wiring so backup/restore snapshots RAM, registers, mapper state, and PPU state without copying callback maps or stale pointers.
- Add mapper extension points for CPU/PPU timing, IRQs, expansion registers, nametable mapping, and PRG RAM behavior.
- Keep mappers 0-3 behavior-compatible after the refactor.
- Add tests using existing mappers and small test/fake mappers to prove the extension points work.

## Required Native Capabilities

The new mapper-facing API should support:

- mapper-owned state snapshot/clone or equivalent deterministic backup/restore;
- CPU IRQ requests from mapper logic into the CPU IRQ path;
- per-CPU-cycle or per-instruction hooks where a mapper requires CPU-cycle counters;
- PPU address/read hooks for MMC3 A12 IRQ detection and MMC2/MMC4 CHR latch behavior;
- mapper handling for `$4020-$5FFF` expansion-area reads and writes;
- mapper handling for `$6000-$7FFF` PRG RAM, write protection, open bus defaults, and banked RAM;
- nametable mapping hooks for mapper-provided CIRAM selection, nametable RAM, nametable ROM, and four-screen RAM;
- explicit mirroring updates without each mapper needing ad hoc callbacks;
- read/write helpers that can model bus conflicts where needed.

## Non-Goals

- Do not implement MMC3, MMC5, VRC, Sunsoft, Namco, Taito, Bandai, or multicart mappers in this spec.
- Do not add audio output or expansion audio mixing in this spec.
- Do not change the Python public API except where needed to keep tests passing.

## Acceptance Criteria

- [ ] The emulator owns mapper instances using RAII, not unmanaged raw `new` without a matching owner.
- [ ] Mapper creation is moved out of a header-defined global function if needed to avoid ODR/linkage issues as mapper count grows.
- [ ] `MapperFactory` registration is easy to extend and can represent mapper IDs from all current mapper specs.
- [ ] Backup/restore saves and restores mapper state, not just CPU, PPU, and bus state.
- [ ] Backed-up and restored buses point to the restored active mapper, not a stale or current-state mapper by accident.
- [ ] Backup/restore does not copy fixed wiring such as callback maps, lambda captures, or device pointers when a smaller state object would be sufficient.
- [ ] A mapper can request a CPU IRQ, and a focused test proves the CPU observes it through the existing IRQ vector path.
- [ ] A mapper can observe PPU pattern-table reads or address transitions sufficiently for MMC3 A12 and MMC2/MMC4 latch follow-up specs.
- [ ] A mapper can handle expansion-area reads/writes in `$4020-$5FFF` without logging them as globally unsupported.
- [ ] A mapper can handle PRG RAM reads/writes, write protection, and banked RAM in `$6000-$7FFF`.
- [ ] The picture bus can delegate nametable reads/writes to a mapper when the mapper owns nametable memory or ROM banking.
- [ ] Mappers 0-3 continue to pass the characterization tests from spec 010.
- [ ] The tiny benchmark profile from spec 010 is run before and after the refactor, and any measurable slowdown is documented with a follow-up optimization note or fixed in this spec.
- [ ] No external ROM assets, generated binaries, wheels, caches, or local virtual environments are committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_nes_env
python -m unittest discover .
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 20 --json --no-progress
```

If native C++ tests are added for fake mapper hooks, run the documented native test command for the active build system.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-api-lifecycle-and-timing-hooks.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

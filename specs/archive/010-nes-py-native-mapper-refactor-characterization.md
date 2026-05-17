# Specification: nes-py Native Mapper Refactor Characterization

## Status: COMPLETE

## Problem

The mapper queue in `specs/mappers/` now reaches far beyond the current `nes-py` native mapper surface. The C++ code supports mappers 0-3 through a narrow `Mapper` interface, while future specs require IRQ counters, scanline-sensitive behavior, CHR latches, nametable ROM/RAM banking, PRG RAM protection, bus conflicts, expansion register ranges, NES 2.0/submapper metadata, multicart variants, and mapper state that survives backup/restore correctly.

Before changing the native emulator architecture, the current behavior needs a characterization suite and benchmark baseline. Without that safety net, broad mapper and binding refactors can silently break the four currently supported mappers or make performance worse without a clear before/after comparison.

## Current Findings

- `Mapper` only exposes PRG/CHR read-write methods plus mirroring; it has no timing hooks, IRQ line, nametable mapping hook, expansion-bus hook, or explicit state snapshot/clone API.
- `MapperFactory` returns raw pointers and the emulator does not own or back up mapper state explicitly. This is risky for mapper 1 already and will be incorrect for complex bank-switching mappers.
- `Cartridge` parses only the minimal iNES fields needed by mappers 0-3 and relies on Python validation before native initialization.
- PRG RAM is treated as `has_extended_ram` from header flag 6 bit 1, which conflates battery-backed RAM with PRG RAM presence and size.
- The C++ path does not have focused native mapper tests. Current tests mostly exercise Python environment behavior and ROM header parsing.
- The packaged benchmark from spec 006 gives a useful CLI/API starting point, but native refactors need a repeatable baseline across mapper families and binding paths.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Add focused characterization tests for all currently supported mapper families: NROM, SxROM/MMC1, UxROM, and CNROM.
- Add tests that prove backup/restore includes mapper-observable state for current mappers, especially bank-select state after PRG/CHR writes.
- Add synthetic ROM/header helpers for mapper tests without adding external ROM assets.
- Add a benchmark profile that records baseline throughput for `reset`, `step`, `render('rgb_array')`, backup/restore, and supported mapper fixtures.
- Document the native capability gaps that block the mapper specs and link this spec to follow-up implementation specs.

## Non-Goals

- Do not implement new mappers in this spec.
- Do not migrate bindings to Cython in this spec.
- Do not require fixed throughput numbers as pass/fail criteria.

## Acceptance Criteria

- [x] A mapper-focused test module exists in `nes-py` and runs through `python -m unittest`.
- [x] Tests identify mapper 0, 1, 2, and 3 from known fixtures or synthetic ROMs and assert expected PRG size, CHR size, CHR RAM/ROM mode, and mirroring.
- [x] Mapper 0 tests cover fixed PRG mapping, 16 KiB mirroring behavior, CHR ROM reads, and reset/step/render smoke behavior.
- [x] Mapper 1 tests cover serial register writes, PRG bank switching, CHR RAM persistence, switchable mirroring, and backup/restore determinism after mapper state changes.
- [x] Mapper 2 tests cover switchable 16 KiB PRG banking at `$8000`, fixed final bank at `$C000`, CHR RAM reads/writes, and documented bus-conflict assumptions.
- [x] Mapper 3 tests cover fixed PRG mapping, switchable 8 KiB CHR ROM banking, and screen stability across bank changes.
- [x] Tests fail on the current known mapper-state backup/restore weakness unless the implementation fixes it in the same spec.
- [x] The benchmark API or CLI can run a small current-mapper benchmark profile and emit structured JSON with environment, compiler/platform, mapper, operation, elapsed time, and steps-per-second fields.
- [x] Benchmark checks assert shape and positivity of results but do not assert machine-specific throughput.
- [x] A short developer note lists the native mapper capability gaps discovered from `specs/mappers/` and points to the follow-up specs.
- [x] No external ROM assets, generated binaries, wheels, caches, or local virtual environments are committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_rom
python -m unittest nes_py.tests.test_nes_env
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_speedtest
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 50 --warmup-steps 10 --json --no-progress
```

If a new benchmark subcommand or profile file is added, run it against at least one mapper 0 fixture and one mapper 1 fixture with a tiny step count suitable for CI.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-native-mapper-refactor-characterization.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

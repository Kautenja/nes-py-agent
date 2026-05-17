# Specification: nes-py Mapper Bank Helpers and Current Mapper Cleanup

## Problem

The existing mapper implementations duplicate bank math and leave several current-functionality risks in place. Mappers 0-3 work for the narrow fixtures, but future mapper specs will multiply the same patterns: fixed/switchable PRG windows, CHR ROM/RAM windows, mirroring changes, bus conflicts, bank masks, PRG RAM behavior, and variant-specific register decoding.

This spec adds shared mapper helpers and cleans up the currently supported mappers before new mapper implementations depend on the old ad hoc structure.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Add small native helper types/functions for PRG/CHR bank windows, RAM-backed CHR, fixed final banks, bus-conflict write values, and safe bank masking.
- Refactor NROM, SxROM/MMC1, UxROM, and CNROM to use those helpers where it reduces duplication or fixes correctness risks.
- Fix current mapper issues discovered by characterization tests, especially mapper-state backup/restore and PRG RAM handling.
- Keep public Python behavior compatible.

## Current Cleanup Targets

- Replace unchecked bank indexing with helper paths that mask or validate bank numbers according to mapper rules.
- Separate CHR RAM ownership from individual mapper one-offs where practical.
- Make SxROM/MMC1 PRG RAM behavior explicit rather than leaving it as a TODO.
- Fix or prove SxROM/MMC1 8 KiB CHR bank selection, where the low bit should be ignored for the 8 KiB bank base rather than accidentally selecting the odd 4 KiB page as the first half.
- Document or implement UxROM bus-conflict behavior consistently.
- Document or implement CNROM bus-conflict behavior consistently.
- Avoid hot-path logging or string work in normal mapper reads/writes.
- Keep mapper helper abstractions small enough that one-off pirate/multicart mappers can opt out when sharing would be misleading.

## Non-Goals

- Do not implement new mapper IDs in this spec.
- Do not introduce a large inheritance hierarchy for every future mapper.
- Do not change ROM fixture policy or add external ROM assets.

## Acceptance Criteria

- [ ] Shared bank helper code exists with focused tests for 8 KiB, 16 KiB, and 32 KiB PRG windows; 1 KiB, 2 KiB, 4 KiB, and 8 KiB CHR windows where useful; fixed first/final banks; and masked bank selection.
- [ ] Current mapper implementations use the helpers where they reduce duplicated or fragile pointer arithmetic.
- [ ] Mapper 0 behavior remains unchanged for NROM-128 and NROM-256 style layouts.
- [ ] Mapper 1 behavior covers serial register reset, control register mirroring modes, PRG bank modes, CHR RAM, and PRG RAM enable/protect behavior needed by existing fixtures.
- [ ] Mapper 1 tests cover 4 KiB and 8 KiB CHR banking math with low-bit masking in 8 KiB mode.
- [ ] Mapper 2 behavior masks bank selection safely and documents or tests bus-conflict assumptions.
- [ ] Mapper 3 behavior masks CHR bank selection safely and documents or tests bus-conflict assumptions.
- [ ] Characterization tests from spec 010 pass without loosening assertions.
- [ ] A small benchmark comparison is recorded before/after the helper refactor, and any performance regression over an agreed noise threshold is investigated or documented.
- [ ] Code comments replace vague TODOs in touched mapper files with specific behavior notes or issue/spec references.
- [ ] No generated binaries, wheels, caches, or local virtual environments are committed.
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
python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 100 --warmup-steps 20 --json --no-progress
```

If native C++ tests are added for bank helpers, run the documented native test command for the active build system.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-bank-helpers-and-current-mapper-cleanup.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

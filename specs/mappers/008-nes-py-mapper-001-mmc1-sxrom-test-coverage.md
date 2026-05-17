# Specification: nes-py Mapper 1 MMC1 SxROM Test Coverage

## Problem

Mapper 1 (MMC1 / SxROM) is already implemented in `nes-py`, and recent mapper characterization work now covers its synthetic ROM behavior. This spec now tracks any remaining representative-fixture alignment for `The Legend of Zelda (USA)` without duplicating the mapper-focused synthetic coverage already added by the archived mapper cleanup specs. The local fixture target is `nes_py/tests/games/the-legend-of-zelda.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/the-legend-of-zelda.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Do not change mapper behavior except to fix a real regression exposed by focused tests.
- Reuse or reference existing `nes_py.tests.test_mappers.ShouldCharacterizeMapper001SxROM`, ROM header, and environment tests where they already satisfy this spec.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Current Baseline

- `nes_py.tests.test_mappers.ShouldCharacterizeMapper001SxROM` covers serial register writes, serial reset behavior, PRG bank modes, CHR ROM/RAM behavior, control-register mirroring modes, PRG RAM protect bits, and backup/restore of mapper state.
- `nes_py.tests.test_mappers.ShouldIdentifySupportedMapperFixtures` covers mapper 1 native metadata through synthetic fixtures.
- `nes_py.tests.test_rom.ShouldReadLegendOfZelda` covers the committed representative fixture header.

## Mapper Details

- Mapper ID: `1` / iNES `001`
- Mapper name: `MMC1 / SxROM`
- Hardware family: `Nintendo MMC1 serial mapper`
- Approximate entries in `nesmapper.txt`: `449`
- Representative test title: `The Legend of Zelda (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Legend_of_Zelda%2C_The_%28USA%29/56074
- Expected local fixture: `nes_py/tests/games/the-legend-of-zelda.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: serial register writes, PRG banking, CHR RAM, battery-backed PRG RAM, switchable mirroring, save/restore determinism.

## Acceptance Criteria

- [ ] Current synthetic mapper 1 characterization remains green and is not duplicated unnecessarily.
- [ ] Representative fixture header coverage is kept or explicitly referenced from the mapper tests or completion log.
- [ ] Representative fixture `NESEnv` reset, deterministic-step, and `rgb_array` rendering coverage is added or explicitly referenced from an existing test.
- [ ] Mapper 1 backup/restore coverage proves bank registers, CHR RAM, mirroring, and PRG RAM protect state survive emulator save-state operations.
- [ ] Tests cover the mapper-specific behavior listed in this spec's focus section, using observable emulator state or a focused mapper/unit harness.
- [ ] The test module or mapper spec explains how to provide the representative ROM legally and never fetches it from the network.
- [ ] Missing fixture skips are narrow and explicit; they do not hide mapper header/unit tests that can run without the commercial ROM.
- [ ] Existing mapper tests still pass after this spec lands.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, local virtual environments, and commercial ROM downloads are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_rom.ShouldReadLegendOfZelda
```

If the representative commercial fixture is absent, the implementer must also run any mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-001-mmc1-sxrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

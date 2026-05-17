# Specification: nes-py Mapper 3 CNROM Test Coverage

## Problem

Mapper 3 (CNROM) is already implemented in `nes-py`, and recent mapper characterization work now covers its core synthetic ROM behavior. This spec now tracks the remaining mapper 3 coverage gaps, especially representative-fixture alignment for `Adventure Island (USA)` and explicit save-state coverage for switchable CHR bank state. The local fixture target is `nes_py/tests/games/adventure-island.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/adventure-island.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Do not change mapper behavior except to fix a real regression exposed by focused tests.
- Reuse or reference existing `nes_py.tests.test_mappers.ShouldCharacterizeMapper003CNROM`, ROM header, and environment tests where they already satisfy this spec.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Current Baseline

- `nes_py.tests.test_mappers.ShouldCharacterizeMapper003CNROM` covers fixed PRG mapping, switchable 8 KiB CHR ROM banking, screen validity/stability across CHR bank changes, and safe CHR bank masking.
- `nes_py.tests.test_mappers.ShouldIdentifySupportedMapperFixtures` covers mapper 3 native metadata through synthetic fixtures.
- Explicit mapper 3 backup/restore coverage for the selected CHR bank is still needed.

## Mapper Details

- Mapper ID: `3` / iNES `003`
- Mapper name: `CNROM`
- Hardware family: `CNROM discrete CHR bank switching`
- Approximate entries in `nesmapper.txt`: `122`
- Representative test title: `Adventure Island (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Hudson's_Adventure_Island_(USA)/55793
- Expected local fixture: `nes_py/tests/games/adventure-island.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: fixed PRG mapping, switchable 8 KiB CHR ROM bank, mirroring, screen stability across CHR bank changes.

## Acceptance Criteria

- [ ] Current synthetic mapper 3 characterization remains green and is not duplicated unnecessarily.
- [ ] Representative fixture header coverage is added when a legal fixture is available, or the mapper-level synthetic coverage remains runnable without the commercial ROM.
- [ ] Representative fixture `NESEnv` reset, deterministic-step, and `rgb_array` rendering coverage is added when a legal fixture is available.
- [ ] Mapper 3 backup/restore coverage proves the selected CHR bank survives emulator save-state operations.
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
```

If the representative commercial fixture is absent, the implementer must also run any mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-003-cnrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

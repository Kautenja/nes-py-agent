# Specification: nes-py Mapper 0 NROM Test Coverage

## Problem

Mapper 0 (NROM) is already implemented in `nes-py`, but the test suite does not have mapper-focused coverage that proves representative cartridge behavior remains stable. The representative title for this spec is `Super Mario Bros. (USA)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/super-mario-bros-1.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/super-mario-bros-1.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Do not change mapper behavior except to add focused tests and small test helpers.
- Keep the current mapper factory registration unchanged unless a test exposes a real bug.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `0` / iNES `000`
- Mapper name: `NROM`
- Hardware family: `No mapper / NROM`
- Approximate entries in `nesmapper.txt`: `149`
- Representative test title: `Super Mario Bros. (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Super_Mario_Bros._%28Japan%2C_USA%29/57098
- Expected local fixture: `nes_py/tests/games/super-mario-bros-1.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: fixed PRG mapping, 16 KiB mirroring behavior, CHR ROM reads, nametable mirroring, reset/step/render smoke coverage.

## Acceptance Criteria

- [ ] Tests identify mapper 0 from the fixture header and assert the expected PRG/CHR sizes and mirroring mode.
- [ ] Tests instantiate `NESEnv` with the representative fixture and run reset, several deterministic steps, and `rgb_array` rendering.
- [ ] Tests include backup/restore coverage for the mapper so mapper state survives emulator save-state operations.
- [ ] Tests cover the mapper-specific behavior listed in this spec's focus section, using observable emulator state or a focused mapper/unit harness.
- [ ] The test module explains how to provide the representative ROM legally and never fetches it from the network.
- [ ] Missing fixture skips are narrow and explicit; they do not hide mapper header/unit tests that can run without the commercial ROM.
- [ ] Existing mapper tests still pass after this spec lands.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, local virtual environments, and commercial ROM downloads are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_mappers.TestMapper000
```

If the representative commercial fixture is absent, the implementer must also run any mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-000-nrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

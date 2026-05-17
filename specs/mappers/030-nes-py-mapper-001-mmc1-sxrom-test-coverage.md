# Specification: nes-py Mapper 1 MMC1 SxROM Test Coverage

## Problem

Mapper 1 (MMC1 / SxROM) is already implemented in `nes-py`, and recent mapper characterization work now covers its synthetic ROM behavior. This spec now tracks any remaining representative-fixture alignment for `The Legend of Zelda (USA)` without duplicating the mapper-focused synthetic coverage already added by the archived mapper cleanup specs. The local fixture target is `nes_py/tests/games/the-legend-of-zelda.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/the-legend-of-zelda.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package and native test separation specs. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage under `nes_emu/test/nes_emu/*` and `nes_emu/benchmark/nes_emu/*`, not as Python private-hook tests.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Do not change mapper behavior except to fix a real regression exposed by focused tests.
- Preserve the behavior covered by the existing `ShouldCharacterizeMapper001SxROM` coverage, but move any native-internal assertions to C++ tests instead of relying on Python private hooks. Keep Python coverage focused on the representative-title application-layer workflow.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Current Baseline

- Existing `ShouldCharacterizeMapper001SxROM` coverage inventory covers serial register writes, serial reset behavior, PRG bank modes, CHR ROM/RAM behavior, control-register mirroring modes, PRG RAM protect bits, and backup/restore of mapper state.
- Existing `ShouldIdentifySupportedMapperFixtures` coverage inventory covers mapper 1 native metadata through synthetic fixtures.
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

- [ ] Native C++ tests preserve mapper 1 characterization coverage without reimplementing native internals through Python private hooks.
- [ ] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [ ] Representative fixture header coverage is kept or explicitly referenced from the mapper tests or completion log.
- [ ] Representative fixture `NESEnv` reset, deterministic-step, and `rgb_array` rendering coverage is added or explicitly referenced from an existing test.
- [ ] Native C++ mapper 1 backup/restore coverage proves bank registers, CHR RAM, mirroring, and PRG RAM protect state survive emulator save-state operations.
- [ ] Native C++ tests cover the mapper-specific behavior listed in this spec's focus section, using Catch2 test-runner coverage and native benchmarks where timing or hot-path behavior matters.
- [ ] The test module or mapper spec explains how to provide the representative ROM legally and never fetches it from the network.
- [ ] Missing fixture skips are narrow and explicit; they do not hide native C++ tests or public Python tests that can run without the commercial ROM.
- [ ] Existing mapper tests still pass after this spec lands.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, local virtual environments, and commercial ROM downloads are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
cmake -S . -B build/nes-emu-debug \
  -DCMAKE_BUILD_TYPE=Debug \
  -DNES_EMU_BUILD_TESTS=ON \
  -DNES_EMU_BUILD_BENCHMARKS=OFF
cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests
ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure
python -m unittest discover nes_py/tests/mappers
python -m unittest nes_py.tests.test_rom.ShouldReadLegendOfZelda
```

Run native benchmarks as well when the mapper changes timing hooks, hot-path dispatch, or performance-sensitive banking behavior, and record the command/output in the completion log.

Native C++ tests must run even when the representative commercial fixture is absent. If the fixture is absent, the Python representative-title application test must skip only that integration case and the completion log must document the skipped ROM-backed coverage. If a legal local fixture is present, the Python application-layer mapper test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-001-mmc1-sxrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

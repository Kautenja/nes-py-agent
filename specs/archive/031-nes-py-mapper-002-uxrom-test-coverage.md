# Specification: nes-py Mapper 2 UxROM Test Coverage

## Status: COMPLETE

## Problem

Mapper 2 (UxROM / UNROM) is already implemented in `nes-py`, and recent mapper characterization work now covers its core synthetic ROM behavior. This spec now tracks the remaining mapper 2 coverage gaps, especially representative-fixture alignment for `Mega Man (USA)` and explicit save-state coverage for switchable PRG bank state. The local fixture target is `nes_py/tests/games/mega-man.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/mega-man.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Native Test Layout

Mapper work in this backlog runs after the mapper test package, native test separation specs, and the native per-mapper test split. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage, not as Python private-hook tests.

Mapper 2 native tests belong in `nes_emu/test/nes_emu/mappers/test_mapper_UxROM.cpp` and should use the `[mapper][uxrom]` Catch2 tags. Mapper 2 Python application tests belong in `nes_py/tests/mappers/test_mapper_002_uxrom.py`. Shared native helpers belong in `nes_emu/test/nes_emu/support/mapper_test_helpers.hpp` only when the helper is truly reusable by more than one mapper.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Parallel execution note: this spec should be safe to run alongside specs 032 and 033 because it owns UxROM-specific test and mapper files. Avoid editing NROM or CNROM files unless diagnosing a cross-mapper regression.
- Do not change mapper behavior except to fix a real regression exposed by focused tests.
- Preserve the behavior covered by the existing `ShouldCharacterizeMapper002UxROM` coverage, but move any native-internal assertions to C++ tests instead of relying on Python private hooks. Keep Python coverage focused on the representative-title application-layer workflow.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Current Baseline

- Existing `ShouldCharacterizeMapper002UxROM` coverage inventory covers switchable PRG banking, fixed final PRG bank behavior, CHR RAM reads/writes, safe bank masking, and the current no-bus-conflict assumption.
- Existing `ShouldIdentifySupportedMapperFixtures` coverage inventory covers mapper 2 native metadata through synthetic fixtures.
- Native mapper 2 characterization now lives in `nes_emu/test/nes_emu/mappers/test_mapper_UxROM.cpp`, separate from the NROM, SxROM, and CNROM native test files.
- Explicit mapper 2 backup/restore coverage for the selected PRG bank is still needed.

## Mapper Details

- Mapper ID: `2` / iNES `002`
- Mapper name: `UxROM / UNROM`
- Hardware family: `UxROM discrete PRG bank switching`
- Approximate entries in `nesmapper.txt`: `203`
- Representative test title: `Mega Man (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Mega_Man_(USA)/56246
- Expected local fixture: `nes_py/tests/games/mega-man.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: switchable 16 KiB PRG bank at $8000, fixed final bank at $C000, CHR RAM behavior, bus-conflict assumptions.

## Acceptance Criteria

- [x] Native C++ tests preserve mapper 2 characterization coverage in `nes_emu/test/nes_emu/mappers/test_mapper_UxROM.cpp` without reimplementing native internals through Python private hooks.
- [x] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [x] Representative fixture header coverage is added when a legal fixture is available, or the mapper-level synthetic coverage remains runnable without the commercial ROM.
- [x] Representative fixture `NESEnv` reset, deterministic-step, and `rgb_array` rendering coverage is added when a legal fixture is available.
- [x] Native C++ mapper 2 backup/restore coverage proves the selected PRG bank and CHR RAM survive emulator save-state operations.
- [x] Native C++ tests cover the mapper-specific behavior listed in this spec's focus section, using the dedicated `[mapper][uxrom]` Catch2 coverage and native benchmarks where timing or hot-path behavior matters.
- [x] The spec implementation does not grow a consolidated mapper test or benchmark file; mapper 2 changes stay in UxROM-specific files unless a cross-mapper helper is justified.
- [x] The test module or mapper spec explains how to provide the representative ROM legally and never fetches it from the network.
- [x] Missing fixture skips are narrow and explicit; they do not hide native C++ tests or public Python tests that can run without the commercial ROM.
- [x] Existing mapper tests still pass after this spec lands.
- [x] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, local virtual environments, and commercial ROM downloads are not committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

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
./build/nes-emu-debug/nes_emu_tests "[mapper][uxrom]"
ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure
python -m unittest nes_py.tests.mappers.test_mapper_002_uxrom
python -m unittest discover nes_py/tests/mappers
```

Run native benchmarks as well when the mapper changes timing hooks, hot-path dispatch, or performance-sensitive banking behavior, and record the command/output in the completion log.

Native C++ tests must run even when the representative commercial fixture is absent. If the fixture is absent, the Python representative-title application test must skip only that integration case and the completion log must document the skipped ROM-backed coverage. If a legal local fixture is present, the Python application-layer mapper test must run and pass.

## Completion Notes

- Added native `Emulator::backup()` / `restore()` coverage for mapper 2 selected PRG bank state and CHR RAM contents.
- Added a representative-title mapper 2 Python application test for `nes_py/tests/games/mega-man.nes`; the local fixture was present during verification, so the ROM-backed integration test ran instead of skipping.
- Shared mapper Python helpers now centralize RGB frame, deterministic step, and backup/restore replay assertions for the representative mapper application tests.
- No mapper behavior or timing-sensitive hook changes were made, so native benchmarks were not required.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-002-uxrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

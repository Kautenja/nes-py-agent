# Specification: nes-py Mapper 0 NROM Test Coverage

## Problem

Mapper 0 (NROM) is already implemented in `nes-py`, and recent mapper characterization work now covers its synthetic ROM behavior. This spec now tracks any remaining representative-fixture alignment for `Super Mario Bros. (USA)` without duplicating the mapper-focused synthetic coverage already added by the archived mapper cleanup specs. The local fixture target is `nes_py/tests/games/super-mario-bros-1.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/super-mario-bros-1.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Native Test Layout

Mapper work in this backlog runs after the mapper test package, native test separation specs, and the native per-mapper test split. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage, not as Python private-hook tests.

Mapper 0 native tests belong in `nes_emu/test/nes_emu/mappers/test_mapper_NROM.cpp` and should use the `[mapper][nrom]` Catch2 tags. Mapper 0 Python application tests belong in `nes_py/tests/mappers/test_mapper_000_nrom.py`. Shared native helpers belong in `nes_emu/test/nes_emu/support/mapper_test_helpers.hpp` only when the helper is truly reusable by more than one mapper.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Parallel execution note: this spec should be safe to run alongside specs 031 and 033 because it owns NROM-specific test and mapper files. Avoid editing UxROM or CNROM files unless diagnosing a cross-mapper regression.
- Do not change mapper behavior except to fix a real regression exposed by focused tests.
- Preserve the behavior covered by the existing `ShouldCharacterizeMapper000NROM` coverage, but move any native-internal assertions to C++ tests instead of relying on Python private hooks. Keep Python coverage focused on the representative-title application-layer workflow.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Current Baseline

- Existing `ShouldCharacterizeMapper000NROM` coverage inventory covers fixed 32 KiB PRG mapping, 16 KiB PRG mirroring, CHR ROM reads, reset/step/render smoke behavior, and PRG RAM backup/restore with synthetic ROMs.
- Existing `ShouldIdentifySupportedMapperFixtures` coverage inventory covers mapper 0 native metadata through synthetic fixtures.
- Native mapper 0 characterization now lives in `nes_emu/test/nes_emu/mappers/test_mapper_NROM.cpp`, separate from the UxROM, SxROM, and CNROM native test files.
- `nes_py.tests.test_rom.ShouldReadSuperMarioBros` covers the committed representative fixture header.
- Existing `nes_py.tests.test_nes_env` coverage exercises `NESEnv` reset/step/render behavior with `super-mario-bros-1.nes`.

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

- [ ] Native C++ tests preserve mapper 0 characterization coverage in `nes_emu/test/nes_emu/mappers/test_mapper_NROM.cpp` without reimplementing native internals through Python private hooks.
- [ ] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [ ] Representative fixture header coverage is kept or explicitly referenced from the mapper tests or completion log.
- [ ] Representative fixture `NESEnv` reset, deterministic-step, and `rgb_array` rendering coverage is kept or explicitly referenced from the mapper tests or completion log.
- [ ] Native C++ mapper 0 backup/restore coverage proves mapper-owned PRG RAM survives emulator save-state operations.
- [ ] Native C++ tests cover the mapper-specific behavior listed in this spec's focus section, using the dedicated `[mapper][nrom]` Catch2 coverage and native benchmarks where timing or hot-path behavior matters.
- [ ] The spec implementation does not grow a consolidated mapper test or benchmark file; mapper 0 changes stay in NROM-specific files unless a cross-mapper helper is justified.
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
./build/nes-emu-debug/nes_emu_tests "[mapper][nrom]"
ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure
python -m unittest nes_py.tests.mappers.test_mapper_000_nrom
python -m unittest discover nes_py/tests/mappers
python -m unittest nes_py.tests.test_rom.ShouldReadSuperMarioBros
python -m unittest nes_py.tests.test_nes_env
```

Run native benchmarks as well when the mapper changes timing hooks, hot-path dispatch, or performance-sensitive banking behavior, and record the command/output in the completion log.

Native C++ tests must run even when the representative commercial fixture is absent. If the fixture is absent, the Python representative-title application test must skip only that integration case and the completion log must document the skipped ROM-backed coverage. If a legal local fixture is present, the Python application-layer mapper test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-000-nrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

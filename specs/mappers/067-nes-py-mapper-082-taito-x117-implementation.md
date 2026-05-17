# Specification: nes-py Mapper 82 Taito X1-017 Mapper Implementation

## Problem

Mapper 82 (Taito X1-017) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 82 are rejected before the emulator can initialize, blocking a known slice of the NES library. The representative title for this spec is `Kyuukyoku Harikiri Stadium (Japan)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/kyuukyoku-harikiri-stadium.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/kyuukyoku-harikiri-stadium.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package and native test separation specs. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage under `nes_emu/test/nes_emu/*` and `nes_emu/benchmark/nes_emu/*`, not as Python private-hook tests.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 82 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 82 only after the C++ mapper is wired.
- Reuse existing mapper hooks and bank helpers where they fit the hardware; keep one-off boards isolated when sharing would be misleading.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `82` / iNES `082`
- Mapper name: `Taito X1-017`
- Hardware family: `Taito X1-017 / X117`
- Approximate entries in `nesmapper.txt`: `4`
- Representative test title: `Kyuukyoku Harikiri Stadium (Japan)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Kyuukyoku_Harikiri_Stadium_3_(Japan)/56041
- Expected local fixture: `nes_py/tests/games/kyuukyoku-harikiri-stadium.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: PRG banking, CHR banking, mirroring, Taito register layout.

## Acceptance Criteria

- [ ] A C++ mapper class for mapper 82 exists under `nes_py/nes/include/mappers` and `nes_py/nes/src/mappers`, or an existing class is safely generalized for this mapper.
- [ ] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 82 with a clear mapper name.
- [ ] Python `NESEnv` validation accepts mapper 82 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [ ] The mapper implements the PRG, CHR, mirroring, RAM, IRQ, and variant behavior needed by the representative title or documents any intentionally unsupported secondary feature.
- [ ] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [ ] Native C++ tests cover mapper-specific bank switching and other low-level behavior without routing through Python private hooks; Python coverage remains a public application-layer smoke/fixture test.
- [ ] The test module explains how to provide the representative ROM legally and never fetches it from the network.
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
python -m unittest discover nes_py/tests
```

Run native benchmarks as well when the mapper changes timing hooks, hot-path dispatch, or performance-sensitive banking behavior, and record the command/output in the completion log.

Native C++ tests must run even when the representative commercial fixture is absent. If the fixture is absent, the Python representative-title application test must skip only that integration case and the completion log must document the skipped ROM-backed coverage. If a legal local fixture is present, the Python application-layer mapper test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-082-taito-x117.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

# Specification: nes-py Mapper 7 AxROM Mapper Implementation

## Problem

Mapper 7 (AxROM / AOROM) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 7 are rejected before the emulator can initialize, blocking a known slice of the NES library. The representative title for this spec is `Battletoads (USA)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/battletoads.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/battletoads.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package, native test separation specs, and the native per-mapper test split. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage. Mapper-specific tests should live in a dedicated `nes_emu/test/nes_emu/mappers/test_mapper_<mapper>.cpp` file with a mapper-specific Catch2 tag such as `[mapper][mmc3]`; shared mapper API harnesses stay under `nes_emu/test/nes_emu/*`, and benchmarks stay under `nes_emu/benchmark/nes_emu/*`. Do not add Python private hooks or Python tests whose purpose is to characterize C++ internals.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 7 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 7 only after the C++ mapper is wired.
- Reuse existing mapper hooks and bank helpers where they fit the hardware; keep one-off boards isolated when sharing would be misleading.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `7` / iNES `007`
- Mapper name: `AxROM / AOROM`
- Hardware family: `Nintendo AxROM one-screen mapper`
- Approximate entries in `nesmapper.txt`: `43`
- Representative test title: `Battletoads (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Battletoads_(USA)/54899
- Expected local fixture: `nes_py/tests/games/battletoads.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: 32 KiB PRG bank switching, one-screen lower/upper nametable mirroring, CHR RAM, bus conflicts if applicable.

## Acceptance Criteria

- [ ] A C++ mapper class for mapper 7 exists under `nes_emu/include/nes_emu/mappers` and `nes_emu/src/nes_emu/mappers`, or an existing class is safely generalized for this mapper.
- [ ] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 7 with a clear mapper name.
- [ ] Python `NESEnv` validation accepts mapper 7 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [ ] The mapper implements the PRG, CHR, mirroring, RAM, IRQ, and variant behavior needed by the representative title or documents any intentionally unsupported secondary feature.
- [ ] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [ ] Native C++ tests cover mapper-specific bank switching and other low-level behavior in a dedicated per-mapper file under `nes_emu/test/nes_emu/mappers/` with a mapper-specific Catch2 tag such as `[mapper][mmc3]`; Python coverage remains a public application-layer smoke/fixture test and does not route through private hooks.
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
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-007-axrom.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

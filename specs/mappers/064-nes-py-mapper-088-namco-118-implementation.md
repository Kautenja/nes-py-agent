# Specification: nes-py Mapper 88 Namco 118 Mapper Implementation

## Problem

Mapper 88 (Namco 118) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 88 are rejected before the emulator can initialize. This mapper has a small or specialized catalog footprint, but supporting it fills out long-tail compatibility after the higher-coverage mappers land. The representative title for this spec is `Dragon Spirit (Japan)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/dragon-spirit-japan.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. Write tests so they use a legally supplied local ROM at `nes_py/tests/games/dragon-spirit-japan.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package and native test separation specs. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage under `nes_emu/test/nes_emu/*` and `nes_emu/benchmark/nes_emu/*`, not as Python private-hook tests.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 88 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 88 only after the C++ mapper is wired.
- Keep bootleg, hacked, multicart, and one-off mapper behavior isolated from common licensed mapper code unless a shared abstraction is clearly correct.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `88` / iNES `088`
- Mapper name: `Namco 118`
- Hardware family: `Namco 118`
- Approximate entries in `nesmapper.txt`: `1`
- Representative test title: `Dragon Spirit (Japan)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Dragon_Spirit_-_Aratanaru_Densetsu_(Japan)/55332
- Expected local fixture: `nes_py/tests/games/dragon-spirit-japan.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: Namco 118 PRG/CHR banking registers, mirroring, compatibility with Dragon Spirit.

## Acceptance Criteria

- [ ] A C++ mapper class for mapper 88 exists under `nes_py/nes/include/mappers` and `nes_py/nes/src/mappers`, or an existing class is safely generalized for this mapper.
- [ ] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 88 with a clear mapper name.
- [ ] Python `NESEnv` validation accepts mapper 88 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [ ] The mapper implements the PRG, CHR, mirroring, RAM, IRQ, audio-register, and variant behavior needed by the representative title or documents any intentionally unsupported secondary feature.
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

If the representative commercial fixture is absent, the implementer must still run mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-088-namco-118.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

# Specification: nes-py Mapper 83 PC-Cony Mapper Implementation

## Problem

Mapper 83 (PC-Cony) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 83 are rejected before the emulator can initialize. This mapper has a small or specialized catalog footprint, but supporting it fills out long-tail compatibility after the higher-coverage mappers land. The representative title for this spec is `Garou Densetsu Special`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/garou-densetsu-special.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. Write tests so they use a legally supplied local ROM at `nes_py/tests/games/garou-densetsu-special.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 83 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 83 only after the C++ mapper is wired.
- Keep bootleg, hacked, multicart, and one-off mapper behavior isolated from common licensed mapper code unless a shared abstraction is clearly correct.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `83` / iNES `083`
- Mapper name: `PC-Cony`
- Hardware family: `PC-Cony pirate mapper`
- Approximate entries in `nesmapper.txt`: `1`
- Representative test title: `Garou Densetsu Special`
- Emuparadise catalog search: https://www.emuparadise.me/roms/search.php?section=roms&sysid=13&query=Garou+Densetsu+Special+NES
- Expected local fixture: `nes_py/tests/games/garou-densetsu-special.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: pirate mapper banking registers, large CHR handling, IRQ behavior if documented.

## Acceptance Criteria

- [ ] A C++ mapper class for mapper 83 exists under `nes_py/nes/include/mappers` and `nes_py/nes/src/mappers`, or an existing class is safely generalized for this mapper.
- [ ] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 83 with a clear mapper name.
- [ ] Python `NESEnv` validation accepts mapper 83 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [ ] The mapper implements the PRG, CHR, mirroring, RAM, IRQ, audio-register, and variant behavior needed by the representative title or documents any intentionally unsupported secondary feature.
- [ ] Tests identify the mapper from the fixture header, instantiate `NESEnv`, run reset, deterministic steps, `rgb_array` rendering, and backup/restore when the representative fixture is legally available.
- [ ] Mapper-specific bank-switching behavior is covered by observable game smoke checks, a focused mapper/unit harness, or both.
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
python -m unittest nes_py.tests.test_mappers
python -m unittest discover .
```

If the representative commercial fixture is absent, the implementer must still run mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-083-pc-cony.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

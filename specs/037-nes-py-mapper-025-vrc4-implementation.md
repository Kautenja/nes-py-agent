# Specification: nes-py Mapper 25 Konami VRC4 Mapper Implementation

## Problem

Mapper 25 (Konami VRC4) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 25 are rejected before the emulator can initialize. This mapper has a small or specialized catalog footprint, but supporting it fills out long-tail compatibility after the higher-coverage mappers land. The representative title for this spec is `Gradius II (Japan)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/gradius-ii-japan.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. Write tests so they use a legally supplied local ROM at `nes_py/tests/games/gradius-ii-japan.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Update Python-side supported mapper validation so mapper 25 ROMs can initialize after the C++ mapper is wired.
- Keep bootleg, hacked, multicart, and one-off mapper behavior isolated from common licensed mapper code unless a shared abstraction is clearly correct.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `25` / iNES `025`
- Mapper name: `Konami VRC4`
- Hardware family: `Konami VRC4 variant`
- Approximate entries in `nesmapper.txt`: `2`
- Representative test title: `Gradius II (Japan)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Gradius_II_(Japan)/55664
- Expected local fixture: `nes_py/tests/games/gradius-ii-japan.nes`
- Technical reference: https://www.nesdev.org/wiki/Mapper
- Focus: VRC4 address-line decoding, PRG banking, CHR banking, mirroring, IRQ counter.

## Acceptance Criteria

- [ ] A C++ mapper class for mapper 25 exists under `nes_py/nes/include/mappers` and `nes_py/nes/src/mappers`, or an existing class is safely generalized for this mapper.
- [ ] `MapperID` and `MapperFactory` register mapper 25 with a clear mapper name.
- [ ] Python ROM validation accepts mapper 25 only after the mapper implementation is wired.
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
python -m unittest nes_py.tests.test_mappers.TestMapper025
python -m unittest discover .
```

If the representative commercial fixture is absent, the implementer must still run mapper-level tests that do not require the fixture and document the skipped integration coverage in the completion log. If a legal local fixture is present, the mapper-specific integration test must run and pass.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-025-vrc4.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

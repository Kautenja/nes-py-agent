# Specification: nes-py Mapper 5 MMC5 Mapper Implementation

## Status: COMPLETE

## Problem

Mapper 5 (MMC5) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 5 are rejected before the emulator can initialize, blocking a known slice of the NES library. The representative title for this spec is `Castlevania III - Dracula's Curse (USA)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/castlevania-iii-draculas-curse.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/castlevania-iii-draculas-curse.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package, native test separation specs, and the native per-mapper test split. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage. Mapper-specific tests should live in a dedicated `nes_emu/test/nes_emu/mappers/test_mapper_<mapper>.cpp` file with a mapper-specific Catch2 tag such as `[mapper][mmc5]`; shared mapper API harnesses stay under `nes_emu/test/nes_emu/*`, and benchmarks stay under `nes_emu/benchmark/nes_emu/*`. Do not add Python private hooks or Python tests whose purpose is to characterize C++ internals.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 5 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 5 only after the C++ mapper is wired.
- Reuse existing mapper hooks and bank helpers where they fit the hardware; keep one-off boards isolated when sharing would be misleading.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `5` / iNES `005`
- Mapper name: `MMC5`
- Hardware family: `Nintendo MMC5 / ExROM`
- Approximate entries in `nesmapper.txt`: `11`
- Representative test title: `Castlevania III - Dracula's Curse (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Castlevania_III_-_Dracula's_Curse_(USA)/55043
- Expected local fixture: `nes_py/tests/games/castlevania-iii-draculas-curse.nes`
- Technical reference: https://www.nesdev.org/wiki/MMC5
- Focus: PRG banking modes, CHR banking modes, extended attributes, ExRAM, IRQ scanline behavior, multiplication registers, save RAM.

## Research Findings (2026-05-17)

Hardware and emulator references consulted:

- NESdev MMC5 hardware reference: https://www.nesdev.org/wiki/MMC5
- Mesen2 MMC5 implementation: https://github.com/SourMesen/Mesen2/blob/fabc9a62174f8734a113df6d244f5539ef6b8fcf/Core/NES/Mappers/Nintendo/MMC5.h
- Mesen2 MMC5 memory-handler implementation: https://github.com/SourMesen/Mesen2/blob/fabc9a62174f8734a113df6d244f5539ef6b8fcf/Core/NES/Mappers/Nintendo/Mmc5MemoryHandler.h
- FCEUX MMC5 implementation: https://github.com/TASEmulators/fceux/blob/1e1168db6662ce86848460b5d078e17c6dc6e2ce/src/boards/mmc5.cpp

Required behavior:

- Implement PRG mode register `$5100` and PRG bank registers `$5113-$5117`, including 8 KiB, 16 KiB, and 32 KiB PRG arrangements and the correct fixed/switchable windows.
- Implement CHR mode register `$5101`, CHR bank registers `$5120-$512B`, and upper CHR bank bits from `$5130`. Support separate sprite/background CHR banks well enough for the representative title and native synthetic tests.
- Implement WRAM protection registers `$5102/$5103`, PRG RAM banking, and battery-backed PRG RAM state according to parsed cartridge metadata.
- Implement ExRAM mode `$5104` and CPU access at `$5C00-$5FFF`; cover attribute, nametable, ordinary RAM, and read-only behavior as supported by the first implementation.
- Implement nametable mapping register `$5105` and fill-mode registers `$5106/$5107` by using mapper-owned nametable mapping rather than trying to express MMC5 through the two-bit base mirroring mode alone.
- Implement scanline IRQ/status registers `$5203/$5204` and multiplier registers `$5205/$5206`.
- Treat vertical split registers `$5200-$5202` and MMC5 pulse/PCM audio as explicit secondary features: implement them if practical, otherwise document them in code and completion logs as intentionally unsupported while ensuring the representative title does not depend on them for the smoke path.
- Preserve all mapper registers, selected banks, ExRAM/WRAM contents, IRQ state, multiplier state, nametable/fill state, and any PPU rendering-context state in backup/restore.

Implementation notes:

- MMC5 is materially larger than the other pending specs. Prefer a focused but honest first pass that covers the representative title and synthetic tests over a partial-looking "supported" flag with undocumented gaps.
- Reuse the existing mapper-owned nametable hooks for `$5105-$5107` and ExRAM-backed nametable behavior.
- Use PPU address/read/write observation only for the MMC5 rendering-context and scanline IRQ details that need it. Keep hot-path read/write mapping table-driven once registers change.
- Native tests should be broad enough to pin PRG modes, CHR modes, WRAM protect behavior, ExRAM access modes, nametable/fill mapping, IRQ/status semantics, multiplier behavior, and backup/restore. Add benchmarks if the implementation introduces always-on PPU or CPU hooks.

## Acceptance Criteria

- [x] A C++ mapper class for mapper 5 exists under `nes_emu/include/nes_emu/mappers` and `nes_emu/src/nes_emu/mappers`, or an existing class is safely generalized for this mapper.
- [x] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 5 with a clear mapper name.
- [x] Python `NESEnv` validation accepts mapper 5 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [x] The mapper implements MMC5 PRG modes, CHR modes, WRAM protect/banking, ExRAM, nametable/fill mapping, scanline IRQ/status, multiplier behavior, and the representative-title variant behavior; vertical split and audio are either implemented or explicitly documented as unsupported secondary features.
- [x] A Python application-layer mapper test exists for the representative title and expected local fixture path listed above; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [x] Native C++ tests cover mapper-specific bank switching and other low-level behavior in a dedicated per-mapper file under `nes_emu/test/nes_emu/mappers/` with a mapper-specific Catch2 tag such as `[mapper][mmc5]`; Python coverage remains a public application-layer smoke/fixture test and does not route through private hooks.
- [x] The test module explains how to provide the representative ROM legally and never fetches it from the network.
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
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-005-mmc5.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

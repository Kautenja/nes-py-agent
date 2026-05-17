# Specification: nes-py Mapper 69 Sunsoft FME-7 Mapper Implementation

## Status: COMPLETE

## Problem

Mapper 69 (Sunsoft FME-7 / Sunsoft 5B) appears in the NES mapper catalog but is not implemented in `nes-py`. ROMs using mapper 69 are rejected before the emulator can initialize, blocking a known slice of the NES library. The representative title for this spec is `Batman - Return of the Joker (USA)`, selected from the NES catalog and cross-checked against the repository mapper list. The local fixture target is `nes_py/tests/games/batman-return-of-the-joker.nes`.

## ROM Fixture Policy

Emuparadise NES catalog at https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/13 lists the representative title, but do not download commercial ROMs from that site. Use a legally owned dump or a redistributable test ROM. Do not commit new commercial ROM assets. The Emuparadise link below is a catalog/title-page reference only; do not add direct download URLs, downloader scripts, or ROM acquisition steps to this spec or tests. If the representative title is already present in the repository, use that fixture. Otherwise, write tests so they use a legally supplied local ROM at `nes_py/tests/games/batman-return-of-the-joker.nes` and skip only the commercial-ROM integration portion with a clear message when the file is absent. Any redistributable public-domain or homebrew mapper test ROM may be committed only if its license is included and permits redistribution.

## Post-023 Test Layering

Mapper work in this backlog runs after the mapper test package, native test separation specs, and the native per-mapper test split. Treat C++ mapper correctness, native-internal edge cases, synthetic ROM characterization, IRQ timing, backup/restore internals, and performance-sensitive hook behavior as native C++ test-runner or benchmark coverage. Mapper-specific tests should live in a dedicated `nes_emu/test/nes_emu/mappers/test_mapper_<mapper>.cpp` file with a mapper-specific Catch2 tag such as `[mapper][fme7]`; shared mapper API harnesses stay under `nes_emu/test/nes_emu/*`, and benchmarks stay under `nes_emu/benchmark/nes_emu/*`. Do not add Python private hooks or Python tests whose purpose is to characterize C++ internals.

Each mapper must still have a Python application-layer test keyed to the representative title and expected local fixture path listed below. That test should be written so a legal ROM can be placed at the fixture path later; when the ROM is absent, skip only that representative-title integration check with a clear message. The Python test should exercise public package behavior such as ROM/header metadata, `NESEnv` construction, reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if that remains part of the package workflow.


## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Add a mapper implementation in the C++ NES core and register it in the mapper factory.
- Register mapper 69 in the native mapper registry so `_native.is_mapper_supported` and Python `NESEnv` validation accept mapper 69 only after the C++ mapper is wired.
- Reuse existing mapper hooks and bank helpers where they fit the hardware; keep one-off boards isolated when sharing would be misleading.
- Preserve existing behavior for all already-supported mappers.
- Do not add, download, or commit commercial ROM files.

## Mapper Details

- Mapper ID: `69` / iNES `069`
- Mapper name: `Sunsoft FME-7 / Sunsoft 5B`
- Hardware family: `Sunsoft FME-7`
- Approximate entries in `nesmapper.txt`: `6`
- Representative test title: `Batman - Return of the Joker (USA)`
- Emuparadise catalog link: https://www.emuparadise.me/Nintendo_Entertainment_System_ROMs/Batman_-_Return_of_the_Joker_(USA)/54874
- Expected local fixture: `nes_py/tests/games/batman-return-of-the-joker.nes`
- Technical reference: https://www.nesdev.org/wiki/Sunsoft_FME-7
- Focus: command/parameter register model, PRG banking, CHR banking, mirroring, IRQ counter, optional Sunsoft 5B audio documented if not implemented.

## Research Findings (2026-05-17)

Hardware and emulator references consulted:

- NESdev Sunsoft FME-7 hardware reference: https://www.nesdev.org/wiki/Sunsoft_FME-7
- Mesen2 Sunsoft FME-7 implementation: https://github.com/SourMesen/Mesen2/blob/fabc9a62174f8734a113df6d244f5539ef6b8fcf/Core/NES/Mappers/Sunsoft/SunsoftFme7.h
- FCEUX Mapper 69 implementation: https://github.com/TASEmulators/fceux/blob/1e1168db6662ce86848460b5d078e17c6dc6e2ce/src/boards/69.cpp

Required behavior:

- Implement the command register at `$8000-$9FFF` and parameter register at `$A000-$BFFF`; command selection uses the low 4 bits.
- Implement commands 0-7 as eight 1 KiB CHR bank registers.
- Implement command 8 for `$6000-$7FFF` mapping, including PRG ROM vs PRG RAM selection and RAM enable/write behavior.
- Implement commands 9-B as the 8 KiB PRG ROM bank registers for `$8000-$9FFF`, `$A000-$BFFF`, and `$C000-$DFFF`; keep the last 8 KiB PRG ROM bank fixed at `$E000-$FFFF`.
- Implement command C mirroring modes: vertical, horizontal, one-screen lower/screen A, and one-screen upper/screen B.
- Implement commands D-F for IRQ control and the 16-bit IRQ counter low/high bytes. The IRQ counter is CPU-cycle based and decrements once per CPU cycle while enabled; flagship implementations assert IRQ when the enabled counter wraps.
- Treat Sunsoft 5B audio as an optional secondary feature: implement it if the audio system can host it cleanly, otherwise document it as unsupported while still preserving the register writes if useful for future compatibility.
- Preserve command select, PRG/CHR registers, `$6000` RAM/ROM state, mirroring, IRQ control/counter state, PRG RAM contents, and any audio register state in backup/restore.

Implementation notes:

- Enable the mapper CPU-cycle hook for the IRQ counter; no PPU address hook is needed for FME-7 banking.
- Keep PRG and CHR mapping table-driven after command writes. Reads should only index active 8 KiB PRG or 1 KiB CHR windows.
- Native tests should cover command/parameter latch behavior, all CHR and PRG windows, `$6000` RAM/ROM switching and RAM disable semantics, all mirroring modes, IRQ countdown/wrap/disable behavior, and backup/restore.

## Acceptance Criteria

- [x] A C++ mapper class for mapper 69 exists under `nes_emu/include/nes_emu/mappers` and `nes_emu/src/nes_emu/mappers`, or an existing class is safely generalized for this mapper.
- [x] The native mapper registry, `MapperFactory`, and `IsMapperSupported` register mapper 69 with a clear mapper name.
- [x] Python `NESEnv` validation accepts mapper 69 through `_native.is_mapper_supported` only after the mapper implementation is wired.
- [x] The mapper implements FME-7 command/parameter registers, 1 KiB CHR banking, 8 KiB PRG banking, `$6000` RAM/ROM mapping, mirroring modes, CPU-cycle IRQ counter behavior, backup/restore, and any representative-title variant behavior; Sunsoft 5B audio is either implemented or explicitly documented as unsupported.
- [x] A Python application-layer mapper test exists for the representative title and expected local fixture path listed below; when a legal fixture is present it identifies the mapper from the header, instantiates `NESEnv`, runs reset, a short deterministic step sequence, `rgb_array` rendering, close, and public backup/restore behavior if retained.
- [x] Native C++ tests cover mapper-specific bank switching and other low-level behavior in a dedicated per-mapper file under `nes_emu/test/nes_emu/mappers/` with a mapper-specific Catch2 tag such as `[mapper][fme7]`; Python coverage remains a public application-layer smoke/fixture test and does not route through private hooks.
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
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-069-sunsoft-fme7.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

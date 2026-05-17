# nes-py Mapper 001 MMC1/SxROM Coverage

## Summary

- Added representative-title Python mapper coverage for `The Legend of Zelda (USA)` at `nes_py/tests/games/the-legend-of-zelda.nes`.
- The representative test verifies mapper 1 header metadata, constructs `NESEnv`, runs reset, deterministic steps, `rgb_array` render, and retained package backup/restore workflow.
- Added native Catch2 emulator save-state coverage proving mapper 1 PRG bank registers, CHR RAM, mirroring, PRG RAM contents, and PRG RAM protect state survive `Emulator::backup()` / `restore()`.
- Kept existing native mapper 1 characterization coverage for serial writes, reset behavior, PRG modes, CHR banking, mirroring modes, and PRG RAM protection.

## Verification

- `.venv/bin/python -m pip install -e .` (passed)
- `cmake -S . -B build/nes-emu-debug -DCMAKE_BUILD_TYPE=Debug -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=OFF` (passed)
- `cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests` (passed)
- `ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure` (23 tests passed)
- `.venv/bin/python -m unittest discover nes_py/tests/mappers` (9 tests passed)
- `.venv/bin/python -m unittest nes_py.tests.test_rom.ShouldReadLegendOfZelda` (21 tests passed)
- `git -C nes-py diff --check` (passed)

Notes:

- `python` was not on PATH and system `python3` rejected editable installs under PEP 668, so verification used the repository virtualenv interpreter.
- The local Zelda fixture was present, so the representative ROM-backed integration test ran and passed. No ROM downloads or new ROM assets were added.
- Native benchmarks were not run because this spec changed tests only, not mapper timing hooks or hot-path behavior.

## Commits

- `nes-py` child submodule: `800c4d062e32662cfe7d2b77d74f683db3a76343`, pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `nes-py` gitlink update, archived spec, history entry, and completion log.

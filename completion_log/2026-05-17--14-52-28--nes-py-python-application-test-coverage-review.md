# nes-py Python Application Test Coverage Review

## Summary

- Reworked Python coverage around public package behavior: ROM metadata, NESEnv construction/reset/step/render/close flows, invalid fixture errors, unsupported mapper errors, deterministic stepping, multi-environment isolation, play CLI, and speedtest API/CLI.
- Removed Python imports of private native metadata/mapper helpers and removed private mapper metadata assertions from Python tests.
- Added native Catch2 cartridge coverage for iNES/NES 2.0 metadata, malformed ROM rejection, trainer/PAL rejection, four-screen priority, and CHR RAM defaults.
- Kept only direct Python `_backup`/`_restore` calls in `ShouldPreservePackageBackupRestoreWorkflow`, because the packaged speedtest API and current game wrapper reset workflows still rely on this private package-level state workflow and there is no public replacement yet.

## Python Test Module Classification

- `nes_py/tests/__init__.py`: package marker, unchanged.
- `nes_py/tests/mapper_fixtures.py`: kept as synthetic iNES fixture helper for application-level tests; docstring updated away from native characterization language.
- `nes_py/tests/rom_file_abs_path.py`: kept as disk fixture path helper.
- `nes_py/tests/test_app_imports.py`: kept public import side-effect coverage.
- `nes_py/tests/test_cartridge_metadata.py`: reworked from Python/native parser alignment into public ROM metadata and public NESEnv rejection coverage; native assertions moved to Catch2.
- `nes_py/tests/test_multiple_makes.py`: kept and strengthened public multi-process, thread, and same-process environment coverage, including visible RAM/controller isolation and close behavior.
- `nes_py/tests/test_nes_env.py`: broadened public NESEnv coverage across all supported on-disk ROMs; mapper-4 disk ROMs now assert public unsupported-mapper errors; NativeEmulator implementation-detail assertions removed.
- `nes_py/tests/test_play.py`: kept public play CLI coverage.
- `nes_py/tests/test_rom.py`: kept public ROM metadata coverage for on-disk fixtures.
- `nes_py/tests/test_speedtest.py`: kept public speedtest API/CLI coverage and added synthesized-ROM benchmark coverage; no C++ native microbenchmarks are invoked through Cython.
- `nes_py/tests/mappers/__init__.py`: package marker, unchanged.
- `nes_py/tests/mappers/common.py`: kept as synthetic mapper public workflow helper; private backup/restore and private close-state checks removed.
- `nes_py/tests/mappers/test_mapper_000_nrom.py`: kept application-level synthetic NROM construction/step coverage; mapper internals remain in Catch2.
- `nes_py/tests/mappers/test_mapper_001_sxrom.py`: kept application-level synthetic SxROM construction/step coverage; mapper internals remain in Catch2.
- `nes_py/tests/mappers/test_mapper_002_uxrom.py`: kept application-level synthetic UxROM construction/step coverage; mapper internals remain in Catch2.
- `nes_py/tests/mappers/test_mapper_003_cnrom.py`: kept application-level synthetic CNROM construction/step coverage; mapper internals remain in Catch2.
- `nes_py/tests/mappers/test_registry.py`: reworked to public synthetic mapper construction and unsupported-mapper constructor rejection; `_is_mapper_supported` and private env metadata calls removed.

Useful native-internal coverage removed from Python is covered by:

- `nes_emu/test/nes_emu/test_cartridge.cpp` for native cartridge metadata and malformed/unsupported cartridge rejection.
- Existing `nes_emu/test/nes_emu/test_current_mappers.cpp` for mapper PRG/CHR banking, mirroring, PRG RAM, CHR RAM, and clone behavior.
- Existing `nes_emu/test/nes_emu/test_cpu.cpp`, `test_main_bus.cpp`, `test_picture_bus.cpp`, `test_mapper_hooks.cpp`, and `test_mapper_bank_helpers.cpp` for CPU, bus, PPU, mapper hooks, and bank helper internals.

## Verification

- `cmake -S . -B build/nes-emu-debug -DCMAKE_BUILD_TYPE=Debug -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=OFF`
- `cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests`
- `ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure` (22 tests passed)
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover nes_py/tests` (177 tests passed)
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 10 --json --no-progress`
- `rg "from nes_py import _native|import nes_py\\._native|_native_.*smoke|characterization_smoke|native_.*benchmark|_read_prg|_write_prg|_read_chr|_write_chr" nes_py/tests nes_py/speedtest.py` (no matches)
- `.venv/bin/python -m build`
- `.venv/bin/python -m pip install dist/*.whl --force-reinstall`
- `/Users/christiankauten/Documents/Projects/gym-nes/nes-py/.venv/bin/python -c "import nes_py; from nes_py.nes_env import NESEnv; print(nes_py.__name__, NESEnv.__name__)"` from `/tmp`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `git diff --check`

Notes:

- `python` is not on PATH in this environment.
- The system `python3` is PEP 668-managed, so package verification used the existing ignored `.venv`.
- The wheel import check must run outside the repo root after a non-editable wheel install because the source tree shadows the installed wheel and does not contain an in-place `_native` extension.
- Gym emitted its existing unmaintained/NumPy 2 warning during Python test, speedtest, and import checks.

## Commits

- `nes-py` child submodule: `d7bef3a259c9fcedcaf277118722b7e2b9c7698b` (`Review Python application test coverage`), pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `nes-py` gitlink update, archive summary, history entry, and completion log.

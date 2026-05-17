# nes-py Mapper 069 Sunsoft FME-7

## Summary

Implemented mapper 69 / Sunsoft FME-7 in `nes-py` with command/parameter register handling, 1 KiB CHR banking, 8 KiB PRG banking, `$6000-$7fff` PRG ROM/RAM selection, mirroring modes, CPU-cycle IRQ counter behavior, clone/save-state preservation, and stored Sunsoft 5B audio register writes for future expansion-audio support. Added native Catch2 mapper coverage and public Python mapper smoke coverage for the local Batman Return of the Joker fixture path.

Sunsoft 5B audio mixing remains unsupported because the current emulator has no expansion-audio mixer path; writes to the 5B audio select/data registers are retained in mapper state.

## Verification

- `cmake -S . -B build/nes-emu-debug -DCMAKE_BUILD_TYPE=Debug -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON` passed.
- `cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests` passed.
- `ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure` passed: 33/33 tests.
- `.venv/bin/python -m pip install -e .` passed.
- `.venv/bin/python -m unittest discover nes_py/tests/mappers` passed: 14 tests.
- `.venv/bin/python -m unittest discover nes_py/tests` passed: 192 tests.
- `cmake --build build/nes-emu-debug --config Debug --target nes_emu_benchmarks` passed.
- `./build/nes-emu-debug/nes_emu_benchmarks` passed: 1 benchmark test case. Observed means included CPU dispatch 329.905 us, main bus I/O dispatch 403.974 us, mapper CPU-cycle dispatch without hook 332.667 us, and with hook 333.289 us.

The local fixture `nes_py/tests/games/batman-return-of-the-joker.nes` was present, identified as mapper 69, and the representative Python integration test ran instead of skipping.

## Commits Pushed

- `nes-py`: `8fdb451` (`codex/spec-038-fme7`) - Add mapper 69 Sunsoft FME-7 support.

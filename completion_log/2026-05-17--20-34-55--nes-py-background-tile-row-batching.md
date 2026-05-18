# nes-py Background Tile Row Batching

Summary:
- Implemented a mapper-gated background tile-row bit cache in `nes-py`.
- Cached reversed low/high pattern bitplanes, attribute palette high bits, and opacity masks per background tile row.
- Preserved exact read-per-pixel behavior for mappers with PPU address/read/write observers.
- Added native PPU coverage for fine X scroll, horizontal nametable wrapping, vertical fine-Y incrementing, attribute quadrant selection, left-edge background masking, and mapper-hook gating.
- Added `nes_py.tests.test_mappers` as a unittest compatibility entry point for the documented mapper test command.

Benchmarks:
- Before, one-sample native PPU benchmark: background-only `458.443 us`; full-frame ROMs: mapper 0 `835.150 us`, mapper 1 `773.318 us`, mapper 2 `407.692 us`, mapper 3 `403.651 us`, mapper 4 `437.900 us`, mapper 5 `478.568 us`, mapper 7 `406.234 us`, mapper 9 `489.692 us`, mapper 69 `778.193 us`.
- A decoded palette-address array experiment was abandoned before commit because it regressed background-only rendering to about `630.942 us`.
- After, final verification native benchmark: background-only `446.525 us`; full-frame ROMs: mapper 0 `745.651 us`, mapper 1 `785.734 us`, mapper 2 `433.567 us`, mapper 3 `426.318 us`, mapper 4 `428.151 us`, mapper 5 `489.567 us`, mapper 7 `428.193 us`, mapper 9 `499.025 us`, mapper 69 `785.317 us`.

Verification:
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON`
- `cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks`
- `build/nes-emu-release/nes_emu_tests`
- `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` (`1321.012` steps/s)
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress` (`1466.732` steps/s)
- `git diff --check`

Commits:
- `nes-py`: `a29f6b3` (`Batch background tile row rendering`)

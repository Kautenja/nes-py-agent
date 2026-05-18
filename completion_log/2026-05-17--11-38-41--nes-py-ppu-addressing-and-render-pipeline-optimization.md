# nes-py PPU Addressing and Render Pipeline Optimization

## Summary

Completed work item 018 in `nes-py`.

- Normalized picture-bus pattern, nametable, `$3000-$3EFF`, palette, and `$3FFF` address handling.
- Fixed PPUDATA buffering to use the original read address for delayed-read decisions.
- Converted PPU OAM, scanline sprite indexes, screen snapshots, palette RAM, and nametable RAM to fixed-size storage.
- Added conservative background tile-row/attribute caching when mapper-visible PPU hooks are not active.
- Replaced per-scanline sprite vector resize/push work with fixed-size sprite index evaluation.
- Added native PPU and picture-bus smoke coverage exposed through Cython/Python tests.
- Documented before/after normal and render-heavy benchmarks in `docs/ppu-addressing-render-pipeline-benchmarks.md`.

## Verification

Commands were run inside `nes-py` with `.venv/bin/python` because `python` is not on PATH in this shell.

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_native_ppu`
- `.venv/bin/python -m unittest nes_py.tests.test_native_cpu_bus`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --render-mode rgb_array --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --render-mode rgb_array --json --no-progress`

Final measured normal step throughput:

- `super-mario-bros-1.nes`: 1262.97 steps/s
- `the-legend-of-zelda.nes`: 1438.24 steps/s

Final measured render-heavy throughput:

- `super-mario-bros-1.nes`: 1287.56 frames/s
- `the-legend-of-zelda.nes`: 1459.13 frames/s

## Commits

- `nes-py`: `fca0c10` (`Optimize PPU address and render paths`), pushed to `origin/ralph-dev`.

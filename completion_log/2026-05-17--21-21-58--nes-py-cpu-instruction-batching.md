# nes-py CPU Instruction Batching

## Summary

Added a native CPU instruction-level API that reports scheduled instruction
cycles, consumes pending stall cycles, and exposes deterministic CPU snapshots
for native tests. `Emulator::step` now uses an instruction-batched frame path
for mappers that do not observe CPU cycles, while CPU-cycle-hooked mappers keep
the original cycle-by-cycle path. Native tests compare cycle-by-cycle and
batched stepping across reset, multiple frames, backup, restore, and
continuation for representative mapper 0-3 ROM fixtures.

## Verification

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON`
- `cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks`
- `build/nes-emu-release/nes_emu_tests`
- `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` -> 1480.70 fps
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress` -> 1560.68 fps
- `git diff --check`

## Commits

- `nes-py`: `c089db295c1b91c5a8e0ae3a7159bda960b7b9f1` pushed to `origin/ralph-dev`
- Umbrella repository: this commit records the updated `nes-py` gitlink, archived spec, history entry, and completion log.

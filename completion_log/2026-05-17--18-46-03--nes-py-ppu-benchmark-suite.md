# nes-py PPU Benchmark Suite

Completed spec 039 by adding a native PPU benchmark suite and baseline
developer note in `nes-py`.

## Summary

- Added native Catch2 benchmark profiles for render-off, background-only, and
  sprite-heavy synthetic PPU frames.
- Added mapper 0, 1, 2, and 3 synthetic CHR read stress profiles using native
  mapper wiring.
- Added representative full-frame ROM profiles for Super Mario Bros., Zelda,
  Mega Man, and Adventure Island fixtures.
- Recorded baseline native benchmark timings and public `nes_py.speedtest`
  Mario/Zelda comparison numbers in `nes-py/docs/ppu-benchmark-suite-baseline.md`.

## Verification

Commands run in `nes-py`:

- `.venv/bin/python -m pip install -e .` passed.
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_BENCHMARKS=ON` passed.
- `cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks` passed.
- `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1` passed: 12 assertions in 4 test cases.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1305.15 steps/s.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1470.35 steps/s.
- `git diff --check` passed in `nes-py` and the umbrella repository.

## Commits

- `nes-py`: `14a781e` (`ralph-dev`) pushed to origin.

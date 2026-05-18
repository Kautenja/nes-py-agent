# nes-py Sprite Row Prefetch

## Summary

- Added a mapper-gated PPU sprite row cache that prefetches selected scanline
  sprite rows for mappers with stable CHR reads and no PPU hook/name-table
  timing requirements.
- Cached per-row sprite X, index, priority, palette base, pattern bytes, and
  decoded 8-pixel color values so sprite-heavy scanlines avoid repeated CHR
  reads and bit extraction inside the visible pixel loop.
- Added native Catch2 coverage for horizontal flip, vertical flip, background
  priority, OAM priority, transparent pixels, 8x16 sprites, sprite-zero hit,
  one-row CHR read counts, and disabled prefetch for mapper PPU observers.

## Benchmark Notes

Before/after native profiles were compared on the same machine using a
temporary baseline worktree at `b9a6216` and the final tree at `4b8b2df`.

- Sprite-heavy synthetic PPU frame, 3 samples: `572.401 us` before,
  `555.414 us` after.
- Full-frame Super Mario Bros. mapper 0, 3 samples: `723.498 us` before,
  `737.415 us` after.
- Full-frame Mega Man mapper 2, 3 samples: `410.457 us` before,
  `409.609 us` after.

The kept optimization is intentionally gated; mapper 1 and hook-observing
mappers do not use the prefetch path.

## Verification

Commands run in `nes-py`:

- `.venv/bin/python -m pip install -e .` passed.
- `.venv/bin/python -m unittest nes_py.tests.test_mappers` was attempted but
  the legacy module path does not exist in this tree.
- `.venv/bin/python -m unittest discover nes_py.tests.mappers` passed: 23 tests.
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env` passed: 23 tests.
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest` passed: 5 tests.
- `.venv/bin/python -m unittest discover .` passed: 201 tests.
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON` passed.
- `cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks` passed.
- `build/nes-emu-release/nes_emu_tests` passed: 522 assertions in 58 test cases.
- `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1` passed: 27 assertions in 4 test cases.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1352.91 steps/s.
- `git diff --check` passed in `nes-py` and the umbrella repository.

## Commits

- `nes-py`: `4b8b2df` (`ralph-dev`) pushed to origin.
- Umbrella repository: this commit records the `nes-py` submodule pointer,
  completion log, history entry, and archive summary.

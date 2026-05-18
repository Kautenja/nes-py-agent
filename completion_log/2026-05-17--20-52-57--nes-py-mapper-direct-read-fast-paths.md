# nes-py Mapper Direct Read Fast Paths

## Summary

- Added mapper-provided direct read pages for NROM, SxROM/MMC1, UxROM, and
  CNROM PRG/CHR windows.
- Cached four 8 KiB PRG pages in `MainBus` and eight 1 KiB CHR pages in
  `PictureBus`, refreshing them after mapper writes and restore-time rewiring.
- Kept CHR writes, PRG RAM, expansion routing, PPU observer hooks, and mapper
  nametable mapping on the existing safe mapper paths.
- Added native regression coverage for direct PRG/CHR reads, bank switching,
  backup/restore, bus cache refresh, CHR RAM writes, and PPU hook bypasses.
- Added PRG read stress benchmarks and recorded before/after PRG, CHR,
  full-frame, and public speedtest results in
  `docs/mapper-direct-read-fast-paths.md`.

## Verification

Commands run in `nes-py`:

- `.venv/bin/python -m pip install -e .` passed.
- `.venv/bin/python -m unittest nes_py.tests.test_mappers` passed: 23 tests.
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env` passed: 23 tests.
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest` passed: 5 tests.
- `.venv/bin/python -m unittest discover .` passed: 224 tests.
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON` passed.
- `cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks` passed.
- `build/nes-emu-release/nes_emu_tests` passed: 626 assertions in 65 test cases.
- `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1` passed: 31 assertions in 5 test cases.
- Temporary baseline PRG benchmark worktree at `a29f6b3` passed with only the
  new benchmark harness applied.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1495.08 steps/s after the change.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1536.16 steps/s after the change.
- `git diff --check` passed in `nes-py`.

## Commits

- `nes-py`: `8e33e74` (`Add mapper direct read fast paths`), pushed to
  `origin/ralph-dev`.
- Umbrella repository: this commit records the `nes-py` submodule pointer,
  completion log, history entry, and archived spec.

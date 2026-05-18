# Completion Log: nes-py Native Hot Path Optimization Benchmarks

## Summary

Completed work item 016, the native benchmark and optimization pass in
`nes-py`.
The measured native frame-step path stayed almost entirely under the Cython
`NativeEmulator.frame_advance` boundary, so the optimization stayed inside the
native hot path and avoided the broader CPU/bus and PPU refactors reserved for
work items 017 and 018.

The landed optimization replaces `MainBus` unordered-map I/O register callback
dispatch with direct CPU/PPU/controller device dispatch for emulator-owned
devices, keeps fixed callback arrays only as fallback slots, and stores CPU RAM
as a fixed 2 KiB `std::array`. The benchmark API/CLI now includes a portable
mapper hook smoke profile so work item 012 CPU-cycle, IRQ, PPU, expansion, PRG
RAM, and nametable hooks are covered by benchmark output.

Before/after benchmark medians and profiling notes are recorded in
`nes-py/docs/native-hot-path-optimization-benchmarks.md`. The key measured
signal was the mapper hook smoke profile improving from `677,097.77` to
`738,052.70` iterations/s. Full-ROM frame stepping was essentially flat to
slightly positive (`855.12` to `856.72` steps/s), while render/view and
backup/restore profiles stayed within timing noise.

## Verification

Run inside `nes-py` with `.venv/bin/python`:

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_rom`
- `.venv/bin/python -m unittest discover .` (`187` tests)
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --backup-interval 200 --restore-interval 350 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --mapper-hook-profile --steps 5000 --warmup-steps 100 --json --no-progress`
- `git diff --check`

The expected Gym deprecation warning was printed during Python test and
benchmark commands.

## Commits Pushed

- `nes-py`: `3caf8d4` (`Optimize native main bus dispatch`) pushed to
  `origin/ralph-dev`.

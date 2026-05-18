# Completion Log: nes-py CPU, Bus Dispatch, and Frame Timing Optimization

## Summary

Completed work item 017 in `nes-py`.

The native CPU status register no longer uses an implementation-defined bool
bitfield union. It now stores one portable 6502 status byte with explicit masks,
status-byte push helpers, and combined zero/negative updates for hot paths.

`CPU::cycle` remains cycle-count based to preserve the existing PPU/CPU/DMA
ordering model, but opcode execution now uses a static opcode-family dispatch
table instead of trying each decoder family in sequence. No instruction-level
CPU API was introduced in this pass.

Added native smoke characterization for:

- CPU reset vectors, stack push/pop behavior, representative addressing modes,
  branch page crossing, IRQ entry, DMA cycle skipping, and status flags.
- Main-bus RAM mirroring, PPU register mirroring, controller reads, OAM DMA page
  access, expansion-area default/delegated behavior, PRG RAM, and mapper PRG
  reads/writes.

Added a packaged `nes_py.speedtest --native-hot-path-profile` benchmark that
isolates CPU dispatch, main-bus I/O dispatch, mapper CPU-cycle hook overhead for
hooked versus unhooked paths, and normal `NESEnv.step` throughput.

## Benchmarks

Baseline before this work item, collected from the pre-change branch state:

- `super-mario-bros-1.nes` public step speedtest:
  `884.79` steps/s (`1000` measured steps, `100` warmup)
- mapper hook smoke profile:
  `672,423.42` iterations/s (`5000` measured iterations, `100` warmup)

Final native hot-path profile after this work item:

- `cpu_dispatch`: `191,233,840.74` iterations/s
- `main_bus_io_dispatch`: `33,722,036.00` iterations/s
- `mapper_cycle_unhooked`: `2,891,008,962.13` iterations/s
- `mapper_cycle_hooked`: `458,883,994.13` iterations/s
- `nes_env_step`: `833.35` iterations/s (`10000` measured noop steps,
  `1000` warmup)

Final public speedtest samples after this work item:

- `super-mario-bros-1.nes` random step speedtest:
  `866.42` steps/s (`1000` measured steps, `100` warmup)
- mapper hook smoke profile:
  `617,709.71` iterations/s (`5000` measured iterations, `100` warmup)
- `the-legend-of-zelda.nes` backup/restore speedtest:
  `937.74` steps/s (`1000` measured steps, `100` warmup,
  backup interval `200`, restore interval `350`)

The final public Mario step sample is about two percent below the first baseline
sample on this machine. I investigated by repeating the benchmark after the
initial implementation, tightening status flag updates, and rerunning the
sample serially after all native profile work finished. The remaining delta is
accepted because the work item intentionally fixes the CPU status register's
portable byte layout and stack/interrupt status behavior; all current behavior
tests and new characterization tests pass, and no generated benchmark artifacts
were committed.

## Verification

Run inside `nes-py` with `.venv/bin/python`:

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_native_cpu_bus`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest nes_py.tests.test_rom`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest discover .` (`191` tests)
- `.venv/bin/python -m nes_py.speedtest --native-hot-path-profile --rom nes_py/tests/games/super-mario-bros-1.nes --steps 10000 --warmup-steps 1000 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --mapper-hook-profile --steps 5000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --backup-interval 200 --restore-interval 350 --json --no-progress`
- `git diff --check`

The expected Gym deprecation warning was printed during Python test and
benchmark commands.

## Commits Pushed

- `nes-py`: `42597816802f33baf9c1a4320634470f9e962859`
  (`Optimize CPU dispatch and characterize bus timing`) pushed to
  `origin/ralph-dev`.

# Completion Log: nes-py Native Batch RAM Info Reads

## Summary

Completed work item 051 by adding generic RAM read descriptors in `nes_py.ram`,
scalar `NESEnv.ram_values(...)`, and vector `VectorNESEmulator.ram_values(...)`
with reusable uint32 outputs. The helper supports byte, little-endian,
big-endian, packed BCD, and digit-sequence reads while keeping game-specific
address lists and reward/info logic in wrapper repositories.

## Verification

- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_ram_reads` (`5 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_speedtest` (`11 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest discover .` (`246 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --ram-profile --steps 1 --warmup-steps 0 --action-policy noop --json --no-progress`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress`
- `nes-py`: `git diff --check`

## Notes

The RAM profile in `docs/native-batch-ram-info-reads.md` shows the native helper
is not faster for tiny isolated RAM reads on this host. It is kept as a shared
validated primitive with reusable outputs and no meaningful full-loop
regression, not as a blanket replacement for direct wrapper indexing.

## Commits

- `nes-py`: `61862c9` (`p90`, pushed to `origin/p90`)
- Umbrella: included in the umbrella commit that records this completion log

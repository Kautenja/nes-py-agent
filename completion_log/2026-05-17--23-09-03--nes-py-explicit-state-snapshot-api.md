# Completion Log: nes-py Explicit State Snapshot API

## Summary

Completed spec 053 by adding an opaque `NES::Emulator::Snapshot` state model,
heap-owned native snapshot handoff for Cython, public scalar `dump_state()` and
`load_state(snapshot)`, and vector per-slot snapshot helpers. Snapshots clone
mapper state and reload through callback rewiring rather than exposing raw
native pointers or raw struct views.

## Verification

- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_nes_env` (`30 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_mappers` (`23 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest discover .` (`246 tests`, `OK`)
- `nes-py`: `build/nes-emu-release/nes_emu_tests` (`819 assertions in 71 test cases`, `OK`)
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --backup-interval 50 --restore-interval 70 --json --no-progress`
- `nes-py`: `git diff --check`

## Notes

Snapshot tests cover mappers 0, 1, 2, 3, 4, 5, 7, 9, and 69 using existing ROM
fixtures. The latency report in `docs/explicit-state-snapshot-api.md` shows
public snapshot round trips are slightly slower than the private backup slot
because they allocate independently owned snapshot objects; the API is kept for
clearer state management and vector reset plumbing, not backup/restore speed.

## Commits

- `nes-py`: `61862c9` (`p90`, pushed to `origin/p90`)
- Umbrella: included in the umbrella commit that records this completion log

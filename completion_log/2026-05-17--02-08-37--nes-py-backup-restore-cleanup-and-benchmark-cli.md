# nes-py Backup/Restore Cleanup and Benchmark CLI

## Summary

- Removed the root-level `backup_restore.py` and `speedtest.py` one-off scripts from `nes-py`.
- Added `nes_py.speedtest` with a programmatic benchmark API, `python -m nes_py.speedtest` CLI, human and JSON output, seeded action selection, warmup, and explicit backup/restore interval stress settings.
- Expanded backup/restore regression coverage to verify screen and RAM restoration, deterministic continuation after restore, and repeated backup/restore/reset cycles with valid `uint8` observations.
- Documented the benchmark command and clarified that throughput numbers are informational, not correctness criteria.

## Verification

- Local environment used `.venv/bin/python` because the host `python3` is externally managed and there is no global `python`.
- Ran `.venv/bin/python -m pip install -e .`.
- Ran `.venv/bin/python -m unittest nes_py.tests.test_nes_env`: 14 tests passed.
- Ran `.venv/bin/python -m unittest discover .`: 148 tests passed.
- Ran `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --seed 1 --no-progress`.
- Ran `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --seed 1 --backup-interval 12 --restore-interval 27 --json --no-progress`.
- Ran `git diff --check`.
- Confirmed the packaged benchmark uses explicit one-based interval semantics; the old script's truthy modulo behavior was corrected rather than preserved.
- No live tag or remote CI smoke test was required for this work item because the `nes-py` workflow does not run on arbitrary `ralph-dev` branch pushes.

## Commits Pushed

- `Kautenja/nes-py@989aa02` - `Package speedtest and cover backup restore`
- `Kautenja/gym-nes@bb36e66` - `Complete nes-py backup restore speedtest spec`

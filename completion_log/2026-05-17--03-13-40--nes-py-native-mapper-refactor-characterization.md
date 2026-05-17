# nes-py Native Mapper Refactor Characterization

## Summary

Completed the mapper characterization baseline in `nes-py`:

- Added synthetic iNES ROM helpers and focused `python -m unittest` coverage for native mappers 0, 1, 2, and 3.
- Added mapper clone support so emulator backup/restore captures mapper-visible bank state and CHR RAM.
- Added narrow native inspection hooks for mapper characterization tests.
- Added a current-mapper benchmark profile API/CLI that emits structured JSON with environment, compiler, platform, mapper, operation, elapsed time, and steps-per-second fields.
- Documented native mapper capability gaps for the follow-up mapper architecture specs.

## Verification

Run inside `nes-py` with the project `.venv` Python 3.14.2 environment:

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest nes_py.tests.test_rom`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 50 --warmup-steps 10 --json --no-progress`
- Mapper profile smoke check against synthetic mapper 0 and mapper 1 fixtures with tiny step counts.
- `.venv/bin/python -m unittest discover nes_py.tests`
- `git diff --check`

## Commits

- `nes-py`: `72dec533bb2cf70afe113fb3c1c46b6138bb08cf` pushed to `origin/ralph-dev`.
- Umbrella: this repository commit records the updated `nes-py` gitlink, archived spec, history entry, and completion log, and is pushed to `origin/main`.

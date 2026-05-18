# gym-zelda-1 Gymnasium API Migration

## Summary

- Migrated `gym-zelda-1` from legacy Gym imports and tuple contracts to Gymnasium, including registration, CLI flows, README examples, and tests.
- Updated `Zelda1Env` for `render_mode`, `reset(seed=..., options=...) -> (observation, info)`, and Gymnasium five-value step results while preserving start-screen skip and backup setup behavior.
- Preserved `Zelda1-v0`, action and observation spaces, current placeholder reward behavior, ROM package data, and stable level/position info keys.
- Kept `gym_zelda_1.make` available as an alias to `gymnasium.make` and fixed stale Mario package metadata.

## Verification

- `.venv/bin/python -m pip install --upgrade pip`
- `.venv/bin/python -m pip install -e ../nes-py`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover .` (5 tests passed)
- Focused Gymnasium smoke for `Zelda1-v0` with `render_mode="rgb_array"` (passed)
- CLI help via module and `./main.sh cli --help` (passed)

Notes:

- `python` is not on PATH in this environment, so verification used the repository virtualenv interpreter.

## Commits

- `gym-zelda-1` child submodule: `4f3b7fe2f22ac847cad82aa80c6cda2dbee471e1`, pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `gym-zelda-1` gitlink update, archive summary, history entry, and completion log.

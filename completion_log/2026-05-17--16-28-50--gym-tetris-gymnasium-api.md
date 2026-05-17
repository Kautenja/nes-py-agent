# gym-tetris Gymnasium API Migration

## Summary

- Migrated `gym-tetris` from legacy Gym imports and tuple contracts to Gymnasium, including registration, CLI flows, README examples, and tests.
- Updated `TetrisEnv` for `render_mode`, `reset(seed=..., options=...) -> (observation, info)`, and Gymnasium five-value step results.
- Preserved public environment IDs, constructor options, reward calculations, deterministic behavior, action spaces, ROM package data, and stable info keys.
- Bumped package metadata for the breaking API migration and direct Gymnasium dependency.

## Verification

- `.venv/bin/python -m pip install --upgrade pip`
- `.venv/bin/python -m pip install -e ../nes-py`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover .` (16 tests passed)
- Focused Gymnasium smoke for `TetrisA-v0` and `TetrisB-v0` with `render_mode="rgb_array"` (passed)
- CLI smoke: `.venv/bin/python -m gym_tetris._app.cli --env TetrisA-v0 --mode random --steps 1 --no-render --seed 123` (passed)
- `git diff --check` (passed)

Notes:

- `python` is not on PATH in this environment, so verification used the repository virtualenv interpreter.
- `gymnasium.utils.env_checker.check_env` passed for direct `TetrisEnv(render_mode="rgb_array")`; registered-env checker coverage was not added because it probes `human` render mode and hits headless display setup.

## Commits

- `gym-tetris` child submodule: `d77063ac936efc779c5d812b59793c0eac91768d`, pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `gym-tetris` gitlink update, archived spec, history entry, and completion log.

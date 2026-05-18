# gym-super-mario-bros Gymnasium API Migration

## Summary

- Migrated `gym-super-mario-bros` from legacy Gym imports and tuple contracts to Gymnasium, including registration, CLI flows, README examples, and tests.
- Updated `SuperMarioBrosEnv` and `SuperMarioBrosRandomStagesEnv` for `render_mode`, `reset(seed=..., options=...) -> (observation, info)`, and Gymnasium five-value step results.
- Preserved public environment IDs, ROM modes, stage IDs, action sets, reward semantics, info keys, ROM package data, and deterministic random-stage selection.
- Bumped package metadata for the breaking API migration and direct Gymnasium dependency.

## Verification

- `.venv/bin/python -m pip install --upgrade pip`
- `.venv/bin/python -m pip install -e ../nes-py`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover .` (50 tests passed)
- Focused Gymnasium smoke for `SuperMarioBros-v0`, `SuperMarioBrosRandomStages-v0`, and `SuperMarioBros1-1-v0` with `render_mode="rgb_array"` (passed)

Notes:

- `python` is not on PATH in this environment, so verification used the repository virtualenv interpreter.

## Commits

- `gym-super-mario-bros` child submodule: `4e1d4b5e6ad61aa9c14c8c0deedb201b967a28ec`, pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `gym-super-mario-bros` gitlink update, archive summary, history entry, and completion log.

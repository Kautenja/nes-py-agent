# nes-py Gymnasium API Migration

## Summary

- Replaced the legacy Gym runtime dependency with Gymnasium and bumped
  `nes-py` to `9.0.0` for the breaking API migration.
- Updated `NESEnv` to subclass `gymnasium.Env`, accept `render_mode`, expose
  Gymnasium render metadata, seed through `reset(seed=...)`, return
  `(observation, info)` from reset, and return
  `(observation, reward, terminated, truncated, info)` from step.
- Kept a deprecated `seed()` shim and `_get_done()` termination bridge for
  downstream compatibility while keeping `nes-py` tests and docs on the
  Gymnasium API.
- Updated `JoypadSpace`, play helpers, speedtest helpers, README examples, and
  application/mapper tests for Gymnasium reset, step, and render behavior.

## Verification

- `/tmp/nes-py-gymnasium-venv/bin/python -m pip install --upgrade pip`
- `/tmp/nes-py-gymnasium-venv/bin/python -m pip install -e .`
- `/tmp/nes-py-gymnasium-venv/bin/python -m pip install build`
- `/tmp/nes-py-gymnasium-venv/bin/python -m unittest nes_py.tests.test_nes_env nes_py.tests.test_joypad_space nes_py.tests.test_multiple_makes` (29 tests passed)
- `/tmp/nes-py-gymnasium-venv/bin/python -m unittest discover .` (186 tests passed)
- Gymnasium `check_env(NESEnv(...), skip_render_check=True)` against the bundled SMB1 test ROM (passed; emitted the expected warning because the deprecated `seed()` shim remains)
- `/tmp/nes-py-gymnasium-venv/bin/python -m build`
- `git diff --check`
- `rg` scan confirmed no supported code/tests/docs use legacy `gym` imports, old render calls, `env.seed(...)`, `render.modes`, or `video.frames_per_second`.

Notes:

- `python` is not on PATH in this environment.
- The system `python3` is PEP 668-managed, so verification used a temporary Python 3.13 virtualenv at `/tmp/nes-py-gymnasium-venv`.

## Commits

- `nes-py` child submodule: `e8170c74e45f21d0cebc3aac69d20819b927c26a` (`Migrate nes-py to Gymnasium API`), pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `nes-py` gitlink update, archived spec, history entry, and completion log.

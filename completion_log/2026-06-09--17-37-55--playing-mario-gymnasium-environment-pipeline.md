# Completion Log: Playing Mario Gymnasium Environment Pipeline

## Summary

Completed the Playing Mario Gymnasium environment pipeline by adding a modern
`mario_rl.envs` package with a public `make_env` factory, `MarioEnvConfig`,
JoypadSpace action-set selection, Gymnasium-compatible preprocessing wrappers,
reward accounting, record-statistics integration, and optional OpenCV MP4 video
recording.

The default training observation is a channel-first grayscale frame stack with
shape `(4, 84, 84)` and `uint8` dtype. Legacy `src/` Gym/Keras modules remain
in place for old scripts, are documented as legacy, and are not imported by the
modern `mario_rl` package surface.

## Red Checks

- `python -m unittest mario_rl.envs.tests.test_wrappers` initially failed with
  `ModuleNotFoundError: No module named 'mario_rl.envs.tests.test_wrappers'`.
- `python -m unittest mario_rl.envs.tests.test_mario_env_factory` initially
  failed with
  `ModuleNotFoundError: No module named 'mario_rl.envs.tests.test_mario_env_factory'`.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.13 venv at `/tmp/gym-nes-ralph-001-venv`.

- `/tmp/gym-nes-ralph-001-venv/bin/python -m pip install -e .`: success.
- `/tmp/gym-nes-ralph-001-venv/bin/python -m unittest mario_rl.envs.tests.test_wrappers`:
  `3 tests`, `OK`.
- `/tmp/gym-nes-ralph-001-venv/bin/python -m unittest mario_rl.envs.tests.test_mario_env_factory`:
  `6 tests`, `OK`.
- `/tmp/gym-nes-ralph-001-venv/bin/python -m pip check`:
  `No broken requirements found.`
- `/tmp/gym-nes-ralph-001-venv/bin/python -m unittest discover .`:
  `26 tests`, `OK` (`skipped=2`).
- Public factory smoke:

  ```text
  (4, 84, 84) dict 7
  ```

- `PATH=/tmp/gym-nes-ralph-001-venv/bin:$PATH ./main.sh unittest`:
  `26 tests`, `OK` (`skipped=2`).

The Gymnasium environment-version deprecation warnings for `SuperMarioBros*-v0`
were emitted during smoke tests and are expected for the spec's requested env
IDs.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `01a11e1`
  (`Add Mario Gymnasium env pipeline`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer.

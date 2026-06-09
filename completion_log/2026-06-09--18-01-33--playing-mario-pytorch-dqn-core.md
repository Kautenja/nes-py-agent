# Completion Log: Playing Mario PyTorch DQN Core

## Summary

Completed the Playing Mario PyTorch DQN core by adding active `mario_rl`
modules for native PyTorch DQN models, Dueling DQN, selected-action TD losses,
uniform replay buffers, and exploration schedules.

The legacy Keras code under `src/` remains isolated. The new active model path
does not import Keras or TensorFlow, reads dimensions and architecture from the
typed config, handles terminal and truncated transitions explicitly, and keeps
prioritized replay behind a tested unsupported config path for the first
Lightning pass.

## Red Checks

- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.models.tests`
  initially failed because `mario_rl.models.DQN` did not exist.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.replay.tests`
  initially failed because `mario_rl.replay.UniformReplayBuffer` did not exist.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_schedules`
  initially failed because `mario_rl.schedules` did not exist.
- A bare Homebrew `python3 -m unittest discover .` failed before implementation
  because that interpreter did not have the project dependencies installed; the
  verified path used the existing submodule `.venv`.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`.

- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.models.tests`:
  `10 tests`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.replay.tests`:
  `4 tests`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_schedules`:
  `3 tests`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest discover .`:
  `70 tests`, `OK` (`skipped=2`).
- `PATH="$PWD/.venv/bin:$PATH" python3 - <<'PY' ...` DQN smoke snippet:
  printed `torch.Size([2, 7])`.

The Gymnasium environment-version deprecation warnings for `SuperMarioBros*-v0`
remain expected for the current wrapper IDs.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `586635e`
  (`Add PyTorch DQN core`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer.

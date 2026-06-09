# Completion Log: Playing Mario Config CLI Project Layout

## Summary

Completed the Playing Mario config CLI project layout by adding a typed
`mario_rl.config` package, packaged YAML config discovery, nested config
overrides, import-safe train/play/random entrypoints, `main.sh` command routing,
and README examples for the new command surface.

The config tree now covers experiment identity, artifact paths, trainer/device
selection, Gymnasium environment preprocessing, replay settings, DQN model
settings, epsilon schedules, training limits, checkpoint names, and evaluation
settings. Train and play are intentionally config-reporting placeholders until
the PyTorch DQN and Lightning specs implement active learning behavior.

## Red Checks

- `python3 -m unittest discover .` under the default Homebrew Python initially
  failed because the interpreter did not have the project runtime dependencies
  installed (`gym_super_mario_bros`, `numpy`, and related packages).
- After installing the editable project in `.venv`, full discovery initially
  failed because the new entrypoint import-safety test assumed
  `gym_super_mario_bros` was absent globally. Earlier env tests can import it
  first, so the test was corrected to assert the help path does not newly
  import env modules.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with a fresh local
Python 3.14 venv at `.venv`.

- `python3 -m venv .venv`: success.
- `.venv/bin/python -m pip install --upgrade pip setuptools wheel`: success.
- `.venv/bin/python -m pip install -e ../nes-py -e ../gym-super-mario-bros -e .`:
  success.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.config.tests`:
  `5 tests`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_entrypoints`:
  `3 tests`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m mario_rl.config list`:
  `smb_dqn_cpu`, `smb_dqn_fast_dev`, `smb_dqn_mps`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m mario_rl.config path smb_dqn_fast_dev`:
  printed the packaged YAML path under `mario_rl/config/data/`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m mario_rl.train --help`: success,
  generated nested config help.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m mario_rl.play --help`: success,
  generated nested config help.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh`: success, printed command help.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh config list`: success.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh train --config smb_dqn_fast_dev --train.fast_dev_run true --env.id SuperMarioBros1-1-v0`:
  success, printed a resolved config JSON payload with the overrides applied.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh play --config smb_dqn_fast_dev --eval.checkpoint runs/example.ckpt`:
  success, printed a resolved config JSON payload.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh random --help`: success, generated
  nested config help for the random rollout command.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m pip check`:
  `No broken requirements found.`
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest discover .`:
  `39 tests`, `OK` (`skipped=2`).
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh unittest`:
  `39 tests`, `OK` (`skipped=2`).

The Gymnasium environment-version deprecation warnings for `SuperMarioBros*-v0`
were emitted during env tests and remain expected for the current wrapper IDs.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `f8492a6`
  (`Add config-driven Mario CLI layout`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer.

# Completion Log: Playing Mario Universal Action Space

## Summary

Completed universal action-space support for
`playing-mario-with-deep-reinforcement-learning`.

The learner now resolves `nes`, `right`, `right_only`, `simple`, and `complex`
through a single action metadata path. The `nes` action set skips `JoypadSpace`
and keeps the native 256-action NES controller space. `right` canonicalizes to
the existing `right_only` constrained list.

Packaged configs now request `model.num_actions: auto`, and runtime config
resolution converts that to a concrete integer model head from the configured
action set. Fixed numeric counts remain supported and fail fast when they do
not match the resolved action count. Train, play, random rollout, metrics, eval
JSON, and MacBook gate summaries report the resolved action set and action
count.

README guidance documents `simple` as the intentional default for fast local
smoke training, while noting that universal all-game training may prefer the
native `nes` action space or the broader `complex` constrained subset.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`. The shell did not provide a `python`
executable, so direct unittest commands used `.venv/bin/python`.

- `.venv/bin/python -m unittest mario_rl.envs.tests.test_mario_env_factory`:
  `11 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`:
  `7 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.models.tests.test_models`:
  `8 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli`:
  `1 test`, `OK`.
- `.venv/bin/python -m unittest mario_rl.tests.test_play_cli`:
  `1 test`, `OK`.
- `.venv/bin/python -m unittest discover .`:
  `117 tests`, `OK` (`skipped=7`).
- `./main.sh random --config smb_dqn_fast_dev --env.action_set nes --env.max_smoke_steps 8`:
  reported `action_set=nes`, `action_count=256`, `native_action_space=true`,
  `steps=8`.
- `./main.sh unittest`:
  `117 tests`, `OK` (`skipped=7`).
- `./main.sh verify-macbook`:
  passed CPU and MPS with no budget warnings. CPU summary: train `2.48s`,
  eval `2.33s`, env FPS `12.93`, optimizer `2.83` steps/s, actions
  `simple:7`. MPS summary: train `2.74s`, eval `2.31s`, env FPS `11.68`,
  optimizer `2.55` steps/s, actions `simple:7`.
- `./main.sh verify-macbook --device mps`:
  passed with no budget warnings; train `2.50s`, eval `2.01s`, env FPS
  `12.82`, optimizer `2.81` steps/s, actions `simple:7`.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `7317557`
  (`Add universal Mario action space sizing`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

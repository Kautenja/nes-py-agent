# Completion Log: Playing Mario Task Suite Curriculum

## Summary

Completed task-suite curriculum sampling for
`playing-mario-with-deep-reinforcement-learning`.

The learner now has a typed `TaskSuiteConfig` and metadata-only `TaskSuite`
resolver that works from `MarioTask` records without constructing environments.
Suites support game-family, single-stage/full-game, train/eval split,
validation-status, alias, explicit env ID, world, and stage filters. Sampling
is deterministic for a fixed seed and chooses a family first using per-family
weights, which prevents large SMB1 and Lost Levels catalogs from dominating
smaller SMB2 USA and SMB3 task sets by raw count.

The suite exposes the full SMB3 stage matrix for catalog/reporting while
training candidates remain restricted to registered validated reset entries.
The Lightning DQN training loop can switch tasks at episode boundaries or by a
configured episode interval, recreating the env only when the sampled env ID
changes. The existing single-env config path remains unchanged, and
task-conditioned models refresh replay/task features when the sampled task
changes.

Added `smb_dqn_task_suite_fast_dev` as a tiny deterministic SMB1/SMB3
task-conditioned smoke config and updated README guidance to use task-suite
sampling instead of the removed `SuperMarioBrosRandomStages-*` environment
family.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`. The shell did not provide a `python`
executable, so direct unittest commands used `.venv/bin/python`.

- `.venv/bin/python -m unittest mario_rl.envs.tests.test_task_suites`:
  `6 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.envs.tests.test_mario_env_factory`:
  `8 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`:
  `5 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`:
  `10 tests`, `OK` (`skipped=1`).
- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli`:
  `1 test`, `OK`.
- `.venv/bin/python -m unittest discover .`:
  `108 tests`, `OK` (`skipped=7`).
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`:
  wrote the standard fast-dev artifacts and reported `env_frames=128`,
  `global_step=25`.
- `./main.sh train --config smb_dqn_task_suite_fast_dev`:
  wrote `runs/smb_dqn_task_suite_fast_dev/checkpoints/task-suite-fast-dev.ckpt`,
  `runs/smb_dqn_task_suite_fast_dev/train-metrics.csv`, and
  `runs/smb_dqn_task_suite_fast_dev/resolved-config.yaml`; reported
  `env_frames=32`, `global_step=7`.
- `./main.sh unittest`:
  `108 tests`, `OK` (`skipped=7`).
- `./main.sh verify-macbook`:
  passed CPU and MPS with no budget warnings. CPU summary: train `2.40s`,
  eval `2.24s`, env FPS `13.36`, optimizer `2.92` steps/s, summary
  `runs/smb_dqn_macbook_gate_cpu/macbook-gate-summary.json`. MPS summary:
  train `2.66s`, eval `2.07s`, env FPS `12.04`, optimizer `2.63` steps/s,
  summary `runs/smb_dqn_macbook_gate_mps/macbook-gate-summary.json`.
- `./main.sh verify-macbook --device mps`:
  passed with no budget warnings; train `2.78s`, eval `2.22s`, env FPS
  `11.50`, optimizer `2.51` steps/s.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `46b7eee`
  (`Add Mario task suite curriculum`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

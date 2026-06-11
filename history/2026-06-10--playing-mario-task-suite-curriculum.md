# Playing Mario Task Suite Curriculum

Completed the task-suite curriculum for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `TaskSuiteConfig` and `TaskSuite` on top of the existing
  `MarioTask` metadata API, resolving candidates without constructing
  ROM-backed environments.
- Supported game-family, single-stage/full-game, train/eval split,
  validation-status, alias, env ID, world, and stage filters, plus deterministic
  seeded sampling and per-family weights.
- Family-first weighted sampling keeps large SMB1 and Lost Levels catalogs from
  automatically swamping smaller SMB2 USA and SMB3 task sets.
- Added SMB3 full-catalog reporting through the suite while keeping training
  candidates restricted to registered validated reset entries.
- Integrated task-suite sampling into the Lightning DQN loop at episode
  boundaries, preserving the default single-env path and refreshing task
  features when a task-conditioned model switches tasks.
- Added `smb_dqn_task_suite_fast_dev`, a tiny deterministic SMB1/SMB3
  task-conditioned smoke config, and updated README guidance away from removed
  `SuperMarioBrosRandomStages-*` IDs.

Verification highlights:

- Full `mario_rl` unittest discovery passed with 108 tests and 7 skips.
- `./main.sh unittest` passed with 108 tests and 7 skips.
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=25`.
- `./main.sh train --config smb_dqn_task_suite_fast_dev` passed with
  `env_frames=32` and `global_step=7`.
- `./main.sh verify-macbook` passed on CPU and MPS with no budget warnings.
  CPU summary: train `2.40s`, eval `2.24s`, env FPS `13.36`, optimizer
  `2.92` steps/s. MPS summary: train `2.66s`, eval `2.07s`, env FPS `12.04`,
  optimizer `2.63` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with train `2.78s`,
  eval `2.22s`, env FPS `11.50`, and optimizer `2.51` steps/s.

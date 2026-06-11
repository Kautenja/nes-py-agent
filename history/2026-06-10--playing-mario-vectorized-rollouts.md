# Playing Mario Vectorized Rollouts

Completed vectorized PPO rollout collection for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added typed `ppo.num_envs` configuration with compatibility default `1` and
  updated `smb_ppo_fast_dev` to exercise two rollout environments.
- Refactored `PPOLightningModule` to keep one live env, active task ID,
  observation, recurrent hidden slot, episode index, and metric episode per
  vector slot.
- Kept the policy pixel-only: task IDs, rewards, and `info` remain metadata for
  resets, metrics, task features when explicitly configured, and artifacts.
- Reset hidden state only for terminated/truncated slots while preserving
  unfinished slots, and sampled task-suite episodes independently per slot.
- Extended metrics to track multiple active episodes, preserving per-task and
  per-family summaries across vector slots.
- Added single-environment play/evaluation support for PPO checkpoints so the
  vectorized training checkpoint remains compatible with existing CLI flows.
- Logged and persisted `ppo_num_envs` in Lightning metrics, CSV metrics,
  structured train JSON, and resolved config artifacts.
- Updated `verify-macbook` to default to the vectorized PPO fast-dev config;
  the previous DQN gate remains available by explicit config.
- Added top-level import shims for `mario_rl.random` and `mario_rl.lightning`
  so the exact `python -m unittest discover mario_rl` command does not shadow
  stdlib `random` or the external `lightning` package.

Verification highlights:

- `python -m unittest mario_rl.tests.test_actor_critic mario_rl.lightning.tests.test_module`
  passed in the project `.venv`.
- `python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_metrics`
  passed in the project `.venv`; `test_play_cli` and `test_verify_macbook`
  were also run with the focused set.
- `python -m unittest discover mario_rl` passed with 162 tests and 2 skips.
- `./main.sh unittest` passed with 162 tests and 2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed and wrote `ppo_num_envs=2`, `env_frames=128`, and `global_step=8`.
- `./main.sh verify-macbook --device cpu` passed with no warnings; train
  `2.55s`, eval `2.16s`, env FPS `50.27`, optimizer `3.14` steps/s.
- `./main.sh verify-macbook --device mps` passed with no warnings; train
  `4.21s`, eval `2.14s`, env FPS `30.39`, optimizer `1.90` steps/s.

# Playing Mario Reward Transform Pipeline

Completed configurable reward transforms for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `RewardTransformConfig` and `RewardTransformer` with `env`, `sign`,
  `unclipped`, `clipped`, and `component_weights` modes.
- Changed packaged learner configs to use `reward_transform.mode: env` and
  disabled the legacy sign-clipping wrapper by default, leaving sign clipping
  available as an explicit baseline mode.
- Added explicit missing-field policies for total reward fields and
  missing-component policies for component-weight transforms.
- Extended replay batches with optional `env_reward`, `raw_reward`,
  `unclipped_reward`, and `clipped_reward` arrays/tensors while keeping the
  training reward in the existing `reward` field.
- Added reward transform metadata to train JSON/CSV artifacts and preserved the
  resolved config as the full reproducibility source.
- Aggregated reward diagnostics across `MaxFrameskipEnv` substeps so
  unclipped, clipped, and component-weight transforms see the same temporal
  unit as the reward returned to training.
- Documented why sign clipping is no longer the default for modern Mario
  training and how to opt back into it.

Verification highlights:

- Focused reward/config/replay/Lightning tests passed with 32 tests and one
  expected skip.
- Full `mario_rl` unittest discovery passed with 126 tests and 7 skips.
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128`, `global_step=25`, and
  `reward_transform_mode=env`.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings. CPU
  summary: train `2.70s`, eval `2.24s`, env FPS `11.87`, optimizer `2.60`
  steps/s. MPS summary: train `3.22s`, eval `2.26s`, env FPS `9.93`,
  optimizer `2.17` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with no budget
  warnings; train `3.00s`, eval `2.40s`, env FPS `10.66`, optimizer `2.33`
  steps/s.

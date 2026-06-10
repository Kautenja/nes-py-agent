# Playing Mario Auxiliary Losses

Completed optional PPO auxiliary losses for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `AuxiliaryLossConfig` and a packaged `smb_ppo_auxiliary_fast_dev`
  smoke config. Auxiliary losses remain disabled unless `auxiliary.enabled` is
  set.
- Supported auxiliary targets are `progress_delta`,
  `progress_normalized`, `clear`, `death`, `transformed_reward`,
  `reward_total_unclipped`, `reward_total_clipped`, and `game_family`.
- Added `mario_rl.auxiliary` target extraction with explicit per-target
  missing-value masks so unavailable `info` fields do not train on default
  values.
- Extended recurrent actor-critic models with optional GRU-shared auxiliary
  heads and added masked regression, binary, and classification losses.
- Extended rollout storage and PPO optimization to carry auxiliary targets,
  combine weighted auxiliary loss with PPO loss, checkpoint the latest
  auxiliary state, and log each auxiliary term plus valid label counts.
- Persisted PPO and auxiliary loss summaries in train metrics JSON and CSV
  artifacts.
- Updated fake environments to provide deterministic normalized Mario metadata
  for ROM-free auxiliary tests.

Verification highlights:

- Focused model, Lightning, config, loss, rollout, auxiliary, and train CLI
  tests passed.
- Full unittest discovery and `./main.sh unittest` passed with 160 tests and
  7 skips.
- `./main.sh train --config smb_ppo_auxiliary_fast_dev
  --trainer.enable_progress_bar false` passed with `env_frames=32` and
  `global_step=4`, wrote `ppo-auxiliary-fast-dev.ckpt`, and persisted
  per-target auxiliary losses/valid counts for `progress_delta`, `clear`,
  `death`, `transformed_reward`, and `game_family`.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings. CPU
  summary: train `2.31s`, eval `2.20s`, env FPS `13.87`, optimizer
  `3.03` steps/s. MPS summary: train `2.76s`, eval `2.16s`, env FPS
  `11.58`, optimizer `2.53` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with no warnings;
  train `2.92s`, eval `2.26s`, env FPS `10.97`, optimizer `2.40` steps/s.

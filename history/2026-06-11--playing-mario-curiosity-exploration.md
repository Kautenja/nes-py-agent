# Playing Mario Curiosity Exploration

Completed pixel-only curiosity exploration for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added a disabled-by-default `exploration` config section for Random Network
  Distillation settings, including intrinsic reward scale, predictor learning
  rate, observation and intrinsic reward normalization toggles, clipping,
  warmup scaling, logging, and the documented `next_observation` source.
- Implemented a pixel-only RND module with a frozen target network and trainable
  predictor network. The RND path consumes only channel-first policy pixel
  observations and does not accept RAM, `info`, task IDs, reward components, or
  progress labels.
- Integrated RND with recurrent PPO rollout collection by computing intrinsic
  rewards from the next pixel observation batch, updating only the predictor,
  and storing total PPO training reward separately from transformed, intrinsic,
  environment, raw, unclipped, and clipped reward diagnostics.
- Added Lightning scalar logs, one-row CSV fields, and structured JSON artifact
  fields for exploration settings, intrinsic reward totals/means, RND raw
  error, predictor loss, and predictor gradient norm.
- Added the packaged `smb_ppo_rnd_fast_dev` real Mario smoke config and README
  documentation for the RND input choice and reward accounting.

Verification highlights:

- `.venv/bin/python -m unittest mario_rl.models.tests.test_models mario_rl.tests.test_train_cli`
  passed with 18 tests.
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module` passed
  with 20 tests and 1 skip.
- `.venv/bin/python -m unittest discover mario_rl` passed with 193 tests and
  2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=8`.
- `./main.sh train --config smb_ppo_rnd_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128`, `global_step=8`, and nonzero intrinsic reward,
  RND loss, and predictor gradient norm artifacts.
- `./main.sh verify-macbook --device cpu` passed with train `2.52s`, eval
  `2.13s`, env FPS `50.77`, and optimizer `3.17` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.23s`, eval
  `2.13s`, env FPS `39.63`, and optimizer `2.48` steps/s.

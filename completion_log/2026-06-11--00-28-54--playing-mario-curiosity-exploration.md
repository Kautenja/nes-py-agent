# Playing Mario Curiosity Exploration

Completed spec `018-playing-mario-curiosity-exploration.md`.

## Summary

- Added a disabled-by-default `exploration` config section and a packaged
  `smb_ppo_rnd_fast_dev` smoke config for opt-in PPO RND curiosity.
- Implemented pixel-only Random Network Distillation with a frozen target
  network, trainable predictor, deterministic fixed-seed behavior, clipped and
  scaled intrinsic rewards, and documented `next_observation` inputs.
- Threaded intrinsic reward into recurrent PPO rollout collection while keeping
  environment, raw, transformed, intrinsic, and total PPO training rewards
  separately logged and persisted.
- Added Lightning scalar, CSV, JSON, config, module, train-artifact, and direct
  RND unit coverage.
- Documented the RND input choice and reward accounting in the README.
- Retired the completed spec from the active root queue.

## Verification

- `.venv/bin/python -m unittest mario_rl.models.tests.test_models mario_rl.tests.test_train_cli`
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`
- `.venv/bin/python -m unittest discover mario_rl`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh train --config smb_ppo_rnd_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The CPU and MPS MacBook gates reported no warnings.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `3300a18` (`Add PPO RND curiosity exploration`)
- umbrella repository: this commit (`Complete Mario curiosity exploration spec`)

# Playing Mario Vectorized Rollouts

Completed spec `014-playing-mario-vectorized-rollouts.md`.

## Summary

- Added vectorized recurrent PPO rollout collection with configurable
  `ppo.num_envs`.
- Updated the packaged PPO fast-dev and MacBook gate paths to use two rollout
  environments.
- Preserved pixel-only policy observations while keeping task/reward/info
  metadata available for metrics, resets, and explicit task features.
- Added slot-aware active metrics, per-slot hidden-state reset behavior,
  vector rollout tests, PPO checkpoint play support, and artifact fields for
  resolved vector settings.
- Retired the completed spec from the active root queue.

## Verification

- `python -m unittest mario_rl.tests.test_actor_critic mario_rl.lightning.tests.test_module`
- `python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_metrics`
- `python -m unittest discover mario_rl`
- `./main.sh unittest`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The CPU and MPS MacBook gates reported no warnings.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `f42c513` (`Add vectorized PPO rollouts`)
- umbrella repository: this commit (`Complete Mario vectorized rollouts spec`)

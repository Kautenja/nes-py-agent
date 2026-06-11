# Playing Mario Prioritized Replay

Completed spec `019-playing-mario-prioritized-replay.md`.

## Summary

- Added an opt-in proportional prioritized replay buffer for DQN while keeping
  uniform replay as the default.
- Extended replay batches with prioritized-only sample indices and normalized
  importance-sampling weights.
- Applied importance weights to per-sample SmoothL1 TD losses and updated
  priorities after each DQN optimizer step from absolute TD error plus epsilon.
- Added replay metadata to train JSON/CSV artifacts and DQN checkpoint state.
- Added the packaged `smb_dqn_prioritized_fast_dev` smoke config, docs, and
  focused replay/loss/module/train artifact tests.
- Retired the completed spec from the active root queue.

## Verification

- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.replay.tests.test_replay mario_rl.models.tests.test_losses mario_rl.lightning.tests.test_module mario_rl.tests.test_train_cli`
- `PATH=".venv/bin:$PATH" python -m unittest discover mario_rl`
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
- `./main.sh train --config smb_dqn_prioritized_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The prioritized DQN smoke recorded
`priority_updates=200`, nontrivial importance weights, `env_frames=128`, and
`global_step=25`. The CPU gate reported train `2.55s`, eval `2.13s`, env FPS
`50.18`, and optimizer `3.14` steps/s. The MPS gate reported train `3.33s`,
eval `2.15s`, env FPS `38.42`, and optimizer `2.40` steps/s.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `cdf6060` (`Add prioritized DQN replay`)
- umbrella repository: this commit (`Complete Mario prioritized replay spec`)

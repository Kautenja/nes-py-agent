# Playing Mario Prioritized Replay

Completed opt-in prioritized replay for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `PrioritizedReplayBuffer` as a proportional replay-buffer variant for
  the existing DQN replay surface, while leaving uniform replay as the default
  and preserving uniform batches with no indices or importance weights.
- Prioritized batches now carry replay indices and normalized importance
  weights. DQN applies those weights to per-sample SmoothL1 TD losses and
  updates priorities after each optimizer step from absolute TD error plus
  epsilon.
- Honored the existing `replay.prioritized`, `priority_alpha`, and
  `priority_beta` config fields, and added the packaged
  `smb_dqn_prioritized_fast_dev` smoke config.
- Persisted replay sampling metadata in train JSON/CSV artifacts and DQN
  checkpoint state, including prioritized status, alpha/beta, epsilon, priority
  update count, priority summaries, and latest importance-weight mean.
- Documented the opt-in prioritized replay path without adding RAM, `info`,
  reward components, object maps, or tile maps to model observations.

Verification highlights:

- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.replay.tests.test_replay mario_rl.models.tests.test_losses mario_rl.lightning.tests.test_module mario_rl.tests.test_train_cli`
  passed with 45 tests and 1 skip.
- `PATH=".venv/bin:$PATH" python -m unittest discover mario_rl` passed with
  202 tests and 2 skips.
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=25`.
- `./main.sh train --config smb_dqn_prioritized_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128`, `global_step=25`, `priority_updates=200`, and
  nontrivial importance weights.
- `./main.sh verify-macbook --device cpu` passed with train `2.55s`, eval
  `2.13s`, env FPS `50.18`, and optimizer `3.14` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.33s`, eval
  `2.15s`, env FPS `38.42`, and optimizer `2.40` steps/s.

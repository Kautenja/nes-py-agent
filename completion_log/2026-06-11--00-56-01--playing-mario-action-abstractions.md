# Playing Mario Action Abstractions

Completed spec `020-playing-mario-action-abstractions.md`.

## Summary

- Added opt-in macro actions for Mario training as named deterministic
  sequences of resolved Joypad action indices.
- Preserved all primitive Joypad actions in macro mode and added a conservative
  default movement set with run-right, short/full jump, run-jump, hold-left,
  crouch when available, and wait actions.
- Aggregated macro rewards, raw/unclipped/clipped diagnostics, reward
  components, and `frames_skipped` with the same rules as frame skip.
- Made automatic model action sizing resolve to the macro action count when
  macros are enabled while keeping native NES 256-action mode available when
  macros are disabled.
- Exposed macro metadata in train, play, eval-matrix, random, resolved config,
  and train CSV/JSON artifacts.
- Added `smb_ppo_macro_fast_dev`, README documentation, wrapper/factory/config
  tests, macro train/play artifact tests, and random payload coverage.
- Retired the completed spec from the active root queue.

## Verification

- `.venv/bin/python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.envs.tests.test_mario_env_factory mario_rl.config.tests.test_config mario_rl.tests.test_train_cli mario_rl.tests.test_play_cli mario_rl.tests.test_random_cli`
- `.venv/bin/python -m unittest discover mario_rl`
- `./main.sh train --config smb_ppo_macro_fast_dev --trainer.enable_progress_bar false`
- `./main.sh play --config smb_ppo_macro_fast_dev --trainer.enable_progress_bar false`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The macro PPO smoke recorded `action_count=19`,
`env_frames=388`, and `global_step=8`; macro play loaded the checkpoint and ran
`total_steps=32`. The baseline PPO smoke recorded `env_frames=128` and
`global_step=8`. The CPU gate reported train `2.61s`, eval `2.38s`, env FPS
`49.13`, and optimizer `3.07` steps/s. The MPS gate reported train `3.77s`,
eval `2.56s`, env FPS `33.91`, and optimizer `2.12` steps/s.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `6d8147c` (`Add Mario macro action abstractions`)
- umbrella repository: this commit (`Complete Mario action abstractions spec`)

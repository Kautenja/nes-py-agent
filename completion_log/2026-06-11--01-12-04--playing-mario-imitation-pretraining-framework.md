# Playing Mario Imitation Pretraining Framework

Completed spec `021-playing-mario-imitation-pretraining-framework.md`.

## Summary

- Added a documented, pixel-only local demonstration format using `.npz`
  segment files plus JSON metadata.
- Added a deterministic imitation loader with validation for action-space,
  macro-action, image-profile, channel, image-size, frame-stack, label-range,
  and episode-boundary contracts.
- Added recurrent-PPO behavior-cloning pretraining, metrics artifacts, action
  histograms, validation accuracy logging, and marked imitation checkpoints.
- Made the normal train command load imitation checkpoints as policy weights
  before continuing RL smoke training.
- Added `./main.sh pretrain`, `smb_ppo_imitation_fast_dev`, ignored
  `data/imitation/`, README documentation, and synthetic unittest fixtures.
- Retired the completed spec from the active root queue.

## Verification

- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_entrypoints mario_rl.tests.test_imitation`
- `.venv/bin/python -m unittest discover mario_rl`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`
- Temporary synthetic dataset CLI check:
  `./main.sh pretrain --config smb_ppo_imitation_fast_dev ...` followed by
  `./main.sh train --config smb_ppo_fast_dev --train.checkpoint_path ...`

All required verification passed. The full `mario_rl` suite passed with 213
tests and 2 skips. The baseline PPO smoke recorded `env_frames=128` and
`global_step=8`. The CPU gate reported train `2.54s`, eval `2.14s`, env FPS
`50.40`, and optimizer `3.15` steps/s. The MPS gate reported train `3.25s`,
eval `2.14s`, env FPS `39.43`, and optimizer `2.46` steps/s. The CLI
pretrain/train-from-pretrain check wrote an imitation checkpoint and completed
default PPO smoke training from it with `env_frames=128` and `global_step=8`.

Additional note: `.venv/bin/python -m unittest tests.test_package_layout tests.test_dependency_contract`
was run as an extra non-required check and still fails on the pre-existing
missing legacy `src` package expected by `tests/test_package_layout.py`.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `6068948` (`Add Mario imitation pretraining`)
- umbrella repository: this commit (`Complete Mario imitation pretraining spec`)

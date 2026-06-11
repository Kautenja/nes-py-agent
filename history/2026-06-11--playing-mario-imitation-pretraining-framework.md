# Playing Mario Imitation Pretraining Framework

Completed the local demonstration and behavior-cloning pretraining framework
for `playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `mario_rl.imitation` with a pixel-only `.npz` dataset contract,
  required JSON metadata, forbidden non-pixel policy-input checks, deterministic
  shuffling, and train/validation splits.
- Validated demonstration action count, action set, macro-action settings,
  pixel profile, channel count, image size, frame stack, channel layout, action
  label range, and episode boundary or terminated/truncated flags.
- Added recurrent actor-critic behavior cloning that trains from pixel tensors
  and action labels only, logs cross-entropy and validation accuracy, writes an
  action histogram and dataset-size metrics, and saves a marked Lightning
  checkpoint.
- Updated the normal train command to detect imitation checkpoints in
  `train.checkpoint_path`, load policy weights, and continue PPO smoke training
  without restoring the pretraining loop state.
- Added `./main.sh pretrain`, the packaged `smb_ppo_imitation_fast_dev` config,
  README instructions for local ignored demonstrations, and a dev version bump
  to `6.0.0.dev1`.

Verification highlights:

- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_entrypoints mario_rl.tests.test_imitation`
  passed with 13 tests.
- `.venv/bin/python -m unittest discover mario_rl` passed with 213 tests and
  2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=8`.
- `./main.sh verify-macbook --device cpu` passed with train `2.54s`, eval
  `2.14s`, env FPS `50.40`, and optimizer `3.15` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.25s`, eval
  `2.14s`, env FPS `39.43`, and optimizer `2.46` steps/s.
- A temporary synthetic `.npz` demo verified `./main.sh pretrain` writes an
  imitation checkpoint and `./main.sh train --train.checkpoint_path ...`
  can continue default PPO smoke training from it.

Note: an extra non-required root-level run of
`.venv/bin/python -m unittest tests.test_package_layout tests.test_dependency_contract`
still fails on the pre-existing missing legacy `src` package expected by
`tests/test_package_layout.py`; the required `mario_rl` suite passed.

# Playing Mario Emulator Snapshot Curriculum

Completed process-local emulator snapshot curriculum support for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Reused the existing public `nes-py` opaque snapshot API without lower-level
  emulator changes.
- Added a `mario_rl.snapshots` library that captures process-local native
  snapshots, copied pixel observations, and wrapper state while persisting only
  JSON-safe metadata.
- Added compatibility keys based on env ID, action set, wrapper stack,
  observation shape, ROM SHA-256/size, and installed emulator/wrapper package
  versions.
- Added snapshot metadata for seed lineage, progress, episode step, task ID,
  tags, rank score, and rank reasons, with ranked sampling and normal-reset
  fallback behavior.
- Wired DQN and vectorized recurrent PPO reset paths to sample compatible
  snapshot starts and capture non-terminal candidates during training.
- Added snapshot-start episode metrics plus full-reset clear counts so
  hard-section starts do not inflate full-level progress.
- Documented the public snapshot contract, process-local limitation, durable
  serialization constraints, and pixel-only policy boundary in the README.

Verification highlights:

- `python -m unittest nes_py.tests.test_nes_env nes_py.tests.test_ram_reads`
  passed with 35 tests.
- `python -m unittest discover nes_py` passed with 246 tests.
- `python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.tests.test_train_cli`
  passed with 15 tests.
- `python -m unittest discover mario_rl` passed with 175 tests and 2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=8`.
- `./main.sh verify-macbook --device cpu` passed with train `2.83s`, eval
  `2.56s`, env FPS `45.28`, and optimizer `2.83` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.77s`, eval
  `2.47s`, env FPS `33.95`, and optimizer `2.12` steps/s.

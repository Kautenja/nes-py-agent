# Playing Mario Action Abstractions

Completed opt-in macro action abstractions for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added a configurable macro-action resolver and `MacroActionEnv` wrapper that
  exposes named deterministic sequences of existing Joypad action indices.
- Kept every selected Joypad primitive action available as a one-step macro,
  then added the conservative movement set: `run_right`, `short_jump`,
  `full_jump`, `run_jump`, `hold_left`, `crouch` when down is available, and
  `wait`.
- Placed macro execution after frame-skip and before image preprocessing so a
  macro step aggregates the underlying frame-skipped Joypad steps and stops
  immediately on termination or truncation.
- Reused the frame-skip reward diagnostic aggregation rules for raw reward,
  unclipped/clipped totals, reward components, and executed `frames_skipped`.
- Added `env.macro_actions` and `env.macro_action_set` config fields,
  macro-aware automatic model action-head sizing, and macro metadata in
  train/play/eval-matrix/random payloads plus train CSV/JSON artifacts.
- Added the packaged `smb_ppo_macro_fast_dev` smoke config and README
  documentation for macro actions, native NES action compatibility, and
  frame-skip interaction.

Verification highlights:

- `.venv/bin/python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.envs.tests.test_mario_env_factory mario_rl.config.tests.test_config mario_rl.tests.test_train_cli mario_rl.tests.test_play_cli mario_rl.tests.test_random_cli`
  passed with 49 tests.
- `.venv/bin/python -m unittest discover mario_rl` passed with 210 tests and
  2 skips.
- `./main.sh train --config smb_ppo_macro_fast_dev --trainer.enable_progress_bar false`
  passed with `action_count=19`, `env_frames=388`, and `global_step=8`.
- `./main.sh play --config smb_ppo_macro_fast_dev --trainer.enable_progress_bar false`
  loaded the macro checkpoint and passed with `total_steps=32`.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128` and `global_step=8`.
- `./main.sh verify-macbook --device cpu` passed with train `2.61s`, eval
  `2.38s`, env FPS `49.13`, and optimizer `3.07` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.77s`, eval
  `2.56s`, env FPS `33.91`, and optimizer `2.12` steps/s.

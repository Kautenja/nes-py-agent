# Playing Mario Pixel Fidelity

Completed explicit pixel fidelity profiles for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added a named pixel-observation profile registry for the fast grayscale
  baseline, a balanced RGB laptop profile, and a higher-fidelity RGB profile.
- Declared `env.pixel_profile` across packaged configs and added
  `smb_ppo_rgb_fast_dev` plus `smb_ppo_rgb_high_fidelity`.
- Resolved `replay.state_shape` and `model.input_channels` from preprocessing
  settings when omitted, and failed clearly when explicit shapes/channels
  disagreed with RGB/grayscale, image size, or frame stack settings.
- Added structured train artifact metadata for pixel profile, grayscale/RGB
  mode, image size, frame stack, input channels, state shape, dtype, and
  per-observation bytes.
- Kept policy observations pixel-only; RAM, `info`, reward components, object
  maps, and tile maps were not added to model observation tensors.
- Documented grayscale, balanced RGB, and high-fidelity RGB tradeoffs with
  approximate memory costs and a real RGB fast-dev train command.

Verification highlights:

- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.config.tests.test_config mario_rl.models.tests.test_models`
  passed with 24 tests.
- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.envs.tests.test_mario_env_factory`
  passed with 12 tests.
- `PATH=".venv/bin:$PATH" python -m unittest discover mario_rl` passed with
  187 tests and 2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128`, `global_step=8`, and
  `pixel_profile=grayscale_84`.
- `./main.sh train --config smb_ppo_rgb_fast_dev --trainer.enable_progress_bar false`
  passed with `env_frames=128`, `global_step=8`, and RGB
  `state_shape=[12, 90, 96]`.
- `./main.sh verify-macbook --device cpu` passed with train `2.56s`, eval
  `2.13s`, env FPS `50.10`, and optimizer `3.13` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.31s`, eval
  `2.24s`, env FPS `38.67`, and optimizer `2.42` steps/s.

# Playing Mario Pixel Fidelity

Completed spec `017-playing-mario-pixel-fidelity.md`.

## Summary

- Added explicit grayscale/RGB pixel-observation profiles and packaged RGB PPO
  configs for laptop smoke and higher-fidelity experiments.
- Resolved or validated replay state shapes and model input channels from
  grayscale/RGB mode, image size, frame stack, channel order, and interpolation.
- Exposed pixel profile metadata in resolved configs and structured train JSON
  artifacts.
- Added config, model, environment factory, fake-env, train artifact, and
  vectorized PPO rollout storage coverage for RGB observations.
- Documented when to choose grayscale 84x84, balanced RGB 90x96, and
  high-fidelity RGB 120x128 profiles.
- Retired the completed spec from the active root queue.

## Verification

- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.config.tests.test_config mario_rl.models.tests.test_models`
- `PATH=".venv/bin:$PATH" python -m unittest mario_rl.envs.tests.test_mario_env_factory`
- `PATH=".venv/bin:$PATH" python -m unittest discover mario_rl`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh train --config smb_ppo_rgb_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The CPU and MPS MacBook gates reported no warnings.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `2296e40` (`Add Mario pixel observation profiles`)
- umbrella repository: this commit (`Complete Mario pixel fidelity spec`)

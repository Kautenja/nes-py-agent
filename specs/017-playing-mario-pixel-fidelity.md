# Playing Mario Pixel Fidelity

## Status: TODO

## Problem

The learner should continue to play from pixels alone, but the current smoke
configs lean heavily on grayscale and aggressive downsampling. That is useful
for fast tests, yet RGB and less compressed observations may make important
game objects easier to learn.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- Preserve pixel-only model inputs. Do not add RAM, `info`, task metadata,
  object maps, or tile maps as policy observations in this spec.

## Requirements

- Add explicit pixel-observation profiles for:
  - the existing fast grayscale baseline;
  - a balanced RGB profile suitable for laptop smoke runs;
  - a higher-fidelity RGB profile for longer experiments.
- Use aspect-ratio-aware image sizes where practical instead of always forcing
  square frames.
- Resolve model `input_channels` and replay `state_shape` from RGB/grayscale
  plus frame-stack settings, or validate mismatches with clear errors.
- Keep downsampling, interpolation, channel order, and frame stacking fully
  visible in resolved configs and artifacts.
- Add trainability guidance documenting the memory and throughput tradeoff
  between grayscale 84x84, balanced RGB, and high-fidelity RGB profiles.
- Ensure vectorized PPO works with RGB observations and does not silently
  overrun memory in fast-dev tests.

## Acceptance Criteria

- A packaged RGB fast-dev config performs optimizer steps from RGB pixel
  observations only.
- Model input channels equal `3 * frame_stack` for RGB configs and
  `1 * frame_stack` for grayscale configs.
- Replay and rollout storage shapes match the resolved observation space.
- Tests fail clearly if config fields disagree about image size, channels, or
  frame stack.
- No policy/model code consumes RAM, `info`, task metadata, object maps, tile
  maps, or reward components as observations.
- Documentation explains when to choose each pixel profile.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.config.tests.test_config mario_rl.models.tests.test_models
python -m unittest mario_rl.envs.tests.test_mario_env_factory
python -m unittest discover mario_rl
./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false
./main.sh verify-macbook --device cpu
```

If Apple Silicon MPS is available, also run:

```shell
./main.sh verify-macbook --device mps
```

## Completion Signal Expectations

- Commit the child repository changes in
  `playing-mario-with-deep-reinforcement-learning`.
- Commit the umbrella submodule pointer.
- Add a history entry and completion log.

<!-- NR_OF_TRIES: 0 -->

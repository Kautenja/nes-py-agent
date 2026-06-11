# Playing Mario Curiosity Exploration

## Status: TODO

## Problem

Plain stochastic action sampling is weak exploration for Mario. The agent often
needs to discover sparse maneuvers such as timing jumps, entering pipes,
surviving enemy patterns, or reaching new screen regions before extrinsic
reward becomes informative.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- Implement a simple, clever exploration bonus that uses pixels only.
- Prefer the recurrent PPO path first. DQN support may be included if it stays
  small, but should not block a complete PPO implementation.

## Chosen Approach

Use Random Network Distillation (RND) for the first exploration upgrade. RND is
simple, works from pixel observations, does not require privileged game state,
and can be logged as an intrinsic reward channel. NoisyNet can remain a later
DQN-specific follow-up if needed.

## Requirements

- Add an exploration config with disabled-by-default RND settings:
  intrinsic reward scale, predictor learning rate, observation normalization,
  clipping, warmup behavior, and logging toggles.
- Build a frozen target network and trainable predictor network that consume
  pixel observations.
- Add intrinsic rewards to the training reward only when enabled.
- Keep extrinsic reward, transformed reward, intrinsic reward, and total
  training reward separately logged and persisted.
- Normalize or clip intrinsic rewards enough that curiosity cannot swamp
  ordinary progress and clear rewards by default.
- Keep all curiosity inputs pixel-only. Do not use RAM, `info`, task IDs,
  reward components, or progress labels for the intrinsic bonus.
- Make RND deterministic under fixed seeds.
- Provide a smoke config that enables RND for a very small PPO run.

## Acceptance Criteria

- With exploration disabled, training artifacts and behavior remain compatible
  with the previous PPO path.
- With RND enabled, the predictor receives gradients and the target network is
  frozen.
- Intrinsic reward metrics appear in CSV, JSON, and Lightning scalar logs.
- RND uses next pixel observations or current pixel observations consistently
  and documents the choice.
- Unit tests show intrinsic rewards are finite, deterministic under seed, and
  not derived from `info`.
- A bounded real Mario PPO smoke run completes with RND enabled.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.models.tests.test_models mario_rl.tests.test_train_cli
python -m unittest mario_rl.lightning.tests.test_module
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

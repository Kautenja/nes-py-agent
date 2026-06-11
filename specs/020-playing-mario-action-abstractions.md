# Playing Mario Action Abstractions

## Status: TODO

## Problem

Mario mechanics often require short temporal button patterns such as run,
short-hop, full jump, run-jump, brake, duck, and wait. Learning those frame
patterns from primitive controller actions alone is expensive, especially early
in training.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- Update `gym-super-mario-bros` or `nes-py` only if a reusable action-wrapper
  boundary clearly belongs there.
- Preserve pixel-only observations.

## Requirements

- Add a configurable macro-action wrapper for Mario RL training.
- Macro actions should be named, documented, deterministic sequences of
  existing Joypad action indices.
- Provide at least one conservative default set that includes primitive actions
  plus useful movement options:
  run right, short jump, full jump, run jump, hold left, crouch where
  available, and wait/no-op.
- Aggregate rewards and reward diagnostics across the macro sequence using the
  same rules as frame skip.
- Stop the macro immediately when the underlying environment terminates or
  truncates.
- Make interaction with `frame_skip` explicit in docs and config artifacts.
- Expose resolved macro metadata in train/play/random artifacts.
- Keep native NES 256-action mode available for experiments that do not want
  abstractions.

## Acceptance Criteria

- Existing action sets continue to work unchanged when macro actions are
  disabled.
- A packaged macro-action fast-dev config performs optimizer steps.
- Unit tests verify macro sequencing, early termination, reward aggregation,
  reward diagnostic aggregation, and action-space sizing.
- The model action head resolves to the macro action count when macros are
  enabled.
- Play/evaluation can load and run checkpoints trained with macro actions.
- Metrics and artifacts identify the active macro set.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.envs.tests.test_mario_env_factory
python -m unittest mario_rl.config.tests.test_config mario_rl.tests.test_train_cli
python -m unittest discover mario_rl
./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false
./main.sh verify-macbook --device cpu
```

If Apple Silicon MPS is available, also run:

```shell
./main.sh verify-macbook --device mps
```

## Completion Signal Expectations

- Commit child repository changes in each touched submodule.
- Commit the umbrella submodule pointer.
- Add a history entry and completion log.

<!-- NR_OF_TRIES: 0 -->

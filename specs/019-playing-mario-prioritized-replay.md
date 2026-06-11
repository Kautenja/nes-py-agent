# Playing Mario Prioritized Replay

## Status: TODO

## Problem

DQN currently samples uniformly from replay even though the config already has
prioritized replay fields. Mario produces many repetitive transitions, so the
off-policy learner should be able to focus more often on surprising or
high-error transitions while keeping importance sampling corrections.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- This spec targets the DQN and dueling-DQN path.
- Preserve pixel-only model inputs.

## Requirements

- Implement proportional prioritized replay for the existing replay buffer
  surface.
- Honor existing config fields for `prioritized`, `priority_alpha`, and
  `priority_beta`; add missing schedule/config fields only if needed.
- Store and sample transition priorities efficiently enough for the existing
  MacBook gate.
- Return sample indices and importance-sampling weights with prioritized
  batches.
- Apply importance weights to per-sample TD losses.
- Update priorities after each optimization step using absolute TD error plus a
  small epsilon.
- Preserve uniform replay as the default and keep its public contract stable.
- Persist enough replay metadata in artifacts or checkpoints to make resumed
  training understandable.

## Acceptance Criteria

- `replay.prioritized: false` preserves current uniform behavior.
- `replay.prioritized: true` trains without raising the existing
  `NotImplementedError`.
- Sampled high-priority transitions are selected more frequently in unit tests.
- TD loss uses importance-sampling weights for prioritized replay.
- Priority updates are deterministic under fixed seeds.
- Existing DQN smoke configs continue to pass.
- A new or updated DQN fast-dev config exercises prioritized replay.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.replay.tests.test_replay mario_rl.models.tests.test_losses
python -m unittest mario_rl.lightning.tests.test_module mario_rl.tests.test_train_cli
python -m unittest discover mario_rl
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
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

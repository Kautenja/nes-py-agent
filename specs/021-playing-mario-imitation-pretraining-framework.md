# Playing Mario Imitation Pretraining Framework

## Status: TODO

## Problem

The project should let the user add demonstration data later and use it to
warm-start the pixel policy. The repository should provide the dataset contract,
loader, validation, and behavior-cloning training path without bundling any
external gameplay data.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- Do not commit user demonstrations, ROMs, videos, or generated datasets.
- Preserve pixel-only training inputs.

## Requirements

- Define a documented imitation dataset format based on pixel observations and
  action labels.
- Support episode/segment files with at least:
  observations, actions, terminated/truncated flags or episode boundaries,
  environment ID, action-set metadata, observation-shape metadata, and optional
  human-readable source notes.
- Validate that dataset action sets, macro-action settings, image profiles, and
  frame-stack/channel layouts match the target config.
- Add an ignored default local data directory and documentation for where users
  can place demonstrations.
- Add a dataset loader with deterministic shuffling and train/validation split
  support.
- Add a behavior-cloning pretrain command that can initialize the active policy
  architecture and save a checkpoint compatible with subsequent RL training.
- Support recurrent actor-critic policy-head pretraining first. DQN imitation
  support may be added if it stays small.
- Add a tiny synthetic dataset fixture for tests only.
- Log cross-entropy loss, validation accuracy, dataset size, action histogram,
  and checkpoint path.

## Acceptance Criteria

- Running imitation tests requires no real user demonstration data.
- The pretrain command can train for a few steps on a synthetic pixel dataset
  and write a checkpoint.
- The normal train command can load the pretrain checkpoint and continue RL
  smoke training.
- Dataset validation catches mismatched action count, channel count, image size,
  and frame stack.
- Documentation tells the user exactly how to add local demonstration files
  without committing them.
- No policy input uses RAM, `info`, reward components, task metadata, object
  maps, or tile maps.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_entrypoints
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

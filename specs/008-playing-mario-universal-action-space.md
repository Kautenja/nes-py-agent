# Playing Mario Universal Action Space

## Status: TODO

Roadmap item: 5.

## Problem

The wrapper defaults to the full NES action space and documents `nes`, `right`,
`simple`, and `complex` action-space choices. `mario_rl` currently knows only
`right_only`, `simple`, and `complex`, and most active configs assume seven
actions. A single policy across Mario titles needs a stable action contract
that can either use the full NES action space or a deliberately chosen universal
subset without silently mis-sizing the model head.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if the
  wrapper action metadata is insufficient or inconsistent.
- Add explicit `nes` and `right` action-set support in `mario_rl`.
- Ensure the environment factory, model factory, configs, and checkpoints agree
  on action-space size.
- Add tests across representative SMB1, Lost Levels, SMB2 USA, and SMB3 envs.

## Repository And Release Rules

- Use local editable installs while developing and testing.
- If upstream action metadata or wrappers need changes, create a child branch
  such as `codex/playing-mario-universal-action-space` in the affected child
  repo before edits.
- Bump child versions only for child behavior changes and defer publishing to
  the final human-approved release pass.

## Acceptance Criteria

- `mario_rl.envs.ACTION_SETS` recognizes `nes`, `right`, `right_only`,
  `simple`, and `complex`.
- `action_set="nes"` leaves the native NES action space available with 256
  discrete actions, instead of wrapping it in `JoypadSpace`.
- `action_set="right"` and `action_set="right_only"` are accepted aliases for
  the same constrained movement list.
- `model.num_actions` can be inferred from a constructed env or resolved action
  set when configs request automatic sizing.
- Config validation fails fast when a fixed `model.num_actions` disagrees with
  the resolved action space.
- The default config choice is intentional and documented. If it remains
  `simple`, documentation explains that universal all-game training may prefer
  `nes` or `complex`.
- Training, play, and random-rollout commands report the resolved action set and
  action count in artifacts or logs.

## Unit Tests

- Unit-test action-set resolution for every supported name and alias.
- Unit-test native `nes` env creation with action space size 256.
- Unit-test constrained env creation with expected action counts.
- Unit-test model-head auto-sizing and mismatch errors.
- Unit-test representative environments:
  `SuperMarioBros-1-1-v0`, `SuperMarioBros2-1-1-v0`,
  `SuperMarioBros2USA-1-1-v0`, and one validated SMB3 single-stage env.
- Unit-test CLI/config overrides for `--env.action_set nes`.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_mario_env_factory
python -m unittest mario_rl.config.tests.test_config
python -m unittest mario_rl.models.tests.test_models
python -m unittest mario_rl.tests.test_train_cli
python -m unittest mario_rl.tests.test_play_cli
python -m unittest discover .
./main.sh random --config smb_dqn_fast_dev --env.action_set nes --env.max_smoke_steps 8
./main.sh unittest
```

After spec `005-playing-mario-macbook-trainability-guardrails` is complete,
also run:

```shell
./main.sh verify-macbook
```

If MPS is available on the current Mac, also run:

```shell
./main.sh verify-macbook --device mps
```

If wrapper changes are needed:

```shell
python -m unittest gym_super_mario_bros.tests.test_cli
python -m unittest gym_super_mario_bros.tests.test_registration
python -m unittest discover .
```

## Completion Signal Expectations

- Action-space sizing is deterministic and tested across the 9.1.0 task
  surface.
- Any needed child repo changes are locally committed before umbrella updates.
- Output `DONE` only after verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

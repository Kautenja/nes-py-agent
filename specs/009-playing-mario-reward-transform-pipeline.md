# Playing Mario Reward Transform Pipeline

## Status: TODO

Roadmap item: 6.

## Problem

`gym-super-mario-bros` 9.x already emits shaped rewards, clipped rewards, and
`info` fields such as `reward_components`, `reward_total_unclipped`, and
`reward_total_clipped`. `mario_rl` still applies an Atari-style sign clipping
wrapper by default. That can hide the richer cross-game reward signal and
double-transform rewards before training sees them.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  reward/info fields are missing or inconsistent on registered tasks.
- Replace the hard-coded sign-clipping assumption with configurable reward
  transforms.
- Preserve raw, wrapper-clipped, and training-transformed rewards in logs and
  replay.
- Keep old sign clipping available as an explicit option for baseline
  comparison.

## Repository And Release Rules

- Keep local editable installs active during implementation.
- Create a child branch before editing `nes-py` or `gym-super-mario-bros`.
- Bump child versions only when child package behavior changes.
- Do not publish releases. Note any required dependency lower-bound updates for
  the final release coordination pass.

## Acceptance Criteria

- `mario_rl` has a reward transform config with at least these modes:
  `env`, `sign`, `unclipped`, `clipped`, and `component_weights`.
- `env` uses the reward returned by the environment unchanged.
- `sign` reproduces the old sign-clipping behavior.
- `unclipped` reads `info["reward_total_unclipped"]` when present and fails or
  falls back according to an explicit config option.
- `clipped` reads `info["reward_total_clipped"]` when present.
- `component_weights` can combine named `reward_components` with configured
  weights and stable missing-component behavior.
- Replay stores the training reward and can optionally store raw/unclipped
  reward fields for metrics and debugging.
- Training artifacts include enough reward transform metadata to reproduce the
  run.
- Documentation explains why sign clipping is no longer the default for modern
  Mario training.

## Unit Tests

- Unit-test each reward transform mode with a fake env and fake `info`.
- Unit-test missing `reward_components` and missing total fields.
- Unit-test old sign-clipping equivalence.
- Unit-test replay batch reward fields and tensor conversion.
- Unit-test config parsing/overrides for reward transform modes.
- Unit-test Lightning training with a fake env that emits reward components.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_wrappers
python -m unittest mario_rl.replay.tests.test_replay
python -m unittest mario_rl.config.tests.test_config
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest discover .
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
./main.sh unittest
```

If wrapper reward fields change:

```shell
python -m unittest gym_super_mario_bros.tests.test_smv_env
python -m unittest gym_super_mario_bros.tests.test_smb2_env
python -m unittest gym_super_mario_bros.tests.test_smb3_env
python -m unittest discover .
```

## Completion Signal Expectations

- Reward transform behavior is explicit, tested, and documented.
- Any upstream reward fixes are versioned and locally committed.
- Output `DONE` only after verification, history, completion log, and required
  local commits are complete.

<!-- NR_OF_TRIES: 0 -->

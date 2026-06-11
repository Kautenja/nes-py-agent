# Playing Mario Auxiliary Losses

## Summary

Implemented optional auxiliary prediction losses for the recurrent PPO path in
`playing-mario-with-deep-reinforcement-learning`.

The new path includes:

- `AuxiliaryLossConfig` with default-off behavior, enabled target selection,
  per-target weights, and auxiliary-head sizing.
- Target extraction from normalized Mario `info` fields with explicit masks for
  missing values.
- Rollout storage for auxiliary target values and masks.
- Recurrent actor-critic auxiliary heads shared from the GRU state.
- Masked regression, binary, and game-family classification losses.
- PPO optimization that adds weighted auxiliary loss to the main PPO objective
  and reports PPO policy/value/entropy/KL/clip-fraction plus each auxiliary
  term separately.
- Durable train metrics JSON/CSV fields for PPO and auxiliary loss summaries.
- Packaged `smb_ppo_auxiliary_fast_dev` smoke config and README guidance.

Enabled smoke-config auxiliary targets:

- `progress_delta`
- `clear`
- `death`
- `transformed_reward`
- `game_family`

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

- `.venv/bin/python -m unittest mario_rl.models.tests.test_models`
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`
- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`
- `.venv/bin/python -m unittest discover .`
- `./main.sh train --config smb_ppo_auxiliary_fast_dev --trainer.enable_progress_bar false`
- `./main.sh unittest`
- `./main.sh verify-macbook`
- `./main.sh verify-macbook --device mps`

Notes:

- The host has no `python` shim, so direct Python module verification used
  `.venv/bin/python`; `main.sh` selects the same interpreter automatically.
- Focused verification passed: model tests 12, Lightning tests 14 with 1 skip,
  and config tests 7.
- Full unittest discovery and `./main.sh unittest` passed with 160 tests and
  7 skips.
- `smb_ppo_auxiliary_fast_dev` completed with `env_frames=32`,
  `global_step=4`, and `algorithm=ppo`.
- Auxiliary metrics were persisted in
  `runs/smb_ppo_auxiliary_fast_dev/train-metrics.json` and
  `train-metrics.csv`, including per-target losses and valid counts.
- MacBook gate CPU completed with train `2.31s`, eval `2.20s`, env FPS
  `13.87`, optimizer `3.03` steps/s, and no warnings.
- MacBook gate MPS completed with train `2.76s`, eval `2.16s`, env FPS
  `11.58`, optimizer `2.53` steps/s, and no warnings.
- Explicit MPS gate completed with train `2.92s`, eval `2.26s`, env FPS
  `10.97`, optimizer `2.40` steps/s, and no warnings.

## Commits

- Child `playing-mario-with-deep-reinforcement-learning`: `4d2b140`
  (`Add Mario PPO auxiliary losses`), pushed to
  `origin/codex/playing-mario-auxiliary-losses`.
- Umbrella: recorded in the companion root commit for this completion log.

## Release Notes

No child version bump was made because this is an unreleased development-path
training feature. The release-facing summary was added to `CHANGELOG.md`.

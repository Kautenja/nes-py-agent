# Playing Mario Evaluation Matrix

## Summary

Implemented matrix evaluation for
`playing-mario-with-deep-reinforcement-learning` with the new
`eval-matrix` command and packaged `smb_dqn_eval_matrix_fast_dev` config.

The new path includes:

- Task matrix construction from game-family, single-stage/full-game,
  train/eval split, validation-status, explicit include/exclude env ID, and
  `max_tasks` filters.
- Deterministic seed expansion and per-task episode counts.
- Optional full SMB3 catalog reporting as non-runnable metadata, while the
  validated 9.1.0 SMB3 stage entries remain runnable tasks.
- Checkpoint-backed DQN/PPO policy evaluation plus fake policy/fake env
  injection for ROM-free tests.
- Shared `MarioMetricsAccumulator` output with global, family, task, and
  episode summaries.
- `eval-matrix-summary.json` and `eval-matrix-episodes.csv`, where the table
  has one row per task, seed, and episode.
- Stable video prefixes such as
  `eval-matrix-supermariobros3-1-1-v0-seed-123-episode-0` without enabling
  rendering when video capture is disabled.

Example matrix output:

- Summary: `runs/smb_dqn_eval_matrix_fast_dev/eval-matrix-summary.json`
- Table: `runs/smb_dqn_eval_matrix_fast_dev/eval-matrix-episodes.csv`
- Selected runnable tasks: `SuperMarioBros-1-1-v0`,
  `SuperMarioBros3-1-1-v0`
- SMB3 catalog metadata entries: 56

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

- `.venv/bin/python -m unittest mario_rl.tests.test_evaluation_matrix`
- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`
- `.venv/bin/python -m unittest mario_rl.tests.test_entrypoints`
- `.venv/bin/python -m unittest mario_rl.envs.tests.test_mario_env_factory`
- `.venv/bin/python -m unittest mario_rl.tests.test_play_cli`
- `.venv/bin/python -m unittest discover .`
- `./main.sh config list`
- `./main.sh eval-matrix --help`
- `./main.sh train --config smb_dqn_eval_matrix_fast_dev --trainer.enable_progress_bar false`
- `./main.sh eval-matrix --config smb_dqn_eval_matrix_fast_dev`
- `./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32`
- `./main.sh unittest`
- `./main.sh verify-macbook`
- `./main.sh verify-macbook --device mps`

Notes:

- The host has no `python` shim, so direct Python module verification used
  `.venv/bin/python`; `main.sh` selects the same interpreter automatically.
- Full unittest discovery and `./main.sh unittest` passed with 149 tests and
  7 skips.
- `./main.sh eval-matrix --config smb_dqn_eval_matrix_fast_dev` wrote two
  task/seed/episode rows and 56 SMB3 metadata entries.
- MacBook gate CPU completed with train `2.56s`, eval `2.13s`, env FPS
  `12.49`, optimizer `2.73` steps/s, and no warnings.
- MacBook gate MPS completed with train `2.68s`, eval `2.04s`, env FPS
  `11.94`, optimizer `2.61` steps/s, and no warnings.
- Explicit MPS gate completed with train `2.60s`, eval `2.13s`, env FPS
  `12.31`, optimizer `2.69` steps/s, and no warnings.

## Commits

- Child `playing-mario-with-deep-reinforcement-learning`: `ee42398`
  (`Add Mario evaluation matrix runner`), pushed to
  `origin/codex/playing-mario-evaluation-matrix`.
- Umbrella: recorded in the companion root commit for this completion log.

## Release Notes

No child version bump was made because this is an unreleased development-path
evaluation feature. The release-facing summary was added to `CHANGELOG.md`.

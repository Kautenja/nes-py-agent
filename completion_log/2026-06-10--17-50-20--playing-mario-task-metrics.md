# Completion Log: Playing Mario Task Metrics

## Summary

Completed structured task metrics for
`playing-mario-with-deep-reinforcement-learning`.

The learner now has a typed metrics accumulator for Gymnasium reset/step info.
It records step-level normalized metrics, freezes episode records, and produces
global, per-game-family, and per-task summaries. Metrics include environment
episode return, transformed return, raw/unclipped/clipped return diagnostics,
clear/death/timeout/truncation counts and rates, progress summaries, task
identity fields, reward component sums, and explicit counters for missing
optional `info` keys.

Lightning training logs stable scalar names for key task metrics. Training keeps
the existing `train-metrics.csv` compatibility artifact and now writes
structured `train-metrics.json`. Evaluation/play uses the same accumulator and
writes the structured payload to `eval-metrics.json`.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`. The shell did not provide a bare `python`
executable, so direct unittest commands used `.venv/bin/python`.

- `.venv/bin/python -m unittest mario_rl.tests.test_metrics`:
  `3 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`:
  `11 tests`, `OK` (`skipped=1`).
- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_play_cli`:
  `2 tests`, `OK`.
- `.venv/bin/python -m unittest discover .`:
  `129 tests`, `OK` (`skipped=7`).
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`:
  reported `env_frames=128`, `global_step=25`, `action_set=simple`,
  `action_count=7`, `clear_rate=0.0`, and `death_rate=0.0`; wrote
  `runs/smb_dqn_fast_dev/train-metrics.csv` and
  `runs/smb_dqn_fast_dev/train-metrics.json`.
- `./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32`:
  wrote `runs/smb_dqn_fast_dev/eval-metrics.json` with `episode_count=1`,
  `total_steps=32`, global/per-family/per-task summaries, and a truncation
  count for the evaluation step limit.
- `./main.sh unittest`:
  `129 tests`, `OK` (`skipped=7`).
- `./main.sh verify-macbook`:
  passed CPU and MPS with no budget warnings and verified `metrics_json`.
  CPU summary: train `2.21s`, eval `2.03s`, env FPS `14.45`, optimizer
  `3.16` steps/s, actions `simple:7`. MPS summary: train `2.54s`,
  eval `2.02s`, env FPS `12.58`, optimizer `2.75` steps/s, actions
  `simple:7`.
- `./main.sh verify-macbook --device mps`:
  passed with no budget warnings; train `2.51s`, eval `2.03s`, env FPS
  `12.77`, optimizer `2.79` steps/s, actions `simple:7`.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `6cfacc0`
  (`Add structured Mario task metrics`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

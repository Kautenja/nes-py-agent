# Playing Mario Task Metrics

Completed structured task metrics for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added a typed `mario_rl.metrics` accumulator with step, episode, and aggregate
  records for Mario task metrics.
- Aggregates now report global, per-game-family, and per-task summaries with
  episode/transformed/raw/unclipped/clipped returns, clear/death/timeout/
  truncation counts and rates, progress summaries, reward component sums, and
  missing optional `info` key counters.
- Lightning training logs stable scalar metric names such as
  `train/clear_rate`, `train/death_rate`, `train/truncation_count`,
  `train/max_progress`, and `train/final_progress_mean`.
- Train still writes the compatibility `train-metrics.csv` and now also writes
  a structured `train-metrics.json`; play/evaluation writes the same structured
  summaries in `eval-metrics.json`.
- Evaluation applies the configured reward transform so eval metrics include
  both environment and transformed returns.
- The MacBook gate verifies the structured train metrics JSON when present.

Verification highlights:

- Focused metrics, Lightning, train CLI, and play CLI tests passed.
- Full unittest discovery and `./main.sh unittest` passed with 129 tests and
  7 skips.
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
  wrote `runs/smb_dqn_fast_dev/train-metrics.csv` and
  `runs/smb_dqn_fast_dev/train-metrics.json` with `env_frames=128` and
  `global_step=25`.
- `./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32`
  wrote `runs/smb_dqn_fast_dev/eval-metrics.json` with one SMB1 task summary,
  32 eval steps, and a truncation count for the evaluation step limit.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings. CPU
  summary: train `2.21s`, eval `2.03s`, env FPS `14.45`, optimizer `3.16`
  steps/s. MPS summary: train `2.54s`, eval `2.02s`, env FPS `12.58`,
  optimizer `2.75` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with no budget
  warnings; train `2.51s`, eval `2.03s`, env FPS `12.77`, optimizer `2.79`
  steps/s.

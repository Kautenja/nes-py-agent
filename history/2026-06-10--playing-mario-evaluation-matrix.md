# Playing Mario Evaluation Matrix

Completed evaluation matrix support for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `EvaluationMatrixConfig` with filters for game families,
  single-stage/full-game tasks, train/eval split, validation status, explicit
  include/exclude env IDs, `max_tasks`, deterministic seeds, per-task episode
  counts, and optional video naming.
- Added a reusable matrix builder that includes registered runnable tasks and
  can report the full 56-entry SMB3 catalog as non-runnable metadata while the
  validated 9.1.0 SMB3 stages remain runnable matrix tasks.
- Added `mario_rl.eval_matrix` and `./main.sh eval-matrix` for checkpoint
  evaluation across the selected matrix.
- Reused the shared task metrics accumulator so matrix outputs include global,
  per-game-family, per-task, and per-episode metrics.
- Wrote `eval-matrix-summary.json` plus `eval-matrix-episodes.csv` with one
  row per task, seed, and episode.
- Added fake-policy/fake-env coverage for ROM-free tests, invalid and empty
  matrix validation, seed expansion, video prefix generation, CLI parsing, and
  SMB3 validated task inclusion.
- Added the packaged `smb_dqn_eval_matrix_fast_dev` config and README
  documentation for recommended train/eval split reporting.

Verification highlights:

- Focused matrix, config, entrypoint, env factory, and play CLI tests passed.
- Full unittest discovery and `./main.sh unittest` passed with 149 tests and
  7 skips.
- `./main.sh train --config smb_dqn_eval_matrix_fast_dev
  --trainer.enable_progress_bar false` produced
  `runs/smb_dqn_eval_matrix_fast_dev/checkpoints/eval-matrix-fast-dev.ckpt`.
- `./main.sh eval-matrix --config smb_dqn_eval_matrix_fast_dev` produced
  `runs/smb_dqn_eval_matrix_fast_dev/eval-matrix-summary.json` and
  `runs/smb_dqn_eval_matrix_fast_dev/eval-matrix-episodes.csv` with two rows
  for `SuperMarioBros-1-1-v0` and `SuperMarioBros3-1-1-v0`, plus 56 SMB3
  catalog metadata entries.
- `./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps
  32` passed against the existing fast-dev checkpoint.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings. CPU
  summary: train `2.56s`, eval `2.13s`, env FPS `12.49`, optimizer `2.73`
  steps/s. MPS summary: train `2.68s`, eval `2.04s`, env FPS `11.94`,
  optimizer `2.61` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with no warnings;
  train `2.60s`, eval `2.13s`, env FPS `12.31`, optimizer `2.69` steps/s.

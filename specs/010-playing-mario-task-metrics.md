# Playing Mario Task Metrics

## Status: TODO

Roadmap item: 7.

## Problem

A universal Mario policy needs more than episode return. The 9.x environments
now expose cross-game `info` fields such as `clear`, `death`, `game_family`,
`task_id`, `progress`, `progress_max`, and reward components. `mario_rl` should
log these fields in a structured way so training and evaluation can answer
which games, stages, and mechanics are improving.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only when
  metrics reveal missing or inconsistent environment `info` fields.
- Add a metrics accumulator that consumes Gymnasium step/reset info.
- Support per-task, per-game-family, and global summaries.
- Write machine-readable artifacts for train and evaluation commands.

## Repository And Release Rules

- Use editable installs for local dependency changes.
- If `gym-super-mario-bros` or `nes-py` needs metric-related fixes, create a
  child branch such as `codex/playing-mario-task-metrics`.
- Bump child versions only for child behavior changes and defer release.

## Acceptance Criteria

- `mario_rl` has a typed metrics accumulator for step-level and episode-level
  Mario metrics.
- Metrics include at minimum: episode return, transformed return, raw/unclipped
  reward when available, clear count/rate, death count/rate, timeout/truncation
  count, max progress, final progress, task ID, game family, world, stage, and
  reward component sums.
- Aggregation supports global, per-game-family, and per-task summaries.
- Lightning logs key scalar metrics with stable names.
- Train command writes a structured metrics artifact, not only ad hoc CSV
  rows.
- Evaluation and play commands can reuse the same metrics accumulator.
- Missing optional `info` keys are handled explicitly and covered by tests.
- Documentation lists the emitted metric fields.

## Unit Tests

- Unit-test accumulator behavior with fake episodes across multiple tasks.
- Unit-test clear/death/truncation counting.
- Unit-test reward component accumulation.
- Unit-test missing-key behavior.
- Unit-test artifact serialization to JSON and CSV or Parquet if chosen.
- Unit-test Lightning metric logging using fake env factories.
- Unit-test CLI smoke outputs include the expected metric files.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest mario_rl.tests.test_train_cli
python -m unittest mario_rl.tests.test_play_cli
python -m unittest discover .
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32
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

If wrapper `info` fields change:

```shell
python -m unittest gym_super_mario_bros.tests.test_smv_env
python -m unittest gym_super_mario_bros.tests.test_smb2_env
python -m unittest gym_super_mario_bros.tests.test_smb3_env
python -m unittest gym_super_mario_bros.tests.test_tasks
python -m unittest discover .
```

## Completion Signal Expectations

- Metrics are structured, tested, and documented.
- Any required child submodule changes are committed locally before umbrella
  pointer updates.
- Completion log includes example metric artifact paths.
- Output `DONE` only after verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

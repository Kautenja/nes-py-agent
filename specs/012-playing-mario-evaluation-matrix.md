# Playing Mario Evaluation Matrix

## Status: TODO

Roadmap item: 9.

## Problem

A universal Mario agent needs evaluation that reports performance by game,
task, split, and stage rather than a single averaged return. `MarioTask`
metadata and SMB3 stage metadata now provide the necessary task inventory, but
`mario_rl` needs a reusable evaluation matrix runner and artifact format.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  evaluation reveals task metadata or environment reset defects.
- Add an evaluation matrix config and runner based on `MarioTask` filters.
- Reuse the metrics accumulator from spec 010.
- Support deterministic seeds, per-task episode counts, optional video capture,
  and machine-readable summary artifacts.

## Repository And Release Rules

- Use local editable installs for dependency changes.
- If a child repo needs fixes, create a branch such as
  `codex/playing-mario-evaluation-matrix` in that child repo before editing.
- Bump child versions only for child behavior changes.
- Do not publish or push. Defer dependency lower-bound changes to the final
  release pass unless the needed version is already released.

## Acceptance Criteria

- `mario_rl` can build an evaluation matrix from filters:
  game families, single-stage/full-game, train/eval split, validated status,
  explicit env ID include/exclude lists, and max tasks.
- The matrix includes 9.1.0 SMB3 validated stage entries and can optionally
  report the full SMB3 catalog as non-runnable/unregistered metadata.
- Evaluation runs each selected task with deterministic seeds and records
  per-episode and aggregate metrics.
- Outputs include a JSON summary and a tabular file with one row per
  task/seed/episode.
- CLI supports evaluating a checkpoint across the matrix.
- Evaluation can run against a fake policy/fake env in unit tests without ROMs.
- Optional video capture uses stable task/seed filenames and does not force
  rendering when disabled.
- Documentation describes recommended train/eval splits and all-game reporting.

## Unit Tests

- Unit-test matrix construction from filters and explicit lists.
- Unit-test deterministic seed expansion.
- Unit-test fake-env evaluation artifacts.
- Unit-test empty matrix and invalid task ID errors.
- Unit-test video path generation without opening real video writers.
- Unit-test CLI parsing for matrix evaluation.
- Unit-test SMB3 validated tasks are included when requested.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_mario_env_factory
python -m unittest mario_rl.tests.test_play_cli
python -m unittest discover .
./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32
./main.sh <new_eval_matrix_command> --config <new_eval_matrix_fast_dev_config>
./main.sh unittest
```

Replace placeholder command/config names with the actual CLI surface added by
this spec.

If wrapper task metadata changes:

```shell
python -m unittest gym_super_mario_bros.tests.test_tasks
python -m unittest gym_super_mario_bros.tests.test_registration
python -m unittest discover .
```

## Completion Signal Expectations

- Evaluation matrix artifacts are created and verified by unit tests.
- Any child repo fixes are locally committed before umbrella pointer updates.
- Completion log includes an example matrix output path and a short summary of
  selected tasks.
- Output `DONE` only after verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

# Playing Mario Task Suite Curriculum

## Status: TODO

Roadmap item: 4.

## Problem

`SuperMarioBrosRandomStages-*` was removed upstream, and `gym-super-mario-bros`
9.1.0 now exposes task metadata and SMB3 stage catalog data. `mario_rl` needs a
general task-suite sampler that can train a single policy across registered
Mario games without relying on one environment ID or the removed random-stage
environment family.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  task metadata or reset behavior defects block task-suite sampling.
- Build a task-suite configuration and sampler on top of `MarioTask`.
- Support deterministic seeded sampling for single-stage and full-game tasks.
- Support balanced sampling across game families and explicit include/exclude
  filters for worlds, stages, splits, and validation status.
- Integrate task-suite sampling into the current training loop before the
  recurrent actor-critic spec lands.

## Repository And Release Rules

- Maintain local editable installs during implementation.
- If `nes-py` or `gym-super-mario-bros` needs changes, create a new child
  branch such as `codex/playing-mario-task-suite-curriculum` before editing.
- Bump child package versions only when behavior in that child repo changes.
- Do not push or publish releases. Record any pending release-order dependency
  notes for the final human-approved release pass.

## Acceptance Criteria

- `mario_rl` has a typed `TaskSuiteConfig` or equivalent that can express:
  game families, single-stage/full-game selection, train/eval split,
  validated-only selection, alias inclusion, per-family weights, and a seed.
- `TaskSuite` or equivalent resolves candidates from `MarioTask` metadata
  without constructing environments.
- Sampling is deterministic for a fixed seed and changes predictably when the
  seed changes.
- Balanced family sampling can prevent SMB1/Lost Levels task counts from
  swamping smaller SMB2 USA and SMB3 task sets.
- The sampler includes SMB3 validated stages exposed by 9.1.0 and can
  optionally inspect the full SMB3 stage matrix for catalog/reporting without
  trying to train on unregistered reset entries.
- Current DQN training can reset into sampled tasks at episode boundaries or at
  a configured interval, while preserving the existing single-env config path.
- CLI/config docs replace old random-stage guidance with task-suite sampling.
- Smoke configs include a tiny deterministic multi-task suite that runs quickly
  in unit tests and CPU smoke checks.

## Unit Tests

- Unit-test candidate resolution for SMB1, Lost Levels, SMB2 USA, and SMB3.
- Unit-test deterministic seeded task ordering/sample choices.
- Unit-test weighted family sampling with small synthetic task sets.
- Unit-test invalid filters and empty candidate errors.
- Unit-test that removed `SuperMarioBrosRandomStages-*` IDs are not required.
- Unit-test training-loop task switches with fake env factories.
- Unit-test that the single-env legacy path still works.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_mario_env_factory
python -m unittest mario_rl.config.tests.test_config
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest mario_rl.tests.test_train_cli
python -m unittest discover .
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
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

If `gym-super-mario-bros` changes:

```shell
python -m unittest gym_super_mario_bros.tests.test_tasks
python -m unittest gym_super_mario_bros.tests.test_registration
python -m unittest discover .
```

## Completion Signal Expectations

- Task-suite sampling works in unit tests and a small smoke train.
- Any child repo changes are committed locally before umbrella pointer updates.
- Completion log records the sampled task surface and any deferred release
  notes.
- Output `DONE` only after tests, commits, and history updates are complete.

<!-- NR_OF_TRIES: 0 -->

# Playing Mario Adaptive Curriculum

## Status: TODO

## Problem

The current Mario task suite samples from fixed metadata filters. That is useful
for reproducibility, but it does not teach the agent progressively. Lost Levels
and later stages should not compete for training time before the learner has
basic movement, jumping, and early Super Mario Bros. progress.

## Scope

- Update `playing-mario-with-deep-reinforcement-learning`.
- Build on the existing task-suite, task metrics, and evaluation-matrix
  surfaces.
- Preserve pixel-only policy inputs.

## Requirements

- Add an adaptive curriculum mode alongside the existing fixed sampler.
- Represent curriculum state with explicit, serializable task progress records:
  sampled episodes, recent clear rate, recent death rate, recent max progress,
  best progress, and mastery status.
- Define configurable mastery and unlock thresholds with sensible defaults.
- Provide a default Mario progression that starts with early SMB1 mechanics and
  follows increasing world/stage order.
- Keep Lost Levels locked until SMB1 mastery criteria are met.
- Prefer earlier levels within each game family before later levels, while still
  allowing configurable includes/excludes for experiments.
- Sample from an active frontier rather than every registered task at once.
- Persist curriculum state and resolved curriculum metadata in training
  artifacts so interrupted runs can resume consistently.
- Make the sampler deterministic under fixed seeds.
- Keep evaluation-matrix task selection independent from adaptive training
  state unless explicitly configured.

## Acceptance Criteria

- Fixed task-suite behavior remains available and backward compatible.
- Adaptive curriculum smoke training starts from an easy SMB1 task and records
  curriculum metadata.
- Lost Levels tasks are not sampled until the configured SMB1 prerequisite is
  satisfied.
- Fake-env tests can drive task mastery and verify that later tasks unlock in
  order.
- The curriculum can resume from a checkpoint or saved state artifact without
  forgetting completed mastery.
- Metrics report active, mastered, locked, and retired task counts.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_task_suites mario_rl.tests.test_metrics
python -m unittest mario_rl.tests.test_train_cli
python -m unittest discover mario_rl
./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false
./main.sh verify-macbook --device cpu
```

If Apple Silicon MPS is available, also run:

```shell
./main.sh verify-macbook --device mps
```

## Completion Signal Expectations

- Commit the child repository changes in
  `playing-mario-with-deep-reinforcement-learning`.
- Commit the umbrella submodule pointer.
- Add a history entry and completion log.

<!-- NR_OF_TRIES: 0 -->

# Playing Mario Adaptive Curriculum

Completed spec `015-playing-mario-adaptive-curriculum.md`.

## Summary

- Added an opt-in adaptive curriculum mode alongside the existing fixed
  task-suite sampler.
- Added explicit serializable task progress records with sampled episodes,
  recent clear/death rates, recent max progress, best progress, mastery state,
  and active/locked/retired status.
- Implemented deterministic active-frontier sampling with early SMB1 defaults
  and Lost Levels locked until selected SMB1 prerequisite tasks are mastered.
- Persisted curriculum metadata/state in train metrics JSON, standalone
  `curriculum-state.json`, and Lightning checkpoints, with explicit saved-state
  artifact resume support.
- Updated PPO fast-dev training to exercise adaptive curriculum while keeping
  fixed sampler behavior and evaluation-matrix task selection independent.
- Retired the completed spec from the active root queue.

## Verification

- `python -m unittest mario_rl.envs.tests.test_task_suites mario_rl.tests.test_metrics`
- `python -m unittest mario_rl.tests.test_train_cli`
- `python -m unittest discover mario_rl`
- `./main.sh unittest`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The CPU and MPS MacBook gates reported no warnings.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `77c47d5` (`Add adaptive Mario curriculum`)
- umbrella repository: this commit (`Complete Mario adaptive curriculum spec`)

# Playing Mario Adaptive Curriculum

Completed adaptive curriculum training for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `task_suite.mode` with backward-compatible `fixed` sampling and an
  opt-in `adaptive` curriculum sampler.
- Added serializable per-task progress records with sampled episodes, recent
  clear/death rates, recent and best progress, mastery status, and active/
  locked/retired status.
- Implemented deterministic active-frontier sampling with default progression
  from early SMB1 stages through later families, keeping Lost Levels locked
  until selected SMB1 prerequisite tasks are mastered.
- Persisted curriculum metadata and state in train metrics JSON, a standalone
  `curriculum-state.json`, and Lightning checkpoints; adaptive configs can also
  resume from an explicit saved state artifact path.
- Updated the PPO fast-dev config to exercise adaptive curriculum while leaving
  fixed task-suite configs and evaluation-matrix task selection independent.

Verification highlights:

- `python -m unittest mario_rl.envs.tests.test_task_suites mario_rl.tests.test_metrics`
  passed.
- `python -m unittest mario_rl.tests.test_train_cli` passed.
- `python -m unittest discover mario_rl` passed with 168 tests and 2 skips.
- `./main.sh unittest` passed with 168 tests and 2 skips.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
  passed and wrote `runs/smb_ppo_fast_dev/curriculum-state.json` with
  `SuperMarioBros-1-1-v0` as the initial active task and Lost Levels locked.
- `./main.sh verify-macbook --device cpu` passed with train `2.52s`, eval
  `2.11s`, env FPS `50.77`, and optimizer `3.17` steps/s.
- `./main.sh verify-macbook --device mps` passed with train `3.19s`, eval
  `2.13s`, env FPS `40.10`, and optimizer `2.51` steps/s.

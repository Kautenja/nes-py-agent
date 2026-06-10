# Playing Mario Task Conditioning

Completed task conditioning for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `mario_rl.tasks` plus `mario_rl.envs` re-exports for the
  `gym-super-mario-bros` 9.1 task metadata surface, including `MarioTask`,
  `available_tasks`, `task_for_env_id`, and `smb3_stage_matrix`.
- Added `TaskFeatureEncoder`, which builds deterministic one-hot vocabularies
  for `game_family`, canonical `task_id`, and `rom_mode`, plus numeric
  `world`/`stage` features and binary `single_stage`/`validated` flags.
- Alias IDs such as `SuperMarioBros1-1-v0` encode to the canonical task ID,
  while unknown/custom IDs use an explicit `<unknown>` bucket without creating
  ROM-backed environments.
- `DQN` and `DuelingDQN` now accept optional task feature tensors while keeping
  the default pixel-only forward path and unconditioned checkpoint layout.
- Uniform replay batches can carry current and next-state task feature vectors,
  and the Lightning train/eval paths pass the configured task features when
  task conditioning is enabled.
- Added `smb_dqn_task_conditioned_fast_dev` as the explicit opt-in config and
  tightened the learner dependency to `gym-super-mario-bros>=9.1.0`.

Verification highlights:

- Full `mario_rl` unittest discovery passed with 98 tests and 7 skips.
- `./main.sh unittest` passed with 98 tests and 7 skips.
- The task-conditioned real-environment train/play smoke passed with a
  four-step train override and one four-step evaluation episode.
- `./main.sh verify-macbook` passed on CPU and MPS with no budget warnings.
  CPU summary: train `2.15s`, eval `2.03s`, env FPS `14.86`, optimizer
  `3.25` steps/s. MPS summary: train `2.53s`, eval `2.02s`, env FPS `12.67`,
  optimizer `2.77` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with train `2.66s`,
  eval `2.19s`, env FPS `12.01`, and optimizer `2.63` steps/s.

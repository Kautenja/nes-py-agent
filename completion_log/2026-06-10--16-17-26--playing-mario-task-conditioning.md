# Completion Log: Playing Mario Task Conditioning

## Summary

Completed task conditioning for
`playing-mario-with-deep-reinforcement-learning`.

The Mario learner now exposes a public task metadata API through
`mario_rl.tasks` and `mario_rl.envs`, wrapping the `gym-super-mario-bros` 9.1
`MarioTask` catalog and SMB3 stage matrix. `TaskFeatureEncoder` deterministically
encodes `game_family`, canonical `task_id`, `world`, `stage`, `rom_mode`,
`single_stage`, and `validated` into model-ready `float32` vectors without
constructing ROM-backed environments.

Task conditioning is opt-in. The default pixel-only DQN path remains unchanged,
while conditioned `DQN` and `DuelingDQN` modules concatenate task features after
the CNN trunk. Replay batches can carry current and next-state task features,
and Lightning training/evaluation pass the configured environment's task vector
when conditioning is enabled. Unknown/custom IDs use an explicit `<unknown>`
bucket, and alias IDs encode to the canonical task ID.

Added `smb_dqn_task_conditioned_fast_dev` as the explicit opt-in smoke config
and updated the learner dependency floor to `gym-super-mario-bros>=9.1.0`.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`.

- `.venv/bin/python -m pip install -e ../nes-py -e ../gym-super-mario-bros -e .`:
  succeeded and installed local editable `gym_super_mario_bros-9.1.0`,
  `nes_py-9.0.1`, and `playing-mario-with-deep-reinforcement-learning`.
- `.venv/bin/python -m unittest mario_rl.envs.tests.test_mario_env_factory`:
  `8 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.envs.tests.test_task_features`:
  `4 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.models.tests.test_models`:
  `7 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.replay.tests.test_replay`:
  `5 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`:
  `8 tests`, `OK` (`skipped=1`).
- `.venv/bin/python -m unittest discover .`:
  `98 tests`, `OK` (`skipped=7`).
- `./main.sh unittest`:
  `98 tests`, `OK` (`skipped=7`).
- `./main.sh train --config smb_dqn_task_conditioned_fast_dev --trainer.enable_progress_bar false --train.max_steps 4 --train.log_interval 1 --replay.warmup 2 --replay.batch_size 2`:
  wrote `runs/smb_dqn_task_conditioned_fast_dev/checkpoints/task-conditioned-fast-dev.ckpt`,
  `runs/smb_dqn_task_conditioned_fast_dev/train-metrics.csv`, and
  `runs/smb_dqn_task_conditioned_fast_dev/resolved-config.yaml`; reported
  `env_frames=16` and `global_step=3`.
- `./main.sh play --config smb_dqn_task_conditioned_fast_dev --eval.episodes 1 --eval.max_steps 4 --trainer.enable_progress_bar false`:
  loaded the task-conditioned checkpoint and wrote
  `runs/smb_dqn_task_conditioned_fast_dev/eval-metrics.json` with `1` episode,
  `4` total steps, and `0.0` total reward.
- `./main.sh verify-macbook`:
  passed CPU and MPS with no budget warnings. CPU summary: train `2.15s`, eval
  `2.03s`, env FPS `14.86`, optimizer `3.25` steps/s, summary
  `runs/smb_dqn_macbook_gate_cpu/macbook-gate-summary.json`. MPS summary:
  train `2.53s`, eval `2.02s`, env FPS `12.67`, optimizer `2.77` steps/s,
  summary `runs/smb_dqn_macbook_gate_mps/macbook-gate-summary.json`.
- `./main.sh verify-macbook --device mps`:
  passed with no budget warnings; train `2.66s`, eval `2.19s`, env FPS
  `12.01`, optimizer `2.63` steps/s.
- After small formatting cleanup, reran:
  `.venv/bin/python -m unittest mario_rl.envs.tests.test_task_features`,
  `.venv/bin/python -m unittest mario_rl.models.tests.test_models`,
  `.venv/bin/python -m unittest mario_rl.replay.tests.test_replay`, and
  `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`; all
  passed with the same focused counts.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `40dda3f`
  (`Add Mario task conditioning`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

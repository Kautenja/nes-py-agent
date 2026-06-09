# Completion Log: Playing Mario Lightning Training And Device Smoke

## Summary

Completed the Playing Mario Lightning training and device smoke spec by adding
the active `mario_rl.lightning` package, replacing train/play placeholders with
real Lightning training and checkpoint evaluation, documenting CPU/MPS/CUDA
commands, and ignoring generated `runs/` artifacts.

The Lightning module uses manual optimization for online DQN, collects
Gymnasium transitions into the existing uniform replay buffer, trains from
replay after configurable warmup, updates a target network on the configured
cadence, supports Double-DQN targets, logs finite training metrics, and saves
config/hparams plus explicit environment frame, episode, loss, update, and
epsilon schedule state in checkpoints.

## Red Checks

- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.lightning.tests`
  initially failed while tightening the training budget because
  `Trainer(max_steps=...)` counted optimizer steps rather than rollout steps,
  allowing warmup transitions to exceed the intended smoke step budget.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_train_cli mario_rl.tests.test_play_cli mario_rl.tests.test_entrypoints`
  initially failed on the same budget mismatch. The fix made training
  dataset-bounded with `max_epochs=1` and `limit_train_batches=train.max_steps`.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`.

- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.lightning.tests`:
  `7 tests`, `OK` (`skipped=1`, CUDA gated).
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_train_cli`:
  `1 test`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest mario_rl.tests.test_play_cli`:
  `1 test`, `OK`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m unittest discover .`:
  `86 tests`, `OK` (`skipped=4`).
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh unittest`:
  `86 tests`, `OK` (`skipped=4`).
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh train --config smb_dqn_fast_dev --train.accelerator cpu`:
  completed and wrote `runs/smb_dqn_fast_dev/checkpoints/fast-dev.ckpt`,
  `env_frames=128`, `global_step=25`.
- `PATH="$PWD/.venv/bin:$PATH" python3 -m mario_rl.play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32`:
  loaded the smoke checkpoint and wrote `runs/smb_dqn_fast_dev/eval-metrics.json`
  for `1` episode and `32` capped steps.
- `PATH="$PWD/.venv/bin:$PATH" python3 - <<'PY' ...` hardware probe:
  printed `mps True` and `cuda False`.
- `PATH="$PWD/.venv/bin:$PATH" ./main.sh train --config smb_dqn_fast_dev --train.accelerator mps --train.devices 1`:
  completed with Lightning using MPS, `env_frames=128`, `global_step=25`.
- Re-ran the play command after the MPS smoke; the checkpoint loaded on CPU and
  completed `1` capped episode with `32` steps.

The Gymnasium deprecation warnings for `SuperMarioBros*-v0` remain expected for
the current wrapper IDs. The bare Homebrew `python3` interpreter did not have
Torch/Lightning installed, so all verification used the checked-out submodule
virtualenv.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `c2d69a1`
  (`Add Lightning DQN training smoke path`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

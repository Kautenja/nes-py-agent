# Completion Log: Playing Mario MacBook Trainability Guardrails

## Summary

Completed the MacBook trainability guardrails for
`playing-mario-with-deep-reinforcement-learning`.

The Mario learner now has a documented `./main.sh verify-macbook` gate that
runs the fast unit subset, performs a bounded real Super Mario Bros. mini
training run, evaluates the checkpoint it produced, verifies all required
artifacts, and writes a per-device `macbook-gate-summary.json`.

The gate records device, selected environment ID, Python/PyTorch versions, wall
time, environment frames per second, optimizer steps per second, eval steps,
peak memory when available, artifact paths, and warning-based budget results.
It verifies CPU by default and runs MPS automatically when PyTorch reports MPS
availability. A `--benchmark-only` mode measures a bounded random rollout plus
the same mini optimization pass for later before/after comparisons.

`main.sh` now prefers `.venv/bin/python` when the local virtualenv exists while
still allowing a `PYTHON=/path/to/python` override. This keeps the documented
commands aligned with the editable-install workflow used by this checkout.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with the existing
Python 3.14 virtualenv at `.venv`.

- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`:
  `5 tests`, `OK`.
- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli`:
  `1 test`, `OK`.
- `.venv/bin/python -m unittest mario_rl.tests.test_play_cli`:
  `1 test`, `OK`.
- `.venv/bin/python -m unittest mario_rl.tests.test_verify_macbook`:
  `10 tests`, `OK`.
- `.venv/bin/python -m unittest discover .`:
  `86 tests`, `OK` (`skipped=7`).
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`:
  wrote `runs/smb_dqn_fast_dev/checkpoints/fast-dev.ckpt`,
  `runs/smb_dqn_fast_dev/train-metrics.csv`, and
  `runs/smb_dqn_fast_dev/resolved-config.yaml`; reported `env_frames=128` and
  `global_step=25`.
- `./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32`:
  loaded the fast-dev checkpoint and wrote
  `runs/smb_dqn_fast_dev/eval-metrics.json` with `1` episode, `32` total steps,
  and `31.0` total reward.
- `./main.sh verify-macbook`:
  passed CPU and MPS with no budget warnings. CPU summary:
  train `2.15s`, eval `1.98s`, env FPS `14.90`, optimizer `3.26` steps/s,
  summary `runs/smb_dqn_macbook_gate_cpu/macbook-gate-summary.json`.
  MPS summary: train `4.01s`, eval `2.04s`, env FPS `7.98`, optimizer `1.74`
  steps/s, summary `runs/smb_dqn_macbook_gate_mps/macbook-gate-summary.json`.
- `./main.sh verify-macbook --device mps`:
  passed with no budget warnings; train `2.42s`, eval `1.98s`, env FPS
  `13.25`, optimizer `2.90` steps/s.
- `./main.sh verify-macbook --benchmark-only --device cpu`:
  passed with no budget warnings; random rollout `38.42` steps/s, train
  `2.14s`, env FPS `14.94`, optimizer `3.27` steps/s, summary
  `runs/smb_dqn_macbook_gate_benchmark_cpu/macbook-gate-summary.json`.

The bare Homebrew `python3` interpreter was missing `gymnasium`, so all
verification used the checked-out submodule virtualenv. The hardcoded
`python3` route in `main.sh` was replaced with local-venv discovery as part of
the fix.

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `ce2558a`
  (`Add MacBook trainability gate`), pushed to `origin/pytorch`.
- Umbrella: records this completion log, history/changelog updates, live-queue
  retirement, and the updated submodule pointer in the root commit for this
  completed spec.

# Playing Mario MacBook Trainability Guardrails

Completed the local trainability gate for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `mario_rl.verify_macbook`, exposed through `./main.sh verify-macbook`,
  to run the fast unit subset, a bounded real Super Mario Bros. training job,
  and checkpoint evaluation against the produced artifact.
- Added `smb_dqn_macbook_gate`, a tiny real-environment config with 40x40
  frame stacks, deterministic seeds, eight training steps, one eight-step eval
  episode, and no rendering or video output by default.
- The gate verifies checkpoint, resolved config, train metrics, TensorBoard
  event output, and eval metrics before writing `macbook-gate-summary.json`.
- Gate summaries record device, Python/PyTorch versions, selected env ID, wall
  time, environment FPS, optimizer steps per second, eval steps, peak memory
  when available, and warning-based performance budget results.
- `--device auto` always runs CPU and runs MPS only when PyTorch reports it as
  available; unavailable MPS produces an explicit skip. `--device mps` provides
  a targeted MPS pass.
- `--benchmark-only` provides a repeatable env-step plus mini-optimization
  profiling mode for later specs.
- `main.sh` now prefers the checked-out `.venv/bin/python` when present while
  preserving a `PYTHON=/path/to/python` override, matching the local editable
  install workflow used by this project.

Verification highlights:

- Full `mario_rl` unittest discovery passed with 86 tests and 7 skips.
- `./main.sh verify-macbook` passed on CPU and MPS with no budget warnings.
  CPU summary: train `2.15s`, eval `1.98s`, env FPS `14.90`, optimizer
  `3.26` steps/s. MPS summary: train `4.01s`, eval `2.04s`, env FPS `7.98`,
  optimizer `1.74` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with train `2.42s`,
  eval `1.98s`, env FPS `13.25`, and optimizer `2.90` steps/s.
- `./main.sh verify-macbook --benchmark-only --device cpu` passed with random
  rollout `38.42` steps/s and mini optimization `3.27` steps/s.

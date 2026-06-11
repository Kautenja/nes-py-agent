# Playing Mario Emulator Snapshot Curriculum

Completed spec `016-playing-mario-emulator-snapshot-curriculum.md`.

## Summary

- Added a documented process-local snapshot curriculum contract for Mario RL
  using opaque `nes-py` snapshots and metadata-only persistence.
- Added `mario_rl.snapshots` with compatibility validation, ranked/tagged
  snapshot capture, sampling, restore, and normal reset fallback.
- Captured and restored wrapper state for frame stacks, frame-skip buffers,
  training timeouts, and reward wrapper counters.
- Wired DQN and vectorized recurrent PPO training to capture non-terminal
  snapshots and sample compatible snapshot reset starts.
- Added snapshot-start episode metrics, full-reset clear counts, and
  `snapshot-metadata.json` artifacts that exclude ROM bytes, native state, and
  copied observations.
- Added fake-env tests, real Mario frame-skip/frame-stack restore smoke
  coverage, and vectorized PPO snapshot-slot coverage.
- Retired the completed spec from the active root queue.

## Verification

- `python -m unittest nes_py.tests.test_nes_env nes_py.tests.test_ram_reads`
- `python -m unittest discover nes_py`
- `python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.tests.test_train_cli`
- `python -m unittest discover mario_rl`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh verify-macbook --device cpu`
- `./main.sh verify-macbook --device mps`

All verification passed. The CPU and MPS MacBook gates reported no warnings.

## Local Commits

- `playing-mario-with-deep-reinforcement-learning`: `8294d0f` (`Add Mario snapshot curriculum`)
- umbrella repository: this commit (`Complete Mario snapshot curriculum spec`)

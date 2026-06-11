# Playing Mario Emulator Snapshot Curriculum

## Status: TODO

## Problem

Long Mario levels waste training time when the agent must repeatedly replay
easy sections before reaching a hard jump, enemy pattern, or end-of-level
sequence. Speed runners solve this with save states. The learner should be able
to build and reuse an internal library of high-value emulator snapshots without
feeding privileged game state into the policy.

## Scope

- Update `nes-py` if public snapshot support is insufficient.
- Update `gym-super-mario-bros` only if wrapper-level reset/restore hooks need
  to expose existing emulator snapshot APIs safely.
- Update `playing-mario-with-deep-reinforcement-learning` with snapshot
  library, sampling, and training integration.
- Do not add ROMs, copyrighted game assets, or bundled external save-state
  data.

## Existing Context

`nes-py` already exposes opaque native state snapshots through
`NESEnv.dump_state()`, `NESEnv.load_state(...)`, and vector-emulator state
helpers. This spec should first assess and reuse that surface. Add lower-level
`nes-py` changes only when needed for deterministic, public, tested Mario RL
use.

## Requirements

- Provide a documented public snapshot contract: what can be captured, what can
  be restored, compatibility requirements, and what is intentionally opaque.
- Associate each snapshot with metadata such as env ID, ROM fingerprint or
  equivalent compatibility key, action set, seed lineage, progress, episode
  step, task ID, and human-readable tags.
- Support process-local opaque snapshots for fast training loops.
- If durable snapshot serialization is implemented, it must exclude ROM data,
  validate compatibility on load, and fail clearly across incompatible emulator
  versions, mappers, ROM hashes, or wrappers.
- Add a Mario RL snapshot library that can:
  - capture candidate snapshots during training or scripted roll-ins;
  - rank or tag snapshots by progress, death proximity, repeated failure,
    clear proximity, or manual labels;
  - sample snapshots as reset starts according to config;
  - fall back to normal environment resets when no valid snapshot exists.
- Track snapshot-start episodes separately in metrics so curriculum progress is
  not confused with full-level clears.
- Ensure restored episodes still produce only pixel observations for the policy.
- Ensure reset/restore behavior interacts correctly with frame stacks,
  frame-skip reward aggregation, recurrent hidden-state reset, and vectorized
  rollout slots.

## Acceptance Criteria

- Focused `nes-py` tests prove snapshot round trips restore screen, RAM, and
  continuation behavior for at least one representative local test ROM or
  existing fixture.
- Mario RL fake-env tests cover snapshot capture, library sampling, and reset
  fallback behavior.
- A real Mario smoke run can capture at least one process-local snapshot and
  later start an episode from it in the same process.
- Snapshot metadata artifacts are written without including ROM bytes.
- Invalid snapshot/env compatibility produces a clear error or skip, not a
  crash or silent wrong restore.
- Pixel observations remain the only model input.

## Verification

Run relevant commands from each touched child repo.

From `nes-py`:

```shell
python -m unittest nes_py.tests.test_nes_env nes_py.tests.test_ram_reads
python -m unittest discover nes_py
```

From `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.envs.tests.test_wrappers mario_rl.tests.test_train_cli
python -m unittest discover mario_rl
./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false
./main.sh verify-macbook --device cpu
```

If Apple Silicon MPS is available, also run:

```shell
./main.sh verify-macbook --device mps
```

## Completion Signal Expectations

- Commit child repository changes in each touched submodule.
- Commit the umbrella submodule pointer.
- Add a history entry and completion log.

<!-- NR_OF_TRIES: 0 -->

# Playing Mario Task Conditioning

## Status: TODO

Roadmap item: 3.

## Problem

`gym-super-mario-bros` 9.1.0 exposes `MarioTask` metadata for full games,
single-stage tasks, SMB3 validated stages, and task identifiers. `mario_rl`
still treats task identity mostly as an environment ID string and its active
DQN models consume only pixels. A single network that can play across SMB1,
Lost Levels, SMB2 USA, and SMB3 needs stable task conditioning that does not
depend on ad hoc environment-name parsing.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  tests reveal missing or inconsistent metadata needed by this spec.
- Add a typed task-conditioning layer in `mario_rl` that converts `MarioTask`
  fields into stable categorical/numeric features.
- Wire task conditioning into the active model factory without breaking
  existing unconditioned DQN checkpoints or smoke tests.
- Thread task metadata through environment creation, replay samples, and
  training/evaluation boundaries so future PPO and evaluation specs can reuse
  the same contract.

## Repository And Release Rules

- Keep local editable installs during implementation:
  `python -m pip install -e ../nes-py -e ../gym-super-mario-bros -e .`
  from `playing-mario-with-deep-reinforcement-learning`.
- If `nes-py` or `gym-super-mario-bros` must change, create a new child branch
  such as `codex/playing-mario-task-conditioning` before editing that child
  repo.
- If a child package behavior changes, bump its version and changelog in that
  child repo, but do not publish or push. Record pending release ordering in
  the completion log: `nes-py`, then `gym-super-mario-bros`, then `mario_rl`
  dependency files after the human-approved releases.
- Commit child submodule changes locally before committing the umbrella
  submodule pointer.

## Acceptance Criteria

- `mario_rl` exposes a task metadata API that wraps or re-exports
  `gym_super_mario_bros.MarioTask` and supports all registered 9.1.0 families,
  including SMB3 validated stage entries from `smb3_stage_matrix`.
- A deterministic `TaskFeatureEncoder` or equivalent maps `game_family`,
  `task_id`, `world`, `stage`, `rom_mode`, `single_stage`, and `validated`
  into tensors suitable for model inputs.
- The encoder has explicit unknown-value behavior for user-provided/custom
  environments and does not require constructing ROM-backed environments.
- DQN and Dueling DQN support optional task-conditioning inputs while preserving
  the old pixel-only forward path.
- Replay batches can carry task IDs or encoded task features when conditioning
  is enabled.
- Training and play/evaluation code pass the active task metadata to the model
  when the selected environment ID is registered in `gym-super-mario-bros`.
- The config surface includes a feature flag for task conditioning and defaults
  preserve existing smoke behavior unless a new task-conditioned config is
  explicitly selected.
- Documentation explains how task conditioning is represented and how it uses
  `MarioTask`.

## Unit Tests

- Add task encoder tests for all game families: `smb1`, `lost_levels`,
  `smb2_usa`, and `smb3`.
- Add tests proving alias IDs, for example `SuperMarioBros1-1-v0`, encode to
  the canonical task ID.
- Add tests for unknown/custom environment IDs.
- Add model tests for pixel-only forward compatibility and task-conditioned
  forward shape compatibility.
- Add replay tests proving task fields survive push/sample/to-torch boundaries.
- Add Lightning/module tests using fake task metadata so no ROM-backed env is
  needed for fast unit coverage.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning` after refreshing
local editable installs:

```shell
python -m unittest mario_rl.envs.tests.test_mario_env_factory
python -m unittest mario_rl.models.tests.test_models
python -m unittest mario_rl.replay.tests.test_replay
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest discover .
./main.sh unittest
```

If `gym-super-mario-bros` changes, also run from that child repo:

```shell
python -m unittest gym_super_mario_bros.tests.test_tasks
python -m unittest gym_super_mario_bros.tests.test_registration
python -m unittest discover .
```

If `nes-py` changes, run the focused Python and native checks appropriate to
the touched emulator area and include the commands in the completion log.

## Completion Signal Expectations

- All acceptance criteria are implemented and verified.
- Required child submodule commits are created locally first.
- The umbrella repo records updated submodule pointers and spec/history files.
- Output `DONE` only after verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

# Specification: Playing Mario Lightning Training And Device Smoke

## Feature: Device-Portable Lightning DQN Training

### Overview
Build the modern training and play path around PyTorch Lightning so a user can
run a small Mario DQN training job on a MacBook using CPU or MPS, or on a Linux
server using CUDA. This spec completes the path started by the dependency,
environment, config, and model-core specs.

### User Stories
- As a MacBook user, I want `fast_dev_run` and short smoke configs to train on
  CPU or MPS without editing code.
- As a Linux server user, I want the same config surface to select CUDA and
  write checkpoints/logs under an experiment directory.
- As a researcher, I want play/evaluation commands that load Lightning
  checkpoints and produce metrics, optional videos, and reproducible results.

---

## Problem Or Goal
The legacy `DeepQAgent` owns environment rollout, replay, Keras prediction,
target updates, checkpointing, and plotting inside one class. The modern
project needs a Lightning-oriented separation: config-driven env construction,
PyTorch model modules, replay-driven training steps, explicit device handling,
checkpointable state, and smoke tests that run quickly.

---

## Scope

### In Scope
- Implement a `mario_rl.lightning` package with a DQN LightningModule and any
  DataModule or rollout dataset needed for online replay training.
- Use the PyTorch model/replay/config/env components from specs 002-004.
- Support CPU, MPS, and CUDA accelerator selection through config and CLI
  overrides.
- Write checkpoints, metrics, logs, copied config, and optional videos under a
  stable experiment directory.
- Implement play/evaluation from a Lightning checkpoint.
- Add fast tests with fake envs and gated smoke tests with real Mario.
- Update README with concise train/play examples.

### Out Of Scope
- Proving game-solving convergence.
- Distributed multi-node training.
- TensorFlow/Keras checkpoint migration.
- Atari or Tetris training.
- Docker image creation unless added by a later spec.

---

## Functional Requirements

### FR-1: Lightning Training Module
Training MUST run through Lightning and native PyTorch.

**Acceptance Criteria:**
- [ ] The module subclasses `lightning.pytorch.LightningModule`.
- [ ] The module uses manual optimization or a clearly tested Lightning-safe
  training pattern appropriate for online DQN.
- [ ] The module owns online Q-network, target Q-network, optimizer, epsilon
  schedule, target update cadence, and Double-DQN behavior from config.
- [ ] Training logs finite loss, episode reward, epsilon, environment frames,
  and learning rate where available.
- [ ] Checkpoints include model weights, optimizer state, config/hparams, and
  enough counters/schedule state to resume a smoke run predictably.
- [ ] No active training module imports Keras or TensorFlow.

### FR-2: Rollout And Replay Integration
The training path MUST collect and train from replay data safely.

**Acceptance Criteria:**
- [ ] Replay warmup is configurable and can be set very small for tests.
- [ ] Env interaction handles Gymnasium `terminated` and `truncated` flags.
- [ ] Env CPU observations are moved to the Lightning module device only at
  tensor boundaries.
- [ ] A fake deterministic Gymnasium env can drive a complete fast-dev-run
  without the Mario emulator.
- [ ] A real Mario smoke config can run a capped rollout without requiring
  convergence.

### FR-3: Device Selection
The CLI MUST support local CPU/MPS and server CUDA.

**Acceptance Criteria:**
- [ ] Config supports `train.accelerator` values suitable for `cpu`, `mps`,
  `cuda`/`gpu`, and `auto`.
- [ ] CPU smoke tests run unconditionally.
- [ ] MPS smoke tests are gated on `torch.backends.mps.is_available()` and
  skip cleanly when unavailable.
- [ ] CUDA smoke tests are gated on `torch.cuda.is_available()` or an explicit
  environment variable such as `MARIO_RL_RUN_CUDA_SMOKE=1`.
- [ ] Device-selection tests verify that tensors and models are placed on the
  requested device when the device exists.

### FR-4: Evaluation And Artifacts
The project MUST support play/evaluation from a checkpoint.

**Acceptance Criteria:**
- [ ] `python3 -m mario_rl.play --config ... --eval.checkpoint ...` loads a
  Lightning checkpoint and runs a configurable number of episodes.
- [ ] Evaluation writes metrics CSV/JSON under the experiment directory.
- [ ] Optional video recording works through Gymnasium-compatible wrappers.
- [ ] The train command writes a resolved config copy beside checkpoints/logs.
- [ ] README documents CPU, MPS, and CUDA commands.

### FR-5: End-To-End Smoke Contract
A user MUST be able to verify the completed modernization without a long run.

**Acceptance Criteria:**
- [ ] `./main.sh train --config smb_dqn_fast_dev --train.accelerator cpu`
  completes on a local machine within a short bounded frame/step budget.
- [ ] On a Mac with MPS available, the same fast-dev config completes with an
  MPS override.
- [ ] On a Linux server with CUDA available, the same fast-dev config completes
  with a CUDA/GPU override.
- [ ] A checkpoint from the smoke run can be loaded by the play command for one
  short evaluation episode or capped rollout.

---

## TDD Plan
1. Red: add LightningModule construction tests that assert model, target model,
   optimizer, and schedule state are initialized from config.
2. Red: add fake-env fast-dev-run tests using `lightning.pytorch.Trainer` with
   a tiny step/frame budget.
3. Red: add checkpoint round-trip tests that save, load, and compare Q-values
   for a fixed input.
4. Red: add CLI smoke tests for train and play using fake env configs.
5. Green: implement LightningModule, rollout/replay integration, checkpoint
   hooks, loggers, train/play commands, and artifact writing.
6. Refactor: keep environment creation, model factories, replay, and CLI config
   separated so each package remains unit-testable.
7. Regression: run CPU tests, run real Mario capped smoke, and run MPS/CUDA
   gated checks where hardware exists.

---

## BDD Scenarios

### Scenario: Local CPU Fast Dev Training
**Given** a fresh local install and the packaged `smb_dqn_fast_dev` config
**When** I run `./main.sh train --config smb_dqn_fast_dev
--train.accelerator cpu`
**Then** Lightning completes the bounded smoke run, writes a checkpoint/logs,
and exits without importing TensorFlow or Keras.

### Scenario: MacBook MPS Training
**Given** a MacBook where PyTorch reports MPS as available
**When** I run the same fast-dev config with `--train.accelerator mps`
**Then** the model tensors are placed on MPS and the bounded smoke run
completes.

### Scenario: Linux CUDA Training
**Given** a Linux server where PyTorch reports CUDA as available
**When** I run the same fast-dev config with a CUDA/GPU accelerator override
**Then** the model tensors are placed on CUDA and the bounded smoke run
completes.

### Scenario: Play From Checkpoint
**Given** a checkpoint written by a smoke training run
**When** I run the play command for one capped episode
**Then** the checkpoint loads, actions are selected from the PyTorch model, and
metrics are written under the experiment directory.

---

## Verification Commands
Run from `playing-mario-with-deep-reinforcement-learning/`.

```bash
python3 -m unittest mario_rl.lightning.tests
python3 -m unittest mario_rl.tests.test_train_cli
python3 -m unittest mario_rl.tests.test_play_cli
python3 -m unittest discover .
./main.sh unittest
./main.sh train --config smb_dqn_fast_dev --train.accelerator cpu
python3 -m mario_rl.play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32
```

Optional hardware-gated checks:

```bash
python3 - <<'PY'
import torch
print('mps', torch.backends.mps.is_available())
print('cuda', torch.cuda.is_available())
PY
./main.sh train --config smb_dqn_fast_dev --train.accelerator mps
MARIO_RL_RUN_CUDA_SMOKE=1 ./main.sh train --config smb_dqn_fast_dev --train.accelerator gpu --train.devices 1
```

---

## Completion Signal Expectations
- [ ] All acceptance criteria are verified.
- [ ] Red and green test commands and outputs are recorded in the completion
  log.
- [ ] Child submodule changes are committed and pushed first.
- [ ] Umbrella submodule pointer and any root spec/history updates are
  committed and pushed second.
- [ ] Only after the above, output `DONE`.

<!-- NR_OF_TRIES: 0 -->

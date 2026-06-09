# Specification: Playing Mario PyTorch DQN Core

## Feature: PyTorch DQN Models, Losses, Schedules, And Replay

### Overview
Replace the active Keras model and training primitives with PyTorch modules
that can be consumed by Lightning. Preserve the useful DQN concepts from the
legacy project while removing Keras masks, `.h5` assumptions, TensorFlow
imports, and deprecated NumPy dtypes.

### User Stories
- As a model developer, I want DQN and Dueling DQN implemented as
  `torch.nn.Module` classes so that they run on CPU, MPS, or CUDA.
- As a researcher, I want replay and epsilon schedules tested independently so
  that training behavior is reproducible.
- As a Ralph agent, I want shape, dtype, and one-step optimization tests so
  that the Lightning spec starts from a trustworthy model core.

---

## Problem Or Goal
The current model builders return compiled Keras `Model` objects with a second
mask input. The training code uses Keras prediction and batch-update methods,
old optimizer objects, and `.h5` weights. A modern PyTorch DQN core should
express selected-action training with tensor indexing/gathering, not model
input masks.

---

## Scope

### In Scope
- Implement PyTorch `DQN` and `DuelingDQN` modules under `mario_rl.models`.
- Implement model factory helpers driven by the typed config from spec 003.
- Implement Huber/SmoothL1 TD loss helpers using PyTorch tensors.
- Modernize replay memory into testable data structures that return tensor or
  NumPy batches with explicit dtype and shape contracts.
- Preserve uniform replay and either preserve prioritized replay or gate it
  behind a tested config option if it is not part of the first Lightning path.
- Add tests for model shape, dueling aggregation, loss values, replay sampling,
  epsilon/annealing schedules, and one optimizer step.

### Out Of Scope
- LightningModule training loops.
- Environment rollout orchestration.
- Loading old Keras `.h5` checkpoints.
- Full training convergence.

---

## Functional Requirements

### FR-1: PyTorch Model Architectures
The active model implementations MUST be native PyTorch modules.

**Acceptance Criteria:**
- [ ] `DQN` accepts channel-first tensors with shape `(batch, channels,
  height, width)` and returns Q-values with shape `(batch, num_actions)`.
- [ ] `DuelingDQN` returns the same shape and combines value and advantage as
  `Q(s, a) = V(s) + A(s, a) - mean_a A(s, a)`.
- [ ] Input normalization is explicit and tested, either in preprocessing or
  inside the model wrapper.
- [ ] Model factories read architecture and dimensions from typed config.
- [ ] No active model module imports `keras` or `tensorflow`.

### FR-2: TD Loss And Action Selection Helpers
The DQN update math MUST be expressed in PyTorch.

**Acceptance Criteria:**
- [ ] Selected Q-values are gathered with action indices rather than a Keras
  mask input.
- [ ] TD targets handle terminal and truncated transitions explicitly.
- [ ] Optional Double-DQN target selection is implemented or marked as a
  tested unsupported config value until the Lightning spec implements it.
- [ ] Huber/SmoothL1 loss tests compare expected scalar values on fixed
  tensors.
- [ ] A single optimizer step on a synthetic batch produces a finite loss and
  changes at least one trainable parameter.

### FR-3: Replay Memory Contract
Replay data MUST have predictable shapes and dtypes.

**Acceptance Criteria:**
- [ ] Uniform replay buffer push/sample behavior is covered by tests.
- [ ] Sampling from a partially filled buffer never returns `None` entries.
- [ ] Sampled batches include `state`, `action`, `reward`, `terminated`,
  `truncated`, and `next_state`.
- [ ] Boolean fields use `bool` or `np.bool_`, not deprecated `np.bool`.
- [ ] Prioritized replay, if retained, has tests for priority insertion,
  sampling weights, and priority updates.
- [ ] Replay structures avoid unnecessary tensor copies on CPU but can move
  batches to a requested torch device.

### FR-4: Schedule And Randomness Utilities
Exploration schedules MUST be deterministic and testable.

**Acceptance Criteria:**
- [ ] Epsilon schedule behavior is covered at first, middle, and final steps.
- [ ] Schedule state can be serialized in a checkpoint-friendly form.
- [ ] Random action selection can be seeded in tests.
- [ ] Config values control start epsilon, final epsilon, and decay frames.

---

## TDD Plan
1. Red: add tests that expect `mario_rl.models.DQN` and `DuelingDQN` to return
   `(batch, actions)` tensors from fixed channel-first inputs.
2. Red: add tests for dueling aggregation using controlled layer outputs or a
   small deterministic module.
3. Red: add replay-memory tests for shape, dtype, partial fill behavior, and
   terminal/truncated flags.
4. Red: add one-step optimization tests on a fake batch.
5. Green: implement models, factories, losses, replay, and schedules.
6. Refactor: delete or quarantine Keras-only active imports and keep legacy
   code out of the `mario_rl` package.
7. Regression: run all unit tests on CPU.

---

## BDD Scenarios

### Scenario: Build A DQN From Config
**Given** a typed config with `model.architecture: dqn` and a seven-action
Mario env
**When** I build the model and pass two stacked-frame observations
**Then** the model returns a finite `(2, 7)` tensor without importing Keras.

### Scenario: Sample Replay For Training
**Given** a replay buffer filled with deterministic fake transitions
**When** I sample a batch of four transitions
**Then** states, next states, actions, rewards, terminated flags, and truncated
flags have the documented shapes and dtypes.

### Scenario: One Synthetic TD Update
**Given** a DQN, target DQN, optimizer, and a synthetic replay batch
**When** I compute TD targets and step the optimizer once
**Then** the loss is finite and model parameters update on CPU.

---

## Verification Commands
Run from `playing-mario-with-deep-reinforcement-learning/`.

```bash
python3 -m unittest mario_rl.models.tests
python3 -m unittest mario_rl.replay.tests
python3 -m unittest mario_rl.tests.test_schedules
python3 -m unittest discover .
python3 - <<'PY'
import torch
from mario_rl.models import DQN
model = DQN(input_channels=4, num_actions=7)
x = torch.zeros(2, 4, 84, 84)
y = model(x)
assert y.shape == (2, 7)
assert torch.isfinite(y).all()
print(y.shape)
PY
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

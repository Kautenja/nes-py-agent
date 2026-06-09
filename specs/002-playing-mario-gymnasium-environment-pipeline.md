# Specification: Playing Mario Gymnasium Environment Pipeline

## Feature: Modern Mario Environment Factory And Wrappers

### Overview
Migrate the Mario learner's environment setup and preprocessing wrappers from
old Gym conventions to the current Gymnasium contract used by `nes-py` and
`gym-super-mario-bros`. The result should be a deterministic, testable Mario
environment factory suitable for PyTorch training.

### User Stories
- As a researcher, I want `SuperMarioBros1-1-v0` to reset and step through the
  modern Gymnasium API so that experiments run with current wrappers.
- As a model developer, I want preprocessing output with stable shape and dtype
  so that PyTorch tensors are created predictably.
- As a Ralph agent, I want fake-env tests and real Mario smoke tests so that
  wrapper regressions are caught before training work starts.

---

## Problem Or Goal
The current code imports `gym`, calls four-value `step`, assumes one-value
`reset`, uses removed `gym.wrappers.Monitor`, and imports
`BinarySpaceToDiscreteSpaceEnv`, which is not exposed by the modern local
`nes-py` wrapper package. This blocks current `gym-super-mario-bros` and
Gymnasium usage.

---

## Scope

### In Scope
- Replace active environment imports with `gymnasium`.
- Replace the old binary-to-discrete action wrapper with
  `nes_py.wrappers.JoypadSpace`.
- Build a `mario_rl.envs` package that owns Mario environment creation and
  preprocessing.
- Update or replace wrappers for Gymnasium reset/step semantics.
- Preserve deterministic seeding, episode reward accounting, frame skipping,
  reward clipping, downsampling, and frame stacking behavior where still
  useful.
- Add unit tests against tiny fake Gymnasium envs and smoke tests against a
  representative real Mario env.

### Out Of Scope
- Rewriting the DQN model in PyTorch.
- Creating Lightning training loops.
- Supporting Atari or Tetris as first-class training targets.
- Adding new ROM assets.

---

## Functional Requirements

### FR-1: Gymnasium Env Factory
The modern package MUST expose a Mario-focused environment factory.

**Acceptance Criteria:**
- [ ] A public factory creates Gymnasium-compatible envs from env IDs such as
  `SuperMarioBros1-1-v0` and `SuperMarioBros-v0`.
- [ ] The factory accepts `render_mode`, `seed`, action-set selection
  (`right_only`, `simple`, `complex`), and preprocessing options from config
  objects or explicit keyword arguments.
- [ ] `JoypadSpace` is used for discrete action mapping.
- [ ] The factory returns an env whose `reset(seed=...)` returns
  `(observation, info)` and whose `step(action)` returns
  `(observation, reward, terminated, truncated, info)`.
- [ ] The old `gym.wrappers.Monitor` path is replaced with Gymnasium-compatible
  record-statistics and optional video recording wrappers.

### FR-2: Preprocessing Contract
Preprocessing MUST produce stable tensors for the PyTorch specs that follow.

**Acceptance Criteria:**
- [ ] Downsampling has explicit image size, interpolation, grayscale/color, and
  dtype behavior.
- [ ] Frame stacking returns a predictable shape documented in tests.
- [ ] The chosen training shape is compatible with PyTorch channel-first model
  code, either by producing `(C, H, W)` directly or by documenting where the
  transpose occurs.
- [ ] Rewards, termination, truncation, and raw score metadata are preserved in
  `info` or wrapper attributes for logging.
- [ ] Wrapper tests cover both `terminated=True` and `truncated=True`.

### FR-3: Deterministic Smoke Behavior
The factory MUST be deterministic when seeded.

**Acceptance Criteria:**
- [ ] Resetting the same Mario env twice with the same seed produces the same
  initial observation shape and stable metadata.
- [ ] A fixed short action sequence produces the same termination/truncation
  flags and compatible rewards across repeated runs on the same platform.
- [ ] Random-stage environments preserve seeded stage selection behavior.
- [ ] Envs are always closed in tests, including failure paths.

### FR-4: Legacy Surface Cleanup
The active code path MUST stop depending on old Gym-specific helpers.

**Acceptance Criteria:**
- [ ] No active modern module imports `gym`.
- [ ] No active modern module imports `BinarySpaceToDiscreteSpaceEnv`.
- [ ] No active modern module calls `gym.wrappers.Monitor`.
- [ ] Any legacy modules left in place are clearly documented as legacy and are
  not imported by `mario_rl`.

---

## TDD Plan
1. Red: add fake-env wrapper tests for Gymnasium `reset` and five-value
   `step`, including terminated and truncated cases.
2. Red: add a Mario env factory smoke test that imports
   `gym_super_mario_bros`, creates `SuperMarioBros1-1-v0`, applies the action
   and preprocessing wrappers, resets with a fixed seed, takes one step, and
   closes the env.
3. Green: implement the `mario_rl.envs` factory and migrate wrappers until the
   fake-env and real-env smoke tests pass.
4. Refactor: remove duplicate wrapper logic, document the observation contract,
   and keep the API narrow enough for the Lightning DataModule spec.
5. Regression: run the full child unittest suite plus a no-training random
   rollout smoke command.

---

## BDD Scenarios

### Scenario: Seeded Mario Reset
**Given** a configured Mario env factory for `SuperMarioBros1-1-v0`
**When** I create two envs with the same seed and reset them
**Then** both resets return Gymnasium two-tuples with matching observation
shape and comparable metadata.

### Scenario: One-Step Preprocessed Rollout
**Given** a preprocessed Mario env using `simple` movement
**When** I sample one discrete action and call `step`
**Then** the result is a five-tuple, the observation has the documented
training shape, the reward is numeric, and the env closes cleanly.

### Scenario: Optional Video Recording
**Given** video recording is enabled in config
**When** a short episode or capped rollout runs
**Then** Gymnasium-compatible video/statistics artifacts are written under the
experiment output directory without using removed Monitor APIs.

---

## Verification Commands
Run from `playing-mario-with-deep-reinforcement-learning/`.

```bash
python3 -m unittest mario_rl.envs.tests.test_wrappers
python3 -m unittest mario_rl.envs.tests.test_mario_env_factory
python3 -m unittest discover .
python3 - <<'PY'
from mario_rl.envs import make_env
env = make_env('SuperMarioBros1-1-v0', render_mode='rgb_array', seed=123)
try:
    obs, info = env.reset(seed=123)
    result = env.step(env.action_space.sample())
    assert len(result) == 5
    print(obs.shape, type(info).__name__, env.action_space.n)
finally:
    env.close()
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

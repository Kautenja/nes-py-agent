# Specification: Playing Mario Config CLI Project Layout

## Feature: TISV-Style Config And Entrypoints

### Overview
Organize the modern Mario learner like the referenced TISV project: an
importable package, typed single-file YAML configs, package-module entrypoints,
and a small `main.sh` that exposes common commands. This spec creates the
control surface that later PyTorch and Lightning work will use.

### User Stories
- As a researcher, I want packaged config names such as `smb_dqn_fast_dev` so
  that I can run repeatable experiments without copying shell flags around.
- As a developer, I want `python3 -m mario_rl.train --config ...` style
  entrypoints so that commands are importable, testable, and notebook-friendly.
- As a Ralph agent, I want typed config tests so that future specs can add
  training behavior without guessing about option names.

---

## Problem Or Goal
The current project exposes a top-level `python .` CLI that takes a few
argparse flags and hardcodes most training details inside `src/train.py` and
`DeepQAgent`. The TISV reference uses package-module entrypoints, typed
dataclass config, packaged YAML config discovery, nested CLI overrides, and
`main.sh` commands. The Mario learner needs the same style before the training
implementation is rebuilt.

---

## Scope

### In Scope
- Create `mario_rl.config` with stdlib dataclasses and a reusable
  jsonargparse-based `cli()` helper.
- Add package data configs under `mario_rl/config/data/*.yaml`.
- Add package-module entrypoints with `main(argv=None)` or `run(config)` APIs
  for at least config listing, training, play/evaluation, and random rollout.
- Add or update `main.sh` commands for `unittest`, `train`, `play`, `random`,
  and `config`.
- Document the CLI in README using the same concise style as TISV.

### Out Of Scope
- Implementing real PyTorch training behavior.
- Implementing model export, quantization, or Docker workflows.
- Preserving the exact old `python . -m train` CLI, except as an optional
  compatibility note.

---

## Functional Requirements

### FR-1: Typed Config Schema
The project MUST have a single typed config tree that covers the planned
training workflow.

**Acceptance Criteria:**
- [ ] Config dataclasses cover top-level experiment fields:
  `experiment_name`, `save_dir`, and device/trainer settings.
- [ ] Config dataclasses cover environment settings: env ID, render mode,
  action set, seed, image size, frame stack, reward clipping, frame skipping,
  video/statistics options, and max smoke steps.
- [ ] Config dataclasses cover replay settings: capacity, batch size, warmup,
  prioritized replay flag, alpha/beta if prioritized replay is enabled, and
  sample dtype/shape assumptions.
- [ ] Config dataclasses cover model settings: architecture (`dqn` or
  `dueling_dqn`), input channels, hidden size, optimizer, learning rate,
  discount factor, Double-DQN flag, target update frequency, and compile flag.
- [ ] Config dataclasses cover training and evaluation settings: max frames or
  max steps, fast-dev-run, log intervals, checkpoint path, evaluation episodes,
  epsilon schedule, and output artifact names.

### FR-2: Packaged Config Discovery
Packaged YAML configs MUST be discoverable by name.

**Acceptance Criteria:**
- [ ] `python3 -m mario_rl.config list` prints packaged config names.
- [ ] `python3 -m mario_rl.config path smb_dqn_fast_dev` prints an absolute
  path to the packaged YAML.
- [ ] `mario_rl.config.load('smb_dqn_fast_dev')` returns a typed config object.
- [ ] Config names and file paths both work with `--config`.
- [ ] Nested CLI overrides such as `--train.fast_dev_run true` and
  `--env.id SuperMarioBros1-1-v0` override the YAML.
- [ ] Bare `KEY=VALUE` positional overrides are rejected unless explicitly
  documented and tested.

### FR-3: Package-Module Entrypoints
Entrypoints MUST be importable and testable without executing work at import
time.

**Acceptance Criteria:**
- [ ] `python3 -m mario_rl.train --help` prints generated config help.
- [ ] `python3 -m mario_rl.play --help` prints generated config help.
- [ ] `python3 -m mario_rl.random --help` or an equivalent evaluation
  entrypoint is present for non-training smoke checks.
- [ ] Each entrypoint exposes a testable `main(argv=None)` and avoids reading
  `sys.argv` outside that function.
- [ ] Importing each entrypoint does not create environments, start training,
  or import TensorFlow/Keras.

### FR-4: TISV-Style Command Wrapper
The project MUST provide a small shell wrapper for common commands.

**Acceptance Criteria:**
- [ ] `./main.sh` prints command help.
- [ ] `./main.sh unittest` runs unittest discovery.
- [ ] `./main.sh config list` delegates to `python3 -m mario_rl.config list`.
- [ ] `./main.sh train --config smb_dqn_fast_dev ...` delegates to
  `python3 -m mario_rl.train`.
- [ ] `./main.sh play --config ... --eval.checkpoint ...` delegates to the play
  entrypoint.

---

## TDD Plan
1. Red: add config package tests for `available_configs`, `config_path`,
   `load`, file-path loading, nested overrides, and invalid overrides.
2. Red: add CLI tests that call `main(argv)` for config, train help, play help,
   and random help without starting a rollout.
3. Green: implement the config dataclasses, YAML package data, CLI helper, and
   command modules with no-op or stub `run(config)` bodies where later specs
   will add behavior.
4. Refactor: make shared CLI resolution code live in `mario_rl.config`, not in
   individual entrypoints.
5. Regression: run full unittest discovery and verify packaged config files
   are included in editable installs.

---

## BDD Scenarios

### Scenario: Discover Packaged Configs
**Given** the package is installed in editable mode
**When** I run `python3 -m mario_rl.config list`
**Then** I see at least `smb_dqn_fast_dev`, `smb_dqn_cpu`, and one
accelerator-oriented config for `mps` or `cuda`.

### Scenario: Override A Fast Dev Run
**Given** the packaged `smb_dqn_fast_dev` config
**When** I run `python3 -m mario_rl.train --config smb_dqn_fast_dev
--train.fast_dev_run true --env.id SuperMarioBros1-1-v0`
**Then** config parsing succeeds and the resulting typed object contains the
overridden values.

### Scenario: Use Main Script
**Given** I am in the child project root
**When** I run `./main.sh unittest`
**Then** the same unittest suite runs as `python3 -m unittest discover .`.

---

## Verification Commands
Run from `playing-mario-with-deep-reinforcement-learning/`.

```bash
python3 -m unittest mario_rl.config.tests
python3 -m unittest mario_rl.tests.test_entrypoints
python3 -m mario_rl.config list
python3 -m mario_rl.config path smb_dqn_fast_dev
python3 -m mario_rl.train --help
python3 -m mario_rl.play --help
./main.sh
./main.sh unittest
python3 -m unittest discover .
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

# Playing Mario MacBook Trainability Guardrails

## Status: TODO

## Problem

The active Mario modernization queue has unit tests and smoke commands, but it
does not yet enforce a repeatable MacBook trainability gate. The end result
must be something that can actually run short training jobs locally, produce
metrics, expose obvious performance regressions, and give each later spec a
concrete verification target beyond isolated unit tests.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if the
  local trainability harness exposes environment or emulator defects.
- Add a small, repeatable verification harness for CPU and Apple Silicon MPS
  where available.
- Add mini training/evaluation configs that are intentionally tiny but exercise
  real Gymnasium environments, model optimization, checkpoint writing, metrics
  writing, and replay or rollout data flow.
- Add lightweight profiling/benchmark output that can guide optimization work
  without requiring a long training run.

## Repository And Release Rules

- Maintain local editable installs during implementation:
  `python -m pip install -e ../nes-py -e ../gym-super-mario-bros -e .`
  from `playing-mario-with-deep-reinforcement-learning`.
- If `nes-py` or `gym-super-mario-bros` must change, create a new child branch
  such as `codex/playing-mario-macbook-trainability-guardrails` before editing
  that child repo.
- If child repo behavior changes, bump that child package version and update
  its changelog, but do not publish or push.
- Defer the final release flow to the user: release `nes-py` first, then
  `gym-super-mario-bros`, then update `mario_rl` dependency lower bounds and
  release it after human approval.

## Acceptance Criteria

- `mario_rl` has a single documented command or script for the local MacBook
  gate, for example `./main.sh verify-macbook` or an equivalent subcommand.
- The gate runs the fast unit test subset first, then a real-environment mini
  training run, then a tiny evaluation/play run against the produced
  checkpoint.
- The gate works on CPU-only Macs and automatically uses MPS only when
  available, with a clear skip message when MPS is unavailable.
- The mini training run performs real optimizer steps, writes a checkpoint,
  writes resolved config, writes metrics, and verifies those artifacts exist
  and are nonempty.
- The mini run is bounded for laptop use: small image size or batch size where
  appropriate, short episode/step limits, no rendering by default, deterministic
  seed, and no long-running full-game training.
- The gate records elapsed wall time, environment frames per second, optimizer
  steps per second, peak memory if reasonably available, device, Python
  version, PyTorch version, and selected environment/task IDs.
- A performance budget is documented for the mini gate. The first
  implementation may set conservative warning thresholds rather than hard
  failures, but the output must make slowdowns obvious.
- There is a repeatable benchmark/profiling mode for environment stepping and
  one mini optimization pass so later specs can compare before/after numbers.
- The completion log for this spec includes one successful local gate run and
  the recorded timing/performance summary.

## Unit Tests

- Unit-test the gate command argument parsing without running long jobs.
- Unit-test device selection for CPU and mocked MPS availability.
- Unit-test artifact verification against temporary files/directories.
- Unit-test metrics parsing and budget warning/failure behavior.
- Unit-test benchmark summary formatting.
- Unit-test that mini configs are loadable and have bounded step counts.
- Unit-test that the gate can run against fake train/eval callables for fast
  control-flow coverage.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.config.tests.test_config
python -m unittest mario_rl.tests.test_train_cli
python -m unittest mario_rl.tests.test_play_cli
python -m unittest discover .
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
./main.sh play --config smb_dqn_fast_dev --eval.episodes 1 --eval.max_steps 32
./main.sh verify-macbook
```

If MPS is available on the current Mac, also verify the MPS mini gate:

```shell
./main.sh verify-macbook --device mps
```

If `gym-super-mario-bros` changes, run from that child repo:

```shell
python -m unittest gym_super_mario_bros.tests.test_tasks
python -m unittest gym_super_mario_bros.tests.test_registration
python -m unittest discover .
```

If `nes-py` changes, run the focused Python and native checks appropriate to
the touched emulator area and record those commands in the completion log.

## Guardrail For Later Specs

After this spec is complete, every active Mario RL modernization spec must run
the fast unit tests it adds, the full `mario_rl` unittest suite, and the
MacBook gate unless the spec explicitly documents why the gate is temporarily
not applicable. Specs that add a new algorithm, data path, or model head must
also add a tiny train/eval config that the gate or an equivalent smoke command
can exercise.

## Completion Signal Expectations

- The local MacBook trainability gate exists, is documented, and passes.
- Unit tests cover gate control flow, artifacts, metrics, and device selection.
- Any child submodule changes are committed locally before umbrella pointer
  updates.
- Completion log includes the gate output summary and any optimization notes.
- Output `DONE` only after tests, mini training, mini evaluation, performance
  summary, history updates, and required local commits are complete.

<!-- NR_OF_TRIES: 0 -->

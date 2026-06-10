# Playing Mario Recurrent Actor Critic

## Status: TODO

Roadmap item: 8.

## Problem

The active learner is a single-env DQN baseline. A single network that plays
many Mario games needs an on-policy or actor-learner path that supports
parallel rollout, recurrent memory, task conditioning, and policy/value
optimization. PPO or APPO is the pragmatic first implementation; IMPALA-style
V-trace can come later if throughput becomes the blocker.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  environment semantics block vectorized or recurrent rollout.
- Add a new actor-critic training path beside the existing DQN path.
- Implement recurrent policy/value models using the task-conditioning contract
  from spec 006.
- Implement rollout storage, generalized advantage estimation, PPO losses, and
  small CPU smoke training.
- Keep DQN tests and configs passing.

## Repository And Release Rules

- Keep local editable installs active.
- If `nes-py` or `gym-super-mario-bros` needs changes for vectorization,
  reset semantics, or info consistency, create a child branch such as
  `codex/playing-mario-recurrent-actor-critic`.
- Bump child versions only for child behavior changes. Do not release or push.
- Record any final release dependency notes in the completion log.

## Acceptance Criteria

- `mario_rl` has a new model architecture for actor-critic policies with:
  visual encoder, optional task embedding, recurrent memory, policy head, and
  value head.
- Rollout storage handles observations, actions, log probabilities, rewards,
  dones, values, recurrent states, task features, and selected `info` metrics.
- PPO loss includes clipped policy loss, value loss, entropy bonus, advantage
  normalization, and configurable gradient clipping.
- Recurrent state resets correctly on terminated or truncated episodes.
- The training CLI can select DQN or PPO-style actor-critic through config.
- A tiny fake-env unit test verifies one optimization step without ROMs.
- A CPU smoke config runs a short Mario rollout/training pass against local
  editable installs.
- DQN remains available and existing DQN smoke tests pass.
- Documentation explains that actor-critic is the recommended path for
  all-game policy training, while DQN remains a baseline.

## Unit Tests

- Unit-test actor-critic forward shapes with and without task conditioning.
- Unit-test recurrent hidden-state reset masks.
- Unit-test rollout buffer insertion, minibatch iteration, and GAE values.
- Unit-test PPO loss on deterministic toy tensors.
- Unit-test config parsing and CLI selection for the new algorithm.
- Unit-test fake-env one-step or few-step optimization.
- Unit-test that existing DQN model and Lightning tests still pass.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.models.tests.test_models
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest mario_rl.config.tests.test_config
python -m unittest mario_rl.tests.test_train_cli
python -m unittest discover .
./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false
./main.sh train --config <new_actor_critic_fast_dev_config> --trainer.enable_progress_bar false
./main.sh unittest
```

After spec `005-playing-mario-macbook-trainability-guardrails` is complete,
also run:

```shell
./main.sh verify-macbook
```

If MPS is available on the current Mac, also run:

```shell
./main.sh verify-macbook --device mps
```

Replace `<new_actor_critic_fast_dev_config>` with the packaged config added by
this spec.

If environment changes are needed:

```shell
python -m unittest discover .
```

from each touched child repo, plus focused tests for reset/step/info behavior.

## Completion Signal Expectations

- Actor-critic smoke training works and DQN remains green.
- Child repo changes, if any, are committed locally before umbrella updates.
- Completion log records the algorithm/config names and test commands.
- Output `DONE` only after all verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

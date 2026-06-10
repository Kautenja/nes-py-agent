# Playing Mario Auxiliary Losses

## Status: TODO

Roadmap item: 10.

## Problem

The 9.x environment surface exposes cross-game signals such as progress,
clear/death flags, reward components, status, score, coins, and SMB2/SMB3
game-specific state. A shared Mario representation should learn from these
signals even when sparse task rewards are noisy. Auxiliary prediction heads can
regularize the visual/recurrent encoder and improve transfer across games.

## Scope

- Primary target: `playing-mario-with-deep-reinforcement-learning`.
- Allowed supporting targets: `gym-super-mario-bros` and `nes-py` only if
  auxiliary targets reveal missing or inconsistent `info` fields.
- Add optional auxiliary heads and losses to the actor-critic path from spec
  011.
- Reuse reward/metrics contracts from specs 009 and 010.
- Keep all auxiliary losses disabled by default unless a config opts in.

## Repository And Release Rules

- Use local editable installs during implementation.
- If `nes-py` or `gym-super-mario-bros` needs info-field fixes, create a child
  branch such as `codex/playing-mario-auxiliary-losses` before editing.
- Bump child versions only for child behavior changes and defer publication to
  the coordinated release.

## Acceptance Criteria

- Config supports enabling/disabling auxiliary targets and per-loss weights.
- Supported targets include at least: progress delta or normalized progress,
  clear flag, death flag, transformed reward or reward component totals, and
  game-family classification.
- Rollout storage records the required target values from `info` with explicit
  missing-value masks.
- Auxiliary heads share the main encoder/recurrent state and produce stable
  shape outputs.
- Total loss reports main policy/value losses and each auxiliary term
  separately.
- Missing or unavailable targets do not silently train on garbage values.
- Unit tests cover fake multi-game batches with partial target availability.
- Documentation explains when to enable auxiliary losses and how to interpret
  their metrics.

## Unit Tests

- Unit-test target extraction from representative `info` dictionaries.
- Unit-test missing-target masks.
- Unit-test auxiliary head forward shapes.
- Unit-test loss computations for regression and classification targets.
- Unit-test weighted total loss composition.
- Unit-test config parsing for enabled targets and weights.
- Unit-test a fake actor-critic training step with auxiliary losses enabled.

## Verification Commands

Run from `playing-mario-with-deep-reinforcement-learning`:

```shell
python -m unittest mario_rl.models.tests.test_models
python -m unittest mario_rl.lightning.tests.test_module
python -m unittest mario_rl.config.tests.test_config
python -m unittest discover .
./main.sh train --config <auxiliary_actor_critic_fast_dev_config> --trainer.enable_progress_bar false
./main.sh unittest
```

Replace `<auxiliary_actor_critic_fast_dev_config>` with the packaged config
added by this spec.

If wrapper info fields change:

```shell
python -m unittest gym_super_mario_bros.tests.test_smv_env
python -m unittest gym_super_mario_bros.tests.test_smb2_env
python -m unittest gym_super_mario_bros.tests.test_smb3_env
python -m unittest discover .
```

## Completion Signal Expectations

- Auxiliary losses are optional, tested, and documented.
- Actor-critic smoke training still works with auxiliary losses enabled.
- Child repo changes, if any, are committed locally before umbrella updates.
- Completion log records enabled auxiliary targets and verification commands.
- Output `DONE` only after verification and local commits are complete.

<!-- NR_OF_TRIES: 0 -->

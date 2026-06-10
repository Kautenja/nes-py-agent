# Playing Mario Recurrent Actor Critic

## Summary

Implemented recurrent PPO actor-critic training in
`playing-mario-with-deep-reinforcement-learning` with algorithm selection
through `train.algorithm`.

The new path includes:

- `RecurrentActorCritic` with visual encoding, optional task embedding, GRU
  memory, policy logits, and value estimates.
- `RolloutStorage` with observations, actions, old log probabilities, rewards,
  termination/truncation masks, values, recurrent states, task features,
  selected reward/info diagnostics, GAE returns, and minibatches.
- Clipped PPO losses with value loss, entropy bonus, advantage normalization,
  approximate KL/clip-fraction metrics, and configurable gradient clipping.
- `PPOLightningModule` and packaged `smb_ppo_fast_dev` smoke config.
- Focused fake-env tests plus README documentation that recommends
  actor-critic for all-game policy training while retaining DQN as a baseline.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning`:

- `.venv/bin/python -m unittest mario_rl.models.tests.test_models`
- `.venv/bin/python -m unittest mario_rl.lightning.tests.test_module`
- `.venv/bin/python -m unittest mario_rl.config.tests.test_config`
- `.venv/bin/python -m unittest mario_rl.tests.test_train_cli`
- `.venv/bin/python -m unittest discover .`
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar false`
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar false`
- `./main.sh unittest`
- `./main.sh verify-macbook`
- `./main.sh verify-macbook --device mps`

Notes:

- The host has no `python` shim, so direct Python module verification used
  `.venv/bin/python`; `main.sh` selects the same interpreter automatically.
- `smb_dqn_fast_dev` completed with `env_frames=128` and `algorithm=dqn`.
- `smb_ppo_fast_dev` completed with `env_frames=64` and `algorithm=ppo`.
- MacBook gate CPU completed with train `2.47s`, eval `2.11s`, env FPS
  `12.97`, optimizer `2.84` steps/s, and no warnings.
- MacBook gate MPS completed with train `2.74s`, eval `2.09s`, env FPS
  `11.70`, optimizer `2.56` steps/s, and no warnings.
- Explicit MPS gate completed with train `2.79s`, eval `2.37s`, env FPS
  `11.47`, optimizer `2.51` steps/s, and no warnings.

## Commits

- Child `playing-mario-with-deep-reinforcement-learning`: `58b8d38`
  (`Add recurrent PPO actor-critic training`), pushed to `origin/pytorch`.
- Umbrella: recorded in the companion root commit for this completion log.

## Release Notes

No child version bump was made because this is an unreleased development-path
training feature. The release-facing summary was added to `CHANGELOG.md`.

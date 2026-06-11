# Playing Mario Recurrent Actor Critic

Completed recurrent PPO actor-critic training for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added a `RecurrentActorCritic` model with the existing visual encoder style,
  optional task feature embedding, GRU memory, policy logits, value estimates,
  and explicit recurrent-state reset masking.
- Added `RolloutStorage` for on-policy observations, actions, log
  probabilities, rewards, termination/truncation masks, values, recurrent
  states, task features, reward diagnostics, frame counts, GAE advantages, and
  minibatch iteration.
- Added clipped PPO loss helpers with advantage normalization, value loss,
  entropy bonus, approximate KL, clip fraction, and configurable gradient
  clipping in the Lightning module.
- Added `PPOLightningModule` beside the DQN module and selected it through
  `train.algorithm: ppo`; DQN remains the default baseline.
- Added the packaged `smb_ppo_fast_dev` CPU smoke config using
  `model.architecture: recurrent_actor_critic` and task conditioning.
- Documented recurrent actor-critic as the recommended all-game training path
  while keeping DQN as a compact baseline.

Verification highlights:

- Focused model, config, Lightning, train CLI, PPO loss, and rollout tests
  passed.
- Full unittest discovery and `./main.sh unittest` passed with 142 tests and
  7 skips.
- `./main.sh train --config smb_dqn_fast_dev --trainer.enable_progress_bar
  false` passed with `env_frames=128` and `algorithm=dqn`.
- `./main.sh train --config smb_ppo_fast_dev --trainer.enable_progress_bar
  false` passed with `env_frames=64` and `algorithm=ppo`.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings. CPU
  summary: train `2.47s`, eval `2.11s`, env FPS `12.97`, optimizer `2.84`
  steps/s. MPS summary: train `2.74s`, eval `2.09s`, env FPS `11.70`,
  optimizer `2.56` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with no warnings;
  train `2.79s`, eval `2.37s`, env FPS `11.47`, optimizer `2.51` steps/s.

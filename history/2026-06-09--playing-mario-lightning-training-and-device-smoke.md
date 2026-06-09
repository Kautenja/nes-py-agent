# Playing Mario Lightning Training And Device Smoke

Completed the Lightning-oriented training and checkpoint evaluation path in
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added `mario_rl.lightning` with a `DQNLightningModule` that owns the online
  Q-network, target Q-network, optimizer creation, epsilon schedule, Double-DQN
  target computation, uniform replay integration, and checkpointed counters.
- Environment rollout remains Gymnasium-native and keeps CPU NumPy
  observations in replay until tensor conversion at the training/evaluation
  boundary.
- `mario_rl.train` now runs bounded Lightning smoke jobs and writes a resolved
  config, Lightning CSV logs, train metrics, and checkpoints under
  `runs/<experiment_name>/`.
- `mario_rl.play` now loads Lightning checkpoints and writes evaluation metrics
  JSON for capped episodes, defaulting to the smoke checkpoint path.
- Fast tests use a deterministic fake Gymnasium env; real smoke checks verified
  CPU and MPS training plus checkpoint evaluation with the packaged Mario
  fast-dev config. CUDA remains gated because this host reported no CUDA.

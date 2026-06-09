# Playing Mario PyTorch DQN Core

Completed the active PyTorch model core in
`playing-mario-with-deep-reinforcement-learning` by adding `mario_rl.models`,
`mario_rl.replay`, and `mario_rl.schedules`.

Key points:

- `DQN` and `DuelingDQN` are native `torch.nn.Module` classes that accept
  channel-first `(batch, channels, height, width)` observations and normalize
  uint8-style inputs explicitly.
- The dueling model combines streams as `V + A - mean(A)`, and model factories
  build the requested architecture from the typed `MarioRLConfig`.
- DQN update helpers gather selected action values by index, compute
  terminal/truncated-aware TD targets, support Double-DQN target selection, and
  use PyTorch SmoothL1 loss.
- `UniformReplayBuffer` stores typed NumPy transition arrays with `state`,
  `action`, `reward`, `terminated`, `truncated`, and `next_state` fields, then
  moves batches to torch devices only at tensor boundaries.
- Prioritized replay is intentionally gated with a tested `NotImplementedError`
  until a later training path owns it.
- Linear epsilon schedules and seeded epsilon-greedy action selection are
  checkpoint-friendly and covered by tests.

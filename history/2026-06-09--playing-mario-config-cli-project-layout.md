# Playing Mario Config CLI Project Layout

Completed the TISV-style config and command surface in
`playing-mario-with-deep-reinforcement-learning` by adding `mario_rl.config`.

Key points:

- The modern learner now has a single typed dataclass config tree covering
  experiment, trainer/device, environment, replay, model, epsilon, training,
  and evaluation settings.
- Packaged configs live under `mario_rl/config/data/` and include
  `smb_dqn_fast_dev`, `smb_dqn_cpu`, and `smb_dqn_mps`.
- Configs can be discovered with `python3 -m mario_rl.config list`, resolved
  with `python3 -m mario_rl.config path NAME`, and loaded by packaged name or
  file path through `mario_rl.config.load`.
- Entry modules `mario_rl.train`, `mario_rl.play`, and `mario_rl.random` expose
  `main(argv=None)` and avoid environment creation at import time.
- Nested CLI overrides use explicit `--section.field value` syntax; bare
  positional `KEY=VALUE` overrides are rejected and covered by tests.
- `main.sh` now routes `unittest`, `config`, `train`, `play`, and `random`.

The train and play commands intentionally report the resolved config for now.
The PyTorch DQN and Lightning specs own real model training and checkpoint
evaluation behavior.

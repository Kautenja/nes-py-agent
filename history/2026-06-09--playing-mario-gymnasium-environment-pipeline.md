# Playing Mario Gymnasium Environment Pipeline

Completed the modern Mario environment surface in
`playing-mario-with-deep-reinforcement-learning` by adding `mario_rl.envs`.

Key points:

- `make_env` creates Gymnasium-compatible `gym-super-mario-bros` environments
  from IDs such as `SuperMarioBros1-1-v0`, `SuperMarioBros-v0`, and
  `SuperMarioBrosRandomStages-v0`.
- `nes_py.wrappers.JoypadSpace` owns action mapping for `right_only`, `simple`,
  and `complex` movement sets.
- The default preprocessing contract is channel-first grayscale frame stacks
  with shape `(4, 84, 84)` and `uint8` dtype.
- Fake-env tests cover Gymnasium reset/five-value step behavior, terminated and
  truncated paths, frame skipping, reward clipping, and raw reward metadata.
- Real Mario smoke tests cover seeded rollouts, random-stage seeding, optional
  OpenCV MP4 recording, and cleanup through `env.close()`.
- Legacy `src/` Gym/Keras modules remain documented as legacy and are not
  imported by `mario_rl`.

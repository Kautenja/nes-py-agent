# Playing Mario Universal Action Space

Completed universal action-space sizing for
`playing-mario-with-deep-reinforcement-learning`.

Key points:

- Added explicit `nes`, `right`, `right_only`, `simple`, and `complex`
  action-set resolution in `mario_rl.envs`.
- `action_set="nes"` now leaves the native Gymnasium environment unwrapped,
  preserving the 256-action NES controller space instead of passing it through
  `JoypadSpace`.
- `action_set="right"` is accepted as an alias for the existing `right_only`
  constrained movement list.
- Packaged configs now use `model.num_actions: auto`, and runtime config
  resolution converts that to a concrete model head size from the action set.
- Fixed numeric `model.num_actions` values are still supported, but train/play
  validation fails early when the configured count does not match the resolved
  action space.
- Train, play, random rollout, metrics CSVs, eval JSON, and MacBook gate
  summaries now report `action_set`, `action_count`, and native-action-space
  status.
- README guidance keeps `simple` as the intentional default for small smoke
  training and documents when universal all-game training may prefer `nes` or
  `complex`.

Verification highlights:

- Focused action/config/model/CLI tests passed, including native `nes` env
  creation with 256 actions and representative SMB1, Lost Levels, SMB2 USA,
  and SMB3 env creation.
- Full unittest discovery passed with 117 tests and 7 skips.
- `./main.sh random --config smb_dqn_fast_dev --env.action_set nes
  --env.max_smoke_steps 8` reported `action_set=nes` and `action_count=256`.
- `./main.sh verify-macbook` passed CPU and MPS with no budget warnings.
  CPU summary: train `2.48s`, eval `2.33s`, env FPS `12.93`, optimizer
  `2.83` steps/s. MPS summary: train `2.74s`, eval `2.31s`, env FPS `11.68`,
  optimizer `2.55` steps/s.
- Explicit `./main.sh verify-macbook --device mps` passed with train `2.50s`,
  eval `2.01s`, env FPS `12.82`, and optimizer `2.81` steps/s.

# Completion Log: Wrapper CLI Playback Parity

## Summary

Implemented CLI playback parity across `gym-super-mario-bros`, `gym-tetris`,
and `gym-zelda-1` with `--render/--no-render`, first-reset `--seed` handling,
headless random playback, action-space selection, README examples, and focused
CLI tests.

## Verification

- `gym-super-mario-bros`: `.venv/bin/python -m unittest discover .`
  (`60 tests`) and `.venv/bin/python -m gym_super_mario_bros._app.cli --mode random --steps 5 --no-render --seed 123`.
- `gym-tetris`: `.venv/bin/python -m unittest discover .` (`25 tests`) and
  `.venv/bin/python -m gym_tetris._app.cli --mode random --steps 5 --no-render --seed 123`.
- `gym-zelda-1`: `.venv/bin/python -m unittest discover .` (`11 tests`) and
  `.venv/bin/python -m gym_zelda_1._app.cli --mode random --steps 5 --no-render --seed 123 --actionspace movement`.

## Commits

- `gym-super-mario-bros`: `c9cfc0eb1471665eb3154b0f461ba5a3d08cdc2e`
  (`Add Mario CLI playback parity`), pushed to `origin/ralph-dev`.
- `gym-tetris`: `4cbbea5ef471fe284d148ea73e954c1ee9f20eef`
  (`Align CLI playback options`), pushed to `origin/ralph-dev`.
- `gym-zelda-1`: `67cea4e4ca954374f464b2dce413a43788ed5246`
  (`Add CLI playback parity options`), pushed to `origin/ralph-dev`.

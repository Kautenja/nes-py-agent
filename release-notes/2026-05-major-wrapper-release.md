# May 2026 NES Gym Release Notes

Draft notes for the next coordinated NES Gym release:

- `nes-py` `9.0.0`
- `gym-super-mario-bros` `8.0.0`
- `gym-tetris` `4.0.0`
- `gym-zelda-1` `0.3.0`

## Summary

This release refreshes the maintained NES Gym stack for the current Python and
reinforcement-learning ecosystem. The largest user-facing change is the move
from the legacy Gym API to Gymnasium across the emulator package and all three
game wrappers.

The release also standardizes packaging and maintenance with `pyproject.toml`,
GitHub Actions, tag-gated publishing, and consistent wrapper documentation.

## Breaking Changes

- Environments now follow the Gymnasium `reset()` and `step()` signatures.
- Supported Python versions now start at `3.13`.
- Runtime dependencies now expect `gymnasium>=1.0.0`.
- Wrapper releases now depend on `nes-py>=9.0.0`.

## Package Highlights

### `nes-py` `9.0.0`

- Migrates the core environment API to Gymnasium.
- Modernizes native packaging and the Cython binding layer.
- Adds cartridge metadata, stronger mapper lifecycle support, explicit state
  snapshots, batch RAM reads, and vectorized emulator instrumentation.
- Improves native mapper coverage and performance-sensitive emulator paths
  while keeping ROM asset handling conservative.

### `gym-super-mario-bros` `8.0.0`

- Migrates all documented environment flows to Gymnasium.
- Keeps the random-stage environment family and related CLI flows in the
  maintained release line.
- Refreshes packaging, CI, publishing, and bootstrap guidance for modern
  Python workflows.

### `gym-tetris` `4.0.0`

- Migrates the Tetris environments and CLI to Gymnasium.
- Preserves the A-type and B-type environment split introduced in the 3.x
  series.
- Carries forward deterministic reset and seed handling from the latest 3.x
  fixes.

### `gym-zelda-1` `0.3.0`

- Migrates the Zelda wrapper to Gymnasium while keeping the existing
  experimental API surface.
- Aligns Python, dependency, packaging, and publishing behavior with the other
  maintained wrappers.
- Sets up the project for a cleaner `1.0.0` stabilization pass after the
  Gymnasium migration.

## Maintainer Notes

- Publish `nes-py` `9.0.0` before publishing the wrapper releases.
- Create Git tags and GitHub releases after final smoke checks so changelog
  sections can be dated consistently.
- Consider calling out `gym-zelda-1` as a compatibility refresh rather than a
  stable-major launch because it remains on a `0.x` version line.

## Release Context

- Use the root `CHANGELOG.md` for the consolidated development summary.
- Use `history.md` for the chronological one-line completion record.
- Use `completion_log/` only when verification commands or pushed commit
  references are needed.

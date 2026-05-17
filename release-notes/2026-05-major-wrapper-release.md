# Upcoming Wrapper Release Notes

Draft notes for the next coordinated wrapper release:

- `gym-super-mario-bros` `8.0.0`
- `gym-tetris` `4.0.0`
- `gym-zelda-1` `0.3.0`

These releases align the game wrappers with `nes-py` `9.0.0` and the
Gymnasium API.

## Summary

This release refreshes the maintained NES Gym wrappers for the current Python
and reinforcement-learning ecosystem. The largest user-facing change is the
move from the legacy Gym API to Gymnasium across all three projects.

The release also standardizes packaging and maintenance by moving each wrapper
to `pyproject.toml`, GitHub Actions, trusted PyPI publishing, and the shared
`main.sh` workflow.

## Breaking Changes

- Environments now follow the Gymnasium `reset()` and `step()` signatures.
- Supported Python versions now start at `3.13`.
- Runtime dependencies now expect `gymnasium>=1.0.0`.
- Wrapper releases now depend on `nes-py>=9.0.0`.

## Package Highlights

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
- Create Git tags and GitHub releases after final smoke checks so the changelog
  "unreleased" sections can be dated consistently.
- Consider calling out `gym-zelda-1` as a compatibility refresh rather than a
  stable-major launch because it remains on a `0.x` version line.

## Historical Sources

- `gym-super-mario-bros`: local git tags plus GitHub Releases for the 7.x line.
- `gym-tetris`: local git tags plus GitHub Releases for the 2.x and 3.x line.
- `gym-zelda-1`: local git tags and repository history; the GitHub Releases
  page currently has no published releases.

# Specification: Wrapper Documentation and Metadata Parity

## Problem

The wrappers have already moved to Gymnasium and modern `pyproject.toml`
metadata, but their docs and metadata still contain small inconsistencies with
the current `nes-py` baseline:

- wrapper READMEs do not state the supported CI Python targets the way
  `nes-py` does.
- wrapper README command examples are not fully aligned with the wrapper CLIs.
- some code comments and docstrings still mention legacy "Gym" wording where
  they describe current Gymnasium behavior.
- `gym-tetris/gym_tetris/tetris_env.py` still comments that its ROM path is
  the "Zelda 1 ROM".
- wrapper `pyproject.toml` files use different indentation and metadata idioms
  from each other and from `nes-py`, including URL and license-file treatment.
- package metadata should preserve the wrappers' educational/proprietary ROM
  sensitivity while still using current packaging fields where possible.

These are not urgent runtime bugs, but they are the kind of drift that makes
the smaller wrappers look less maintained than `nes-py` and the Mario flagship.

## Scope

- Work inside `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1`.
- Update docs, comments, and packaging metadata only.
- Do not change runtime environment behavior, reward behavior, action spaces,
  ROM modes, info keys, or registered IDs.
- Do not change license meaning without explicit maintainer approval.
- Do not add, remove, or modify ROM assets.

## Acceptance Criteria

- [ ] Each wrapper README states the supported Python versions tested in CI.
- [ ] README installation, Python usage, and CLI examples match the actual
      Gymnasium API and implemented command-line options.
- [ ] README examples consistently use `reset(seed=...)` where determinism is
      being demonstrated and avoid `env.seed(...)`.
- [ ] README development or publishing sections are consistent with the current
      trusted-publishing workflow.
- [ ] Stale comments and docstrings that describe current behavior as legacy
      Gym behavior are updated to Gymnasium wording.
- [ ] Obvious copied-game comments, including the Tetris "Zelda 1 ROM" comment,
      are corrected.
- [ ] `pyproject.toml` metadata is formatted consistently across wrappers while
      preserving each package's name, version, description, classifiers, URLs,
      dependencies, console scripts, and package-data configuration.
- [ ] License metadata continues to reflect the actual wrapper license files
      and educational-use restrictions; no license text is broadened without
      explicit approval.
- [ ] No generated artifacts, caches, build outputs, or local virtual
      environments are committed.

## Verification

Run metadata and distribution checks:

```sh
cd gym-super-mario-bros
python -m build
```

```sh
cd gym-tetris
python -m build
```

```sh
cd gym-zelda-1
python -m build
```

Run the wrapper test suites if any packaging metadata changes may affect
runtime imports:

```sh
cd gym-super-mario-bros
python -m unittest discover .
```

```sh
cd gym-tetris
python -m unittest discover .
```

```sh
cd gym-zelda-1
python -m unittest discover .
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push each changed wrapper submodule.
- Commit and push the umbrella repository's updated submodule pointers.
- Append the required one-line summary to `history.md`.
- Add a completion log for this spec.
- Output `DONE` only after local verification passes and required remote checks
  are green.

<!-- NR_OF_TRIES: 0 -->

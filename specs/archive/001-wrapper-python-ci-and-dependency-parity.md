# Specification: Wrapper Python, CI, and Dependency Parity

## Status: COMPLETE

## Problem

`nes-py` now advertises and tests Python 3.13 and 3.14 across Linux, Windows,
and macOS. The three wrapper repositories depend on `nes-py>=9.0.0`, but their
support and CI surfaces do not fully match that baseline:

- `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1` CI only set up
  Python 3.13.
- `gym-tetris` declares `requires-python = ">=3.13,<3.14"`, which prevents
  installation on a Python version supported by `nes-py`.
- wrapper package classifiers only list Python 3.13.
- wrapper CI artifact names are platform-only, while `nes-py` includes the
  Python version in build artifact names.
- wrapper `requirements.txt` files use different development dependency
  policies: Mario and Zelda track `nes-py` `ralph-dev`, while Tetris pins a
  specific `nes-py` commit SHA.

This creates unnecessary friction for coordinated releases because the pure
Python wrappers can appear incompatible with a supported `nes-py` runtime even
when their code may already work.

## Scope

- Work inside `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1`.
- Keep native build and wheel policy in `nes-py`; wrappers remain pure Python
  packages.
- Do not add, remove, or modify ROM assets.
- Do not backport Mario-only gameplay features to Tetris or Zelda as part of
  this spec.
- If submodule commits are made, commit and push each child repository before
  updating the umbrella gitlink.

## Acceptance Criteria

- [x] Each wrapper's `pyproject.toml` has a Python support range that is
      intentionally aligned with the current `nes-py` release, unless a tested
      wrapper-specific incompatibility is documented in the spec completion
      notes.
- [x] Each wrapper lists Python 3.13 and 3.14 classifiers if both versions are
      supported.
- [x] Each wrapper CI matrix tests Python 3.13 and 3.14 on the same operating
      system runners currently used by the wrapper.
- [x] Wrapper CI artifact names include both platform and Python version, or
      otherwise avoid collisions when multiple Python versions upload
      distributions.
- [x] The wrapper development bootstrap dependency on sibling or remote
      `nes-py` uses one documented policy across all three repositories.
- [x] `requirements.txt` comments consistently state that canonical runtime
      metadata lives in `pyproject.toml`.
- [x] CI still installs the package in a way that exercises the declared
      package metadata and the selected `nes-py` dependency.
- [x] No generated artifacts, caches, build outputs, or local virtual
      environments are committed.

## Verification

Run focused local checks before pushing:

```sh
cd gym-super-mario-bros
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover .
python -m build
```

```sh
cd gym-tetris
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover .
python -m build
```

```sh
cd gym-zelda-1
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover .
python -m build
```

After pushing, verify that GitHub Actions runs the expanded Python matrix for
each changed wrapper.

## Completion Notes

All three wrappers are intentionally aligned with the current `nes-py` Python
support range. No wrapper-specific Python 3.14 incompatibility was found. The
shared development bootstrap policy is to install `nes-py` from the `ralph-dev`
branch in `requirements.txt`, while canonical runtime metadata remains in each
wrapper's `pyproject.toml`.

## Completion Signal

When all acceptance criteria are met:

- Commit and push each changed wrapper submodule.
- Commit and push the umbrella repository's updated submodule pointers.
- Append the required one-line summary to `history.md`.
- Add a completion log for this spec.
- Output `DONE` only after local verification passes and required remote checks
  are green.

<!-- NR_OF_TRIES: 1 -->

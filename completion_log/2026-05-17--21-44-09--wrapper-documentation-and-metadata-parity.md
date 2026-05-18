# Completion Log: Wrapper Documentation and Metadata Parity

## Summary

Completed spec 005 across `gym-super-mario-bros`, `gym-tetris`, and
`gym-zelda-1` by aligning README usage and publishing docs with the current
Gymnasium and CLI behavior, documenting the supported CI Python targets, and
normalizing wrapper `pyproject.toml` metadata toward the current `nes-py`
baseline. The packaging pass also updated the wrappers to use
`LicenseRef-Proprietary` plus explicit `license-files` entries so modern
setuptools can build them while preserving the existing proprietary /
educational-use license intent in the checked-in `LICENSE` files and README
guidance.

## Verification

- `gym-super-mario-bros`: `./.venv/bin/python -m build --no-isolation`
- `gym-super-mario-bros`: `./.venv/bin/python -c "import unittest; from gymnasium import logger as gym_logger; gym_logger.min_level = 40; suite = unittest.defaultTestLoader.discover('.'); result = unittest.TextTestRunner(verbosity=1).run(suite); raise SystemExit(0 if result.wasSuccessful() else 1)"` (`67 tests`, `OK`)
- `gym-tetris`: `./.venv/bin/python -m build --no-isolation`
- `gym-tetris`: `./.venv/bin/python -m unittest discover .` (`30 tests`, `OK`)
- `gym-zelda-1`: `./.venv/bin/python -m build --no-isolation`
- `gym-zelda-1`: `./.venv/bin/python -m unittest discover .` (`17 tests`, `OK`)
- Removed generated `dist/` and `*.egg-info/` artifacts after verification.

## Notes

- The default isolated `python -m build` path tried to create temporary build
  environments and download backend wheels from PyPI, which is blocked in this
  sandbox. Installing local `setuptools` / `wheel` into each wrapper venv and
  using `--no-isolation` verified the wrapper metadata and produced both sdist
  and wheel artifacts without leaving generated outputs in the repos.
- Modern setuptools rejected the legacy `License :: Free For Educational Use`
  trove classifier once a license expression was present, so the wrappers now
  preserve license intent through `LicenseRef-Proprietary`, the checked-in
  `LICENSE` file, and README wording instead of the deprecated classifier.

## Commits

- No commits created in this interactive session.

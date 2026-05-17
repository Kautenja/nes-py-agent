# gym-zelda-1 GitHub Actions CI

Completed the Travis-to-GitHub-Actions migration for `gym-zelda-1`.

## Summary

- Removed `.travis.yml`.
- Added `.github/workflows/ci.yml` with Python 3.13 build/test coverage on Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- Added tag-gated release artifact attachment through `gh release`.
- Updated README CI badge links, Python/package metadata, packaging requirements, and stale CI-adjacent Zelda references.
- Added `pyproject.toml` for modern `python -m build` packaging.
- Disabled Gym's passive env checker for the registered Zelda env to avoid Gym 0.25's NumPy 2.x `np.bool8` checker failure while preserving the existing old Gym step API.

## Verification

- `python3.13 -m venv .venv`
- `.venv/bin/python -m pip install --upgrade pip`
- `.venv/bin/python -m pip install -r requirements.txt`
- `.venv/bin/python -m pip install .`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m build`
- workflow trigger/matrix validation script
- `gh run watch --repo Kautenja/gym-zelda-1 25983720695 --exit-status --interval 30`

Local build emitted setuptools' existing license-classifier deprecation warning; it did not fail the build.

Tag release behavior was verified by workflow configuration only to avoid publishing a throwaway release.

## Commits

- `gym-zelda-1`: `cb0e9eea2e0d365f7cbeed78f2b6c4cccbbf28d3`

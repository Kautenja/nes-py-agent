# nes-py GitHub Actions CI Migration

## Summary

- Replaced Travis/SCons CI with `.github/workflows/ci.yml` in `nes-py`.
- Moved native extension builds to the Python packaging path with `pyproject.toml`, `setuptools.Extension`, and platform-specific compiler flags.
- Updated README badge/docs, package Python classifiers, build requirements, make targets, manifest exclusions, and release tooling.
- Fixed NumPy 2.x ROM header arithmetic needed by the Python 3.13 dependency set.

## Verification

- Local environment used `.venv/bin/python` because the host has `python3` but no global `python`.
- Ran `.venv/bin/python -m pip install --upgrade pip`.
- Ran `.venv/bin/python -m pip install -r requirements.txt`.
- Ran `.venv/bin/python -m pip install .`.
- Ran `.venv/bin/python -m unittest discover .`: 143 tests passed.
- Ran `.venv/bin/python -m build`: sdist and wheel built successfully.
- Ran workflow trigger parsing check with PyYAML.
- Checked sdist and wheel contents for `.DS_Store`, bytecode, caches, and object files.
- Ran `git diff --check`.
- Verified GitHub-hosted runner labels against the official GitHub Actions hosted runner reference. The configured labels are `ubuntu-24.04`, `ubuntu-24.04-arm`, `windows-2022`, `macos-15-intel`, and `macos-15`.
- Opened PR `Kautenja/nes-py#104` to trigger the required pull request workflow without enabling arbitrary branch push builds.
- GitHub Actions run `25982331860` passed for Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- Tag release upload was not live-tested to avoid publishing a throwaway release; the release job is gated with `if: startsWith(github.ref, 'refs/tags/')` and was skipped on the pull request run as expected.

## Commits Pushed

- `Kautenja/nes-py@812653b` - `Migrate CI to GitHub Actions`
- `Kautenja/nes-py@62c1b20` - `Use current GitHub Actions versions`

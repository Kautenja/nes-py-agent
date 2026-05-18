# gym-super-mario-bros GitHub Actions CI Migration

## Summary

Migrated `gym-super-mario-bros` from Travis CI to GitHub Actions. The wrapper now has a Python 3.13 build/test workflow covering Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64, with per-platform distribution artifacts and a tag-gated release attachment job.

Removed Travis README badges and stale Travis-era dependencies, added `pyproject.toml`, moved builds to `python -m build`, and updated package metadata to stop advertising unsupported Python versions. The Python 3.13 path also required keeping Gym on the old-API 0.25 line, disabling Gym's NumPy-2-incompatible passive env checker for registered legacy environments, converting RAM bytes to Python integers before arithmetic, and installing a fixed pushed `nes-py` commit in CI requirements so the wrapper is not dependent on the umbrella checkout.

## Verification

- Local Python 3.13.11 virtualenv:
  - `python -m pip install --upgrade pip`
  - `python -m pip install -r requirements.txt`
  - `python -m pip install .`
  - `python -m unittest discover .`
  - `python -m build`
- Workflow inspection verified pull request, `master`, and tag triggers; no arbitrary branch push trigger; five required runner labels; package install/test/build steps; and tag-only release gating.
- GitHub Actions PR run `25983401964` for `Kautenja/gym-super-mario-bros#138` passed all five matrix jobs:
  - Linux x64
  - Linux arm64
  - Windows x64
  - macOS x64
  - macOS arm64
- Live tag smoke test was skipped to avoid creating a throwaway release; release upload is gated by `startsWith(github.ref, 'refs/tags/')`.

## Commits

- `gym-super-mario-bros`: `b7762013dc2734d19899fd1d4c18ae3f7dd1631b` pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the updated `gym-super-mario-bros` gitlink and archive summary.

# gym-tetris GitHub Actions CI

Completed the Travis-to-GitHub-Actions migration for `gym-tetris`.

## Summary

- Removed `.travis.yml`.
- Added `.github/workflows/ci.yml` with Python 3.13 build/test coverage on Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- Added tag-gated release artifact attachment through `gh release`.
- Updated README CI badge links, Python/package metadata, packaging requirements, and the makefile build path.
- Fixed Python 3.13 dependency compatibility in tests and BCD decoding under NumPy 2.x.
- Verified runner labels against GitHub's hosted runner reference: https://docs.github.com/en/actions/reference/github-hosted-runners-reference

## Verification

- `python3.13 -m venv .venv`
- `.venv/bin/python -m pip install --upgrade pip`
- `.venv/bin/python -m pip install -r requirements.txt`
- `.venv/bin/python -m pip install .`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m build`
- workflow trigger/matrix validation script
- `gh run watch --repo Kautenja/gym-tetris 25983924981 --exit-status --interval 30`

Local build emitted setuptools' existing license-classifier deprecation warning; it did not fail the build.

Tag release behavior was verified by workflow configuration only to avoid publishing a throwaway release.

## Commits

- `gym-tetris`: `c17c60d4a6850ee0ba462e026cebc262d03c3ba7`
- Draft PR opened to trigger pull-request CI: https://github.com/Kautenja/gym-tetris/pull/26

# Specification: gym-zelda-1 GitHub Actions CI Migration

## Status: COMPLETE

## Problem

`gym-zelda-1` still uses Travis CI and an obsolete Python/runtime matrix. The project needs to follow the same GitHub Actions CI rules and release-artifact pattern now used by `nes-py`, while keeping the wrapper package independently buildable and testable.

## Reference Implementation

Use `nes-py/.github/workflows/ci.yml` as the behavioral reference for:

- workflow name, trigger policy, and permissions;
- Python 3.13 setup;
- Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64 runner coverage;
- build/test job plus tag-only release artifact attachment job;
- artifact upload naming and tag-release gating style.

Adjust only where the wrapper package needs a simpler pure-Python build path or package-specific artifact names.

## Scope

- Work inside the `gym-zelda-1` submodule unless an umbrella gitlink update is required after committing the submodule.
- Remove Travis CI configuration and Travis README references completely.
- Add a GitHub Actions workflow under `gym-zelda-1/.github/workflows/`.
- Keep CI triggers aligned with `nes-py`: pull requests, pushes to `master`, and tags only.
- Build and test using Python packaging commands rather than relying on Travis-era `make` behavior as the primary CI interface.
- Keep the package install/test/release flow independent of sibling checkouts in the umbrella repository.
- Do not add ROM assets, redistribute new external game assets, or change environment behavior.

## Platform Matrix

Use the same required platform coverage as the `nes-py` workflow unless GitHub-hosted runner labels have changed at implementation time:

| Target | Architecture | Candidate runner label |
| --- | --- | --- |
| Linux Intel | x64 | `ubuntu-24.04` |
| Linux ARM | arm64 | `ubuntu-24.04-arm` |
| Windows Intel | x64 | `windows-2022` |
| macOS Intel | x64 | `macos-15-intel` |
| macOS Apple Silicon | arm64 | `macos-15` |

If any label has changed, use the current stable label and document the reason in the completion log.

## Python Version

Use Python 3.13 for the required GitHub Actions matrix, matching `nes-py`. Do not restore the old Travis-era Python 3.5-3.9 matrix.

## Acceptance Criteria

- [x] `gym-zelda-1/.travis.yml` is deleted.
- [x] `gym-zelda-1/README.md` no longer links to Travis CI and its build badge points to the GitHub Actions workflow.
- [x] A GitHub Actions workflow exists under `gym-zelda-1/.github/workflows/`.
- [x] The workflow runs automatically for pull request commits.
- [x] The workflow runs automatically for commits pushed to `master`.
- [x] The workflow runs automatically for tags.
- [x] The workflow does not run automatically for arbitrary branch pushes outside `master` and tags.
- [x] The required workflow matrix uses Python 3.13 on Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- [x] The workflow installs package dependencies and then installs `gym-zelda-1` through the Python packaging path.
- [x] The workflow runs `python -m unittest discover .` after installation.
- [x] The workflow builds distributions with `python -m build` or an equivalently modern Python packaging command.
- [x] Build artifacts from each platform are uploaded as workflow artifacts with package-specific names.
- [x] Tag builds attach completed distribution artifacts to the corresponding GitHub Release or create the release if needed.
- [x] Release artifact upload steps are gated so they do not run for pull requests or non-tag pushes.
- [x] Any compiler or native dependency setup copied from `nes-py` is platform-specific and justified by the `nes-py` dependency install path; unnecessary native setup is omitted rather than kept as cargo-cult CI.
- [x] `requirements.txt`, `setup.py`, `pyproject.toml`, `makefile`, or related packaging files are updated as needed so normal install/test/build paths match the GitHub Actions workflow.
- [x] Package metadata no longer advertises unsupported Travis-era Python versions unless those versions remain tested elsewhere.
- [x] Stale CI or release dependencies that are no longer needed for normal installs are removed or moved to an appropriate tooling path.
- [x] Existing incorrect or stale package metadata discovered while touching CI-adjacent files is corrected when it is directly relevant to badges, repository URLs, descriptions, or tested Python support.
- [x] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [x] The `gym-zelda-1` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd gym-zelda-1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install .
python -m unittest discover .
python -m build
```

Inspect the workflow trigger configuration and release gating:

```sh
cd gym-zelda-1
python - <<'PY'
from pathlib import Path
import yaml

workflow = next(Path(".github/workflows").glob("*.yml"))
data = yaml.safe_load(workflow.read_text())
triggers = data.get("on", {})
assert "pull_request" in triggers
push = triggers.get("push", {})
assert push.get("branches") == ["master"]
assert push.get("tags")
PY
```

After pushing the `gym-zelda-1` branch, verify GitHub Actions directly:

```sh
gh run list --repo Kautenja/gym-zelda-1 --branch master --limit 5
gh run watch --repo Kautenja/gym-zelda-1 <run-id> --exit-status --interval 30
```

For tag release behavior, the workflow configuration must clearly gate artifact attachment to tag refs. If a live tag smoke test is skipped to avoid publishing a throwaway release, document that decision in the completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-zelda-1` submodule changes.
- Commit and push the umbrella repository's updated `gym-zelda-1` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--gym-zelda-1-github-actions-ci.md` file.
- Output `DONE` only after the pushed GitHub Actions run passes for the full required matrix.

## Completion Log

- Child commit: `cb0e9eea2e0d365f7cbeed78f2b6c4cccbbf28d3`
- GitHub Actions run: `25983720695`
- Verification: local Python 3.13 install/test/build checks passed; workflow trigger/matrix validation passed; pushed CI passed on Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- Tag release behavior was verified by workflow configuration only to avoid publishing a throwaway release.

<!-- NR_OF_TRIES: 1 -->

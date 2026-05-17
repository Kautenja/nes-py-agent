# Specification: nes-py GitHub Actions CI Migration

## Status: COMPLETE

## Problem

`nes-py` still uses Travis CI and Unix-oriented build steps that do not represent the supported platform set. The project needs to replace Travis with GitHub Actions, build and test the native extension on macOS Apple Silicon, macOS Intel, Windows Intel, Linux ARM, and Linux Intel, and clean up stale build tooling so future releases are driven by the supported Python packaging path.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Remove Travis CI configuration and references completely.
- Add GitHub Actions workflow coverage for the requested operating system and CPU architecture matrix.
- Trigger CI automatically for pull request commits, commits pushed to `master`, and tags only.
- Attach built distribution artifacts to tag releases after tag builds complete.
- Replace or remove legacy SCons-driven build steps if a simpler Python packaging build path can build the native C++ extension reliably.
- Clean up build tooling as needed to make the GitHub Actions builds reliable and idiomatic for Python packaging.
- Do not add ROM assets or change emulator behavior.

## Platform Matrix

Use current GitHub-hosted runner labels from the official GitHub Actions runner documentation at implementation time. As of 2026-05-17, suitable labels include:

| Target | Architecture | Candidate runner label |
| --- | --- | --- |
| Linux Intel | x64 | `ubuntu-24.04` |
| Linux ARM | arm64 | `ubuntu-24.04-arm` |
| Windows Intel | x64 | `windows-2022` or `windows-2025` |
| macOS Intel | x64 | `macos-15-intel` |
| macOS Apple Silicon | arm64 | `macos-15` or `macos-14` |

If any label has changed, use the current stable label and document the reason in the completion log.

## Python Version

Use Python 3.13 for the required GitHub Actions matrix. Python 3.13 is currently in upstream bugfix support, is new enough to replace the obsolete Travis-era Python 3.5-3.9 matrix, and is less likely than a brand-new interpreter line to expose avoidable dependency churn in `gym`, `pyglet`, or native-extension packaging. Do not target prerelease Python versions. Python 3.14 may be added only as an extra non-blocking compatibility job after dependency and wheel compatibility are proven.

## Workflow Triggers

The GitHub Actions workflow must avoid building arbitrary branch commits. It should run automatically for:

- `pull_request` events so every pull request commit is built and tested.
- `push` events to `master`.
- `push` events for tags.

Do not configure a broad `push` trigger that runs for every branch. The active development branch can still be tested by opening a pull request.

## Tag Artifacts

Tag builds should produce Python distribution artifacts and attach them to the corresponding GitHub tag release after the matrix builds complete. The release upload should only run for tag refs and should not publish release artifacts for pull requests or ordinary branch pushes.

## Acceptance Criteria

- [ ] `nes-py/.travis.yml` is deleted.
- [ ] `nes-py/README.md` no longer links to Travis CI and its build badge points to the GitHub Actions workflow.
- [ ] A GitHub Actions workflow exists under `nes-py/.github/workflows/` and runs automatically for pull request commits.
- [ ] The workflow runs automatically for commits pushed to `master`.
- [ ] The workflow runs automatically for tags.
- [ ] The workflow does not run automatically for arbitrary branch pushes outside `master` and tags.
- [ ] The required workflow matrix uses Python 3.13 on every supported operating system and architecture.
- [ ] The workflow builds and installs `nes-py` through the Python packaging path rather than manually moving a Unix-only `.so` from the SCons build directory.
- [ ] The workflow runs the Python test suite after the compiled extension is available.
- [ ] Build artifacts from each platform are uploaded as workflow artifacts.
- [ ] Tag builds attach the completed distribution artifacts to the corresponding GitHub Release or create the release if needed.
- [ ] Release artifact upload steps are gated so they do not run for pull requests or non-tag pushes.
- [ ] The workflow covers Linux x64, Linux arm64, Windows x64, macOS x64, and macOS arm64.
- [ ] Platform-specific compiler setup is handled explicitly and does not force `g++` on Windows or other incompatible runners.
- [ ] SCons is removed from the required build path unless the implementer documents a concrete reason it remains necessary.
- [ ] If SCons is no longer needed, `nes-py/nes_py/nes/SConstruct`, `makefile` targets, CI setup, and documentation are updated so no normal build/test/release path depends on it.
- [ ] The native extension build is driven by Python packaging tools such as `setuptools.Extension` with a `pyproject.toml` build-system declaration, or an equally simple Python-native approach.
- [ ] Any remaining local build targets in `makefile`, `setup.py`, `pyproject.toml`, `requirements.txt`, or new packaging config are consistent with the GitHub Actions build path.
- [ ] Python package metadata no longer advertises unsupported Travis-era versions unless those versions remain tested elsewhere; supported classifiers and docs reflect the new tested Python target.
- [ ] Stale CI or release dependencies that are no longer needed for normal installs are removed or moved to an appropriate extra/tooling path.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd nes-py
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install .
python -m unittest discover .
python -m build
```

After pushing the `nes-py` branch, verify GitHub Actions directly:

```sh
gh run list --repo Kautenja/nes-py --branch ralph-dev --limit 5
gh run watch --repo Kautenja/nes-py <run-id> --exit-status --interval 30
```

Also inspect the workflow trigger configuration and release path:

```sh
cd nes-py
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

The implementation is not complete until every required matrix job succeeds or any intentionally skipped job is justified by a documented GitHub-hosted runner limitation. For tag release behavior, the workflow configuration must clearly gate artifact attachment to tag refs; if a live tag smoke test is skipped to avoid publishing a throwaway release, document that decision in the completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-github-actions-ci.md` file.
- Output `DONE` only after the pushed GitHub Actions run passes for the full required matrix.

<!-- NR_OF_TRIES: 1 -->

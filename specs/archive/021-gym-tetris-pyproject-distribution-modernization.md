# Specification: gym-tetris pyproject Distribution Modernization

## Status: COMPLETE

## Problem

`gym-tetris` still keeps its canonical distribution metadata in `setup.py` and does not yet have a `pyproject.toml` build declaration. The wrapper should match the modernized `nes-py` packaging direction by making `pyproject.toml` the single distribution source of truth and removing the legacy `setup.py` installer path.

## Scope

- Work inside the `gym-tetris` submodule unless an umbrella gitlink update is required.
- Create a `pyproject.toml` with the build backend and all static package metadata, dependencies, package discovery, package data, release extras, URLs, and console scripts from `setup.py`.
- Preserve the existing distribution identity and import package: distribution `gym_tetris`, Python package `gym_tetris`.
- Preserve bundled ROM package data under `gym_tetris/_roms/*.nes` without adding, removing, or redistributing any new ROM assets.
- Keep the project buildable with `setuptools.build_meta` through `pyproject.toml`.
- Update developer and release documentation only where commands or packaging expectations change.

## Non-Goals

- Do not change environment registration, rewards, action spaces, or emulator behavior.
- Do not migrate the wrapper from Gym to Gymnasium in this spec.
- Do not change the package version, dependency ranges, license text, or ROM inventory unless required to preserve the existing package metadata exactly.
- Do not introduce native extension build machinery; this wrapper should remain a pure Python package around its existing assets.

## Acceptance Criteria

- [x] `pyproject.toml` exists and contains the canonical project metadata: name, version, description, README, Python requirement, classifiers, keywords, license metadata, authors, dependencies, optional release dependencies, URLs, package discovery, package data, and scripts.
- [x] `setup.py` is removed, and no published distribution metadata, install requirements, package data declarations, or entry points remain in `setup.py` or `setup.cfg`.
- [x] Any retained `requirements.txt` file is clearly only for CI/developer bootstrap needs, not the canonical source for package metadata.
- [x] The build backend is `setuptools.build_meta`, with explicit setuptools configuration for package discovery and `gym_tetris/_roms/*.nes` package data.
- [x] The console script `gym_tetris = gym_tetris._app.cli:main` is installed and still exposes help successfully.
- [x] Editable installs, standard installs, wheel builds, and sdist builds work from a clean checkout.
- [x] Built wheels and sdists include the Python package, bundled ROM files, README-derived long description, metadata, and console script entry point.
- [x] Runtime dependencies remain equivalent to the current `setup.py`: `gym>=0.25.2,<0.26` and `nes-py>=8.2.1`.
- [x] Release extra dependencies remain equivalent to the current `setup.py`: `twine>=6.1.0`.
- [x] README, CI, and release notes are updated if they still instruct maintainers to use `setup.py` directly.
- [x] No generated build artifacts, wheels, caches, or local virtual environments are committed.
- [x] The `gym-tetris` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd gym-tetris
python -m pip install --upgrade pip build
python -m pip install -e .
gym_tetris --help
python -m build
python -m pip install dist/*.whl --force-reinstall
python -c "import importlib.metadata as metadata; import gym_tetris; print(metadata.metadata('gym_tetris')['Name']); print(metadata.version('gym_tetris'))"
python -m zipfile -l dist/*.whl
python -m tarfile -l dist/*.tar.gz
```

Inspect the wheel and sdist listings to confirm `gym_tetris/_roms/*.nes` and package metadata are present.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-tetris` submodule changes.
- Commit and push the umbrella repository's updated `gym-tetris` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--gym-tetris-pyproject-distribution-modernization.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

## Completion Log

Completed in `gym-tetris` commit `a993605` with a new `pyproject.toml`
containing PEP 621 metadata, setuptools package discovery and ROM package
data, release extras, project URLs, and console script metadata. Removed
`setup.py` and clarified that `requirements.txt` is only for developer/CI
bootstrap.

Verification used `.venv/bin/python`:

- `./main.sh install`
- `.venv/bin/gym_tetris --help`
- `./main.sh build`
- `.venv/bin/python -m pip install dist/gym_tetris-3.0.4-py3-none-any.whl --force-reinstall`
- `.venv/bin/python -m pip install . --force-reinstall`
- `.venv/bin/python -c "import importlib.metadata as metadata; import gym_tetris; print(metadata.metadata('gym_tetris')['Name']); print(metadata.version('gym_tetris'))"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `git diff --check`

<!-- NR_OF_TRIES: 1 -->

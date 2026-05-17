# Specification: nes-py pyproject Build Modernization

## Status: COMPLETE

## Problem

`nes-py` already has a minimal `pyproject.toml`, but package metadata, dependencies, extension discovery, compiler flags, entry points, and release extras still live in `setup.py`. The project should move toward the standard `pyproject.toml` configuration path while preserving native extension builds across Linux, macOS, and Windows.

This is also a prerequisite for a cleaner Cython binding migration: the build system should have one obvious source of truth before the binding layer changes.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Move static package metadata and dependency declarations from `setup.py` into `pyproject.toml`.
- Keep any unavoidable dynamic extension-build glue as small and well documented as possible.
- Preserve existing install, editable install, test, build, and release workflows.
- Keep CI and local build behavior aligned.

## Non-Goals

- Do not migrate the ctypes binding to Cython in this spec.
- Do not change emulator behavior.
- Do not remove compiler/platform support that currently works unless it is explicitly unsupported and documented.

## Acceptance Criteria

- [x] `pyproject.toml` contains the canonical project metadata: name, version, description, README, Python requirement, classifiers, keywords, license, authors, dependencies, optional release dependencies, scripts, package discovery, and build backend configuration.
- [x] `setup.py` is removed or reduced to the smallest compatibility/build helper needed for native extensions.
- [x] Native extension source discovery is deterministic and includes C++ mapper sources and headers in sdists.
- [x] Compiler flags remain platform-aware and preserve the current C++ standard and optimization intent.
- [x] `python -m pip install .`, `python -m pip install -e .`, and `python -m build` work from a clean checkout.
- [x] Built wheels and sdists include the required C++ sources, headers, Python files, and package metadata.
- [x] The console script entry point `nes_py = nes_py.app.cli:main` still works.
- [x] The packaged benchmark module from spec 006 remains runnable after installation.
- [x] CI configuration, README developer notes, and packaging docs are updated if command names or requirements change.
- [x] No generated build artifacts, wheels, caches, or local virtual environments are committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install --upgrade pip build
python -m pip install -e .
python -m unittest discover .
python -m build
python -m pip install dist/*.whl --force-reinstall
python -m unittest nes_py.tests.test_nes_env
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --json --no-progress
```

Run the strongest feasible platform checks locally and rely on CI for the full platform matrix.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-pyproject-build-modernization.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

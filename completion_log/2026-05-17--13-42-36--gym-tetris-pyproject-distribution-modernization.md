# gym-tetris pyproject Distribution Modernization

## Summary

Completed work item 021 in `gym-tetris`.

- Created `pyproject.toml` with distribution metadata, runtime dependencies,
  release extra, URLs, package discovery, ROM package data, and console script
  metadata.
- Removed legacy `setup.py`.
- Clarified that `requirements.txt` is only for developer/CI bootstrap.

## Verification

Commands were run inside `gym-tetris` with `.venv/bin/python`.

- `./main.sh install`
- `.venv/bin/gym_tetris --help`
- `./main.sh build`
- `.venv/bin/python -m pip install dist/gym_tetris-3.0.4-py3-none-any.whl --force-reinstall`
- `.venv/bin/python -m pip install . --force-reinstall`
- `.venv/bin/python -c "import importlib.metadata as metadata; import gym_tetris; print(metadata.metadata('gym_tetris')['Name']); print(metadata.version('gym_tetris'))"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `git diff --check`

The wheel and sdist listings include the Python package, dist metadata,
entry point metadata, README-derived package metadata, and the existing
`gym_tetris/_roms/*.nes` assets.

## Commits

- `gym-tetris`: `a993605` (`Modernize pyproject packaging`), pushed to
  `origin/ralph-dev`.

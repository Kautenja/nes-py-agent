# gym-zelda-1 pyproject Distribution Modernization

## Summary

Completed spec 020 in `gym-zelda-1`.

- Moved distribution metadata, runtime dependencies, release extra, URLs,
  package discovery, ROM package data, and console script metadata into
  `pyproject.toml`.
- Removed legacy `setup.py`.
- Clarified that `requirements.txt` is only for developer/CI bootstrap.

## Verification

Commands were run inside `gym-zelda-1` with `.venv/bin/python`.

- `./main.sh install`
- `.venv/bin/gym_zelda_1 --help`
- `./main.sh build`
- `.venv/bin/python -m pip install dist/gym_zelda_1-0.2.2-py3-none-any.whl --force-reinstall`
- `.venv/bin/python -m pip install . --force-reinstall`
- `.venv/bin/python -c "import importlib.metadata as metadata; import gym_zelda_1; print(metadata.metadata('gym_zelda_1')['Name']); print(metadata.version('gym_zelda_1'))"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `git diff --check`

The wheel and sdist listings include the Python package, dist metadata,
entry point metadata, README-derived package metadata, and the existing
`gym_zelda_1/_roms/*.nes` assets.

## Commits

- `gym-zelda-1`: `fc5a468` (`Modernize pyproject packaging`), pushed to
  `origin/ralph-dev`.

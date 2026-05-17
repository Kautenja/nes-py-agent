# gym-super-mario-bros pyproject Distribution Modernization

## Summary

Completed spec 019 in `gym-super-mario-bros`.

- Moved distribution metadata, runtime dependencies, release extra, URLs,
  package discovery, ROM package data, and console script metadata into
  `pyproject.toml`.
- Removed legacy `setup.py`.
- Clarified that `requirements.txt` is only for developer/CI bootstrap.

## Verification

Commands were run inside `gym-super-mario-bros` with `.venv/bin/python`.

- `./main.sh install`
- `.venv/bin/gym_super_mario_bros --help`
- `./main.sh build`
- `.venv/bin/python -m pip install dist/gym_super_mario_bros-7.4.0-py3-none-any.whl --force-reinstall`
- `.venv/bin/python -m pip install . --force-reinstall`
- `.venv/bin/python -c "import importlib.metadata as metadata; import gym_super_mario_bros; print(metadata.metadata('gym_super_mario_bros')['Name']); print(metadata.version('gym_super_mario_bros'))"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `git diff --check`

The wheel and sdist listings include the Python package, dist metadata,
entry point metadata, README-derived package metadata, and the existing
`gym_super_mario_bros/_roms/*.nes` assets.

## Commits

- `gym-super-mario-bros`: `ba2f955` (`Modernize pyproject packaging`),
  pushed to `origin/ralph-dev`.

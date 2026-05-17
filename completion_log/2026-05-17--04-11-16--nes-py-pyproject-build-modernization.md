# Completion Log: nes-py pyproject Build Modernization

## Summary

Moved static `nes-py` package metadata, runtime dependencies, release extras,
console scripts, package discovery, and package data into `pyproject.toml`.
Reduced `setup.py` to the native extension build helper, with deterministic
sorted C++ source discovery and the existing platform-aware C++14 optimization
flags.

Updated `MANIFEST.in` and wheel package data so C++ mapper sources and headers
are present in source and wheel distributions. Updated developer notes and
kept `requirements.txt` focused on development build tooling.

## Verification

Run inside `nes-py` with `.venv/bin/python` because this machine has no
`python` executable on `PATH`:

- `.venv/bin/python -m pip install --upgrade pip build`
- `.venv/bin/python -m pip install .`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m build`
- inspected `dist/nes_py-8.2.1.tar.gz` for `pyproject.toml`, `setup.py`,
  package Python files, C++ sources, mapper sources, and headers
- inspected `dist/nes_py-8.2.1-*.whl` for the native extension, package Python
  files, C++ sources, mapper sources, headers, license, metadata, and entry
  point metadata
- `.venv/bin/python -m pip install dist/*.whl --force-reinstall`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/nes_py --help`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --json --no-progress`
- `.venv/bin/python -m pip check`
- `git diff --check`

## Commits Pushed

- `nes-py`: `a290cab` (`Modernize pyproject packaging`) pushed to
  `origin/ralph-dev`.

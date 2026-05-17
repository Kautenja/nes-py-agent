# nes-py Mapper Test Package Refactor

## Summary

Completed spec 023 in `nes-py`.

- Split the former monolithic `nes_py/tests/test_mappers.py` coverage into the
  `nes_py/tests/mappers/` package.
- Added package-local shared mapper helpers in `common.py`, registry and
  lifecycle smoke modules, and one canonical mapper module each for NROM,
  SxROM/MMC1, UxROM, and CNROM.
- Removed `nes_py/tests/test_mappers.py`; no compatibility shim remains, so
  normal discovery has no duplicate mapper test path.
- Converted existing non-mapper test fixture imports to absolute package imports
  so `unittest discover nes_py/tests` works with the requested filesystem start
  directory.
- Updated the active Python coverage review spec to point at
  `nes_py/tests/mappers/`.

## Verification

Commands were run inside `nes-py` with `.venv/bin/python` because `python` is not
available on PATH and the system `python3` environment is externally managed.

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover nes_py/tests/mappers` (21 tests)
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_registry`
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_lifecycle_hooks`
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_mapper_000_nrom`
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_mapper_001_sxrom`
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_mapper_002_uxrom`
- `.venv/bin/python -m unittest nes_py.tests.mappers.test_mapper_003_cnrom`
- `.venv/bin/python -m unittest discover nes_py/tests` (192 tests)
- `git diff --check`

Gym emitted its existing unmaintained-package warning during test startup; all
listed test commands passed.

## Commits

- `nes-py`: `b4a198d` (`Refactor mapper tests into package`), pushed to
  `origin/ralph-dev`.

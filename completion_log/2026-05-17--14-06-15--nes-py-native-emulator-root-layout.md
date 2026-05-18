# nes-py Native Emulator Root Layout

## Summary

Completed work item 022 in `nes-py`.

- Moved the native emulator implementation from `nes_py/nes` to `nes_emu`.
- Placed headers under `nes_emu/include/nes_emu` and sources under
  `nes_emu/src/nes_emu`, including mapper subdirectories.
- Updated CMake, Cython extern declarations, C++ includes, sdist inclusion,
  and README development notes for the project-scoped native layout.

## Verification

Commands were run inside `nes-py` with `.venv/bin/python`.

- `.venv/bin/python -m pip install --upgrade pip build`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_app_imports`
- `.venv/bin/python -m unittest nes_py.tests.test_rom`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m build`
- `.venv/bin/python -m pip install dist/*.whl --force-reinstall`
- `.venv/bin/python -c "import nes_py; import nes_py._native; print(nes_py.__name__)"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `rg "nes_py/nes|nes-py/nes|nes/.*include|from \"common.hpp\"|#include \"common.hpp\"" .`
- `git diff --check`

The wheel listing included only the Python package and compiled extension. The
sdist listing included the root-level `nes_emu/include/nes_emu/...` and
`nes_emu/src/nes_emu/...` native source tree.

## Commits

- `nes-py`: `bbecebc` (`Move native emulator sources to nes_emu`), pushed to
  `origin/ralph-dev`.

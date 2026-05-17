# Specification: nes-py Native Emulator Root Layout

## Status: COMPLETE

## Problem

The native NES emulator code currently lives under `nes_py/nes`, which made sense when the Python package tree also owned the extension build layout. After the scikit-build/CMake migration, the C++ code no longer needs to live literally inside the import package. Keeping it there makes the repository layout harder to scan, blurs Python package contents with native source layout, and keeps includes in an un-namespaced `include/*` form that is less standard for C++ projects.

Move the native emulator implementation into a root-level C++ source tree and give headers and sources a project-scoped layout.

## Current Findings

- `nes-py/CMakeLists.txt` sets `NES_NATIVE_ROOT` to `nes_py/nes`.
- Native headers currently live at `nes_py/nes/include/*.hpp` and `nes_py/nes/include/mappers/*.hpp`.
- Native sources currently live at `nes_py/nes/src/*.cpp` and `nes_py/nes/src/mappers/*.cpp`.
- C++ files include local project headers as `"common.hpp"`, `"emulator.hpp"`, and `"mappers/mapper_NROM.hpp"`.
- `nes_py/_native.pyx` declares C++ bindings from headers such as `"common.hpp"`, `"cartridge.hpp"`, `"emulator.hpp"`, and `"mapper_factory.hpp"`.
- The new build system already owns native compilation through CMake, so source discovery can target a root-level native tree instead of the Python package directory.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Move the native emulator tree from `nes_py/nes` to root-level `nes_emu`.
- Use a standard project-scoped C++ layout:
  - Headers under `nes_emu/include/nes_emu/...`
  - Sources under `nes_emu/src/nes_emu/...`
  - Mapper headers and sources under matching `nes_emu/mappers/...` subdirectories.
- Update CMake to compile the moved source tree and expose `nes_emu/include` as the include root.
- Update C++ includes and Cython extern declarations to use project-scoped paths such as `nes_emu/common.hpp`, `nes_emu/emulator.hpp`, and `nes_emu/mappers/mapper_NROM.hpp`.
- Preserve the existing C++ namespace, Python package name, Python extension module name, public Python API, mapper support, runtime behavior, and build backend.
- Update documentation, developer notes, and repository references that still point maintainers at `nes_py/nes`.

## Non-Goals

- Do not rename the Python package from `nes_py`.
- Do not rename the Cython extension module or move `_native.pyx` out of `nes_py`.
- Do not change the C++ namespace from `NES` in this spec.
- Do not perform emulator optimizations or mapper behavior changes beyond what is required for the layout migration.
- Do not add or remove mapper implementations.
- Do not add generated build artifacts, compiled extensions, wheels, sdists, caches, or local virtual environments.

## Acceptance Criteria

- [x] The native emulator tree lives at `nes-py/nes_emu`.
- [x] No native emulator headers or sources remain under `nes-py/nes_py/nes`; the old directory is removed once the move is complete.
- [x] Public and internal native headers live under `nes_emu/include/nes_emu`, including mapper headers under `nes_emu/include/nes_emu/mappers`.
- [x] Native source files live under `nes_emu/src/nes_emu`, including mapper sources under `nes_emu/src/nes_emu/mappers`.
- [x] CMake no longer references `nes_py/nes`; it discovers native sources from `nes_emu/src/nes_emu` and adds `nes_emu/include` to the extension include path.
- [x] All project header includes in C++ use the project-scoped include path, for example `#include "nes_emu/common.hpp"` or an equivalent angle-bracket include.
- [x] `nes_py/_native.pyx` Cython extern declarations include headers through the project-scoped path, for example `cdef extern from "nes_emu/emulator.hpp" namespace "NES"`.
- [x] Any source-distribution configuration includes the root-level `nes_emu` tree, while wheel/install contents do not accidentally expose the native source tree as Python package data.
- [x] `rg "nes_py/nes|nes-py/nes|nes/.*include|from \"common.hpp\"|#include \"common.hpp\"" nes-py` finds no stale layout references except in intentional historical notes or archived logs.
- [x] Editable install, wheel build, and sdist build still compile the native extension with the moved layout.
- [x] Existing Python tests for imports, ROM parsing, mapper behavior, environment stepping, app entry points, and speedtest behavior still pass.
- [x] No generated profiling dumps, build artifacts, wheels, caches, compiled extensions, or local virtual environments are committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install --upgrade pip build
python -m pip install -e .
python -m unittest nes_py.tests.test_app_imports
python -m unittest nes_py.tests.test_rom
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_nes_env
python -m unittest nes_py.tests.test_speedtest
python -m unittest discover .
python -m build
python -m pip install dist/*.whl --force-reinstall
python -c "import nes_py; import nes_py._native; print(nes_py.__name__)"
python -m zipfile -l dist/*.whl
python -m tarfile -l dist/*.tar.gz
rg "nes_py/nes|nes-py/nes|from \"common.hpp\"|#include \"common.hpp\"" .
```

Inspect the wheel listing to confirm the installed Python package does not include the native source tree as package data. Inspect the sdist listing to confirm `nes_emu/include/nes_emu/...` and `nes_emu/src/nes_emu/...` are present.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-native-emulator-root-layout.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

## Completion Log

Completed in `nes-py` commit `bbecebc` by moving the native emulator source
tree from `nes_py/nes` to `nes_emu`, with headers under
`nes_emu/include/nes_emu` and sources under `nes_emu/src/nes_emu`. Updated CMake
source discovery, Cython extern declarations, C++ project includes, sdist
configuration, and README development notes for the new layout.

Verification used `.venv/bin/python`:

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

The wheel listing included only the Python package and compiled extension; the
sdist listing included `nes_emu/include/nes_emu/...` and
`nes_emu/src/nes_emu/...`.

<!-- NR_OF_TRIES: 1 -->

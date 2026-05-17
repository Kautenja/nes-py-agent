# Specification: nes-py Cython Binding Migration

## Status: COMPLETE

## Problem

The current Python binding uses `ctypes` to load `lib_nes_env*`, discover symbols by globbing package paths, pass a wide-character ROM path into a C ABI, and call small native functions for reset, step, backup, restore, screen, memory, and controller buffers. This works, but it adds dynamic-loading complexity, weak error handling, path conversion risk, and avoidable Python overhead around hot operations.

Moving the binding layer toward Cython should make the native interface faster, easier to package, and easier to build under `pyproject.toml`, while keeping the public `NESEnv` behavior stable.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Add a Cython extension layer that owns or wraps the C++ `Emulator` directly.
- Preserve the public Python API expected by wrappers and tests.
- Expose NumPy-compatible screen, RAM, and controller buffers without copying during normal operation.
- Release the GIL around frame stepping where it is safe.
- Keep ctypes as a temporary fallback only if needed during migration, and document any remaining fallback path.

## Binding Direction

The implementation should prefer:

- typed Cython declarations for `NES::Emulator` and relevant buffer pointer methods;
- a small Python-visible wrapper object that manages emulator lifetime with deterministic close behavior;
- direct `step(action)` or `frame_advance(action)` paths that avoid NumPy slice assignment plus a separate ctypes call;
- exception translation from native initialization failures into Python exceptions;
- memoryview or NumPy array views over stable native buffers;
- a reviewed screen-buffer layout: the current native 32-bit pixel buffer plus Python channel reversal creates a 24-bit view through slicing, so the migration should either expose an efficient RGB observation view or document why the existing layout remains best;
- tests proving arrays remain valid after reset, step, backup, restore, and close boundaries.

## Non-Goals

- Do not rewrite the emulator core in Cython.
- Do not change game wrapper APIs.
- Do not remove the old binding path until the Cython path passes tests, benchmarks, and packaging checks on supported platforms.

## Acceptance Criteria

- [ ] A Cython extension builds under the active `pyproject.toml` build system.
- [ ] `NESEnv` uses the Cython binding path by default when available.
- [ ] The old ctypes dynamic-library globbing path is removed or retained only as an explicitly documented fallback.
- [ ] Native emulator lifetime is deterministic: close is idempotent or raises the same documented error as before, and object destruction does not leak or double-free.
- [ ] Native initialization errors are translated into Python exceptions with clear messages.
- [ ] Screen, RAM, and controller arrays have the same shapes, dtypes, mutability, and no-copy behavior expected by current tests and wrappers.
- [ ] Screen buffer exposure is benchmarked and checked for layout surprises such as negative strides, needless channel shuffles, or avoidable observation copies.
- [ ] Stepping with an action avoids unnecessary Python-level buffer writes when the Cython path can pass the action directly.
- [ ] The GIL is released around the native frame step if thread safety analysis shows it is safe.
- [ ] Existing `NESEnv` tests, wrapper expectations, and benchmark CLI behavior pass without public API regression.
- [ ] Benchmarks compare ctypes and Cython binding paths where both exist, or compare against the spec 010 baseline after ctypes removal.
- [ ] Any performance claim in the completion log is backed by benchmark output, not intuition.
- [ ] Source distributions include `.pyx` and generated C/C++ sources according to the release policy chosen for the project.
- [ ] Wheels build and import successfully from a clean environment.
- [ ] No generated build artifacts outside intentionally packaged generated C/C++ sources, caches, or local virtual environments are committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install --upgrade pip build
python -m pip install -e .
python -m unittest nes_py.tests.test_nes_env
python -m unittest nes_py.tests.test_mappers
python -m unittest discover .
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 200 --warmup-steps 50 --json --no-progress
python -m build
```

If a temporary binding selector is provided, run the test and benchmark suite with both the ctypes and Cython paths before removing the ctypes path.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-cython-binding-migration.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

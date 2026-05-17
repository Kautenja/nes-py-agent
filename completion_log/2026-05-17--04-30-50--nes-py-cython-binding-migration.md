# Completion Log: nes-py Cython Binding Migration

## Summary

Migrated `NESEnv` from the Python `ctypes` shared-library loader to a default
`nes_py._native` Cython extension that owns `NES::Emulator` directly. The new
binding exposes writable no-copy NumPy views for screen, RAM, and controller
buffers, translates native C++ initialization failures into Python exceptions,
passes controller actions directly before frame stepping, and releases the GIL
around the per-frame native `Emulator::step()` call. Existing mapper metadata
and smoke helpers are retained through linked legacy C ABI helper functions, not
runtime dynamic library discovery.

The screen view preserves the existing zero-copy RGB layout over the native
32-bit pixel buffer: shape `(240, 256, 3)`, dtype `uint8`, writable, base object
`NativeEmulator`, and strides `(1024, 4, -1)` on this little-endian platform.
The negative channel stride is deliberate to avoid copying or channel-shuffling
the native `0x00RRGGBB` pixel buffer during normal observation access.

## Verification

Run inside `nes-py` with `.venv/bin/python`:

- `.venv/bin/python -m pip install --upgrade pip build`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_cartridge_metadata nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 200 --warmup-steps 50 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 200 --json --no-progress`
- screen view layout benchmark: 5000 `render('rgb_array')` accesses in `0.0004600000102072954` seconds, `10869564.97619813` views/s, shape `(240, 256, 3)`, dtype `uint8`, strides `(1024, 4, -1)`, native base `True`, writable `True`
- ctypes baseline comparison from temporary worktree at `a290cab`: 1000 measured steps, `874.5252967305697` steps/s
- Cython path comparison from current tree: 1000 measured steps, `879.923672745649` steps/s
- `.venv/bin/python -m build`
- clean virtualenv wheel install from `dist/*.whl` and import of `nes_py._native.NativeEmulator`
- `.venv/bin/python -m pip check`
- `git diff --check`

Build warnings about NumPy headers not being added to `MANIFEST.in` are expected
because NumPy is a build dependency, not vendored package data.

## Commits Pushed

- `nes-py`: `690386c` (`Migrate NESEnv to Cython native binding`) pushed to
  `origin/ralph-dev`.

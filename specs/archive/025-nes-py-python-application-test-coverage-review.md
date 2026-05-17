# Specification: nes-py Python Application Test Coverage Review

## Status: COMPLETE

## Problem

As native emulator tests and benchmarks move out of the Python extension surface,
the Python test suite needs a deliberate coverage review. Some current Python
tests reach into private native hooks, mapper PRG/CHR internals, or
characterization helpers that should live at the C++ layer after the native API
separation work. Those assertions should not be silently dropped: useful
low-level coverage should be ported to Catch2 if an equivalent native test does
not already exist, and then removed from Python.

Python tests should cover the application-level behavior that package consumers
actually use: ROM validation, environment construction, reset/step/render/close
flows, deterministic backup/restore behavior exposed through the package's
existing workflows, multi-environment behavior, app entry points, and the public
speedtest API/CLI.

## Current Findings

- Available on-disk test ROMs include:
  - `nes_py/tests/games/super-mario-bros-1.nes`
  - `nes_py/tests/games/super-mario-bros-2.nes`
  - `nes_py/tests/games/super-mario-bros-3.nes`
  - `nes_py/tests/games/super-mario-bros-lost-levels.nes`
  - `nes_py/tests/games/the-legend-of-zelda.nes`
  - `nes_py/tests/games/excitebike.nes`
  - invalid fixtures `nes_py/tests/games/blank` and
    `nes_py/tests/games/empty.nes`
- `nes_py/tests/mapper_fixtures.py` can synthesize iNES ROMs for mapper and
  header edge cases when existing disk ROMs are not enough.
- `nes_py/tests/test_nes_env.py` covers many public environment workflows but
  also imports `_native`, asserts implementation details of `NativeEmulator`,
  and uses private backup/restore behavior directly.
- `nes_py/tests/mappers/` characterizes native mapper behavior through package
  modules that currently use private `_read_prg`, `_write_prg`, `_read_chr`,
  and `_write_chr` helpers.
- `nes_py/tests/test_native_cpu_bus.py` validates native CPU and main-bus
  characterization helpers through Python rather than through C++ tests.
- `nes_py/tests/test_speedtest.py` currently covers both public `NESEnv`
  throughput benchmarking and native microbenchmark plumbing.
- Spec 024 removes native test and benchmark fixtures from the Python extension
  surface; this spec audits the Python suite after that boundary is cleaned up.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Perform this after spec 024, or perform it together with spec 024 if that is
  more efficient and the completion log clearly explains the combined work.
- Review every Python test module under `nes_py/tests`.
- Classify each test as one of:
  - public application-level Python coverage to keep;
  - useful native-internal coverage to port to Catch2 before removing from
    Python;
  - obsolete or duplicated coverage to remove after confirming equivalent
    coverage exists elsewhere.
- Use the ROMs already available in `nes_py/tests/games` to broaden
  application-level environment coverage across real mapper/game combinations.
- Use synthesized temporary ROMs for validation or edge cases that the on-disk
  ROM set cannot cover without adding new assets.
- Preserve or improve current public behavior coverage for ROM parsing,
  environment construction, resets, stepping, rendering, close/error behavior,
  backup/restore behavior reachable through existing package workflows,
  multi-instance behavior, app imports, and speedtest CLI/API behavior.
- Keep Python tests reasonably fast and deterministic. Use short step counts,
  fixed seeds, `subTest` loops, and synthetic ROMs where appropriate.
- Update test helper module names and docstrings so they describe
  application-level fixtures instead of native mapper characterization fixtures
  when their role changes.

## Non-Goals

- Do not add new external or commercial ROM assets.
- Do not make Python tests inspect native mapper, CPU, bus, PPU, or benchmark
  internals by adding replacement private hooks.
- Do not preserve Python tests solely because they existed before if their only
  purpose is native-internal characterization.
- Do not remove useful low-level assertions until they are either covered by
  existing Catch2 tests or ported to new Catch2 tests.
- Do not change emulator behavior except to fix a real issue exposed by the
  coverage review.
- Do not convert the project away from `unittest`.

## Application Coverage Targets

The final Python suite should cover these public workflows:

- Importing package modules and app entry points without side effects.
- Rejecting invalid ROM paths, non-iNES files, empty ROMs, unsupported mapper
  ROMs, PAL ROMs, trainer ROMs, and malformed headers through public
  construction or ROM metadata paths.
- Constructing `NESEnv` for every usable on-disk ROM and confirming Gym-level
  metadata, action space, observation space, reset output shape/dtype, and close
  behavior.
- Stepping every usable on-disk ROM for a small deterministic action sequence
  and confirming returned tuple shape, observation shape/dtype, reward type,
  done flag type, and info dictionary type.
- Rendering `rgb_array` for representative ROMs and confirming the frame shape,
  dtype, and absence of aliasing surprises visible through the public API.
- Running two or more environments in the same process without shared mutable
  state leaks visible through observations, RAM, controller buffers, or close
  behavior.
- Exercising backup/restore behavior only through supported package workflows
  that are intentionally kept; if backup/restore remains private, tests should
  justify the package-level need or move deeper assertions to C++.
- Verifying deterministic continuation for fixed seeds/action sequences where
  the public API promises or relies on determinism.
- Running the public `nes_py.speedtest` API and CLI against at least one
  on-disk ROM and one synthesized ROM where useful.

## Acceptance Criteria

- [x] Every Python test module under `nes_py/tests` has been reviewed and
  classified in the completion log or a short developer note.
- [x] Useful native-internal assertions removed from Python are covered by
  Catch2 tests under `nes_emu/test/nes_emu/*`, unless an equivalent Catch2 test
  already exists and is cited.
- [x] Python tests no longer import `_native` directly for native internals.
- [x] Python tests no longer import `nes_env` helper functions whose only
  purpose is native smoke, characterization, or microbenchmark coverage.
- [x] Python tests no longer use private PRG/CHR mapper read/write hooks to
  characterize mapper internals.
- [x] If Python tests still call any private `NESEnv` helper, each remaining use
  is justified as package-level behavior that has no public equivalent yet, or a
  follow-up spec is created to expose/remove that behavior intentionally.
- [x] Application-level tests exercise every usable on-disk `.nes` ROM at least
  for construction, reset, short deterministic stepping, and close.
- [x] Invalid on-disk fixtures `blank` and `empty.nes` remain covered through
  public error paths.
- [x] Synthesized ROMs are used for edge cases not covered by the on-disk ROM
  set, such as unsupported mappers, PAL flags, trainers, NES 2.0 metadata, or
  small deterministic mapper smoke workflows.
- [x] Speedtest tests cover the public API/CLI only and do not invoke native
  C++ microbenchmarks through Cython.
- [x] Multi-environment behavior is covered at the Python level.
- [x] Test names and helper docstrings reflect application-level intent rather
  than native characterization when they remain in Python.
- [x] Python test discovery is deterministic and does not depend on commercial
  ROM downloads or network access.
- [x] No generated build trees, FetchContent downloads, compiled binaries,
  wheels, sdists, caches, `.pyc` files, or local virtual environments are
  committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository
  records the updated submodule pointer.

## Verification

Run focused native checks if this spec ports coverage to new or existing Catch2
tests:

```sh
cd nes-py
cmake -S . -B build/nes-emu-debug \
  -DCMAKE_BUILD_TYPE=Debug \
  -DNES_EMU_BUILD_TESTS=ON \
  -DNES_EMU_BUILD_BENCHMARKS=OFF
cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests
ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure
```

Run the Python package checks:

```sh
cd nes-py
python -m pip install -e .
python -m unittest discover nes_py/tests
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 10 --json --no-progress
rg "from nes_py import _native|import nes_py._native|_native_.*smoke|characterization_smoke|native_.*benchmark|_read_prg|_write_prg|_read_chr|_write_chr" nes_py/tests nes_py/speedtest.py
```

Run build/package checks if test helper layout or package data configuration
changes:

```sh
cd nes-py
python -m build
python -m pip install dist/*.whl --force-reinstall
python -c "import nes_py; from nes_py.nes_env import NESEnv; print(nes_py.__name__, NESEnv.__name__)"
python -m zipfile -l dist/*.whl
python -m tarfile -l dist/*.tar.gz
```

The `rg` command should report no Python tests or speedtest code reaching into
removed native-internal hooks. If a private helper remains by design, document
the exception and the reason in the completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink and this
  spec if it is still active.
- Append the required one-line summary to `history.md`.
- Add the required
  `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-python-application-test-coverage-review.md`
  file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 1 -->

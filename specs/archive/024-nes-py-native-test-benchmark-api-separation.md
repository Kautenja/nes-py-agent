# Specification: nes-py Native Test and Benchmark API Separation

## Status: COMPLETE

## Problem

Native emulator characterization and benchmarking code has leaked into the
runtime library boundary. `lib_nes_env.cpp` contains C++ test mappers, smoke
checks, characterization helpers, and microbenchmark runners alongside the C ABI
used by the Cython extension. Those helpers are then declared and exposed through
`nes_py/_native.pyx`, which makes testing and benchmarking fixtures part of the
Python native module surface.

This makes the runtime source harder to reason about, bloats the compiled
extension, and encourages Python tests to reach below the API that emulator
consumers actually use. C++ internals should be tested and benchmarked at the
C++ layer. Python should test user-facing emulator behavior through `NESEnv`,
the package API, and the supported benchmark CLI/API only.

## Current Findings

- `nes-py/nes_py/nes/src/lib_nes_env.cpp` contains fixture mappers such as
  `ProgramTestMapper`, `IRQTestMapper`, `ExpansionTestMapper`,
  `PRGRAMTestMapper`, `NameTableTestMapper`, and `PictureBusTestMapper`.
- The same file exports C ABI test and benchmark functions such as
  `MapperIRQSmokeTest`, `CPUCharacterizationSmokeResults`,
  `MainBusCharacterizationSmokeResults`, `PPUCharacterizationSmokeResults`,
  `NativeCPUDispatchBenchmark`, `NativeMainBusIODispatchBenchmark`, and mapper
  hook benchmark helpers.
- `nes-py/nes_py/_native.pyx` declares those C ABI helpers and exposes Python
  wrappers such as `mapper_hook_smoke_results`,
  `cpu_characterization_smoke_results`, and
  `native_cpu_dispatch_benchmark`.
- Python tests import private native characterization wrappers from
  `nes_py.nes_env` and inspect mapper internals through private PRG/CHR read and
  write helpers.
- `nes-py/nes_py/speedtest.py` mixes public `NESEnv` throughput benchmarking
  with C++ microbenchmarks that only exist because native benchmark functions are
  exported through `_native.pyx`.
- Spec 022 will move native emulator code into root-level `nes_emu`, so this
  cleanup should target that layout instead of adding more files under
  `nes_py/nes`.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Perform this after spec 022, or preserve the spec 022 target layout while
  doing the work.
- Keep runtime native source under `nes_emu/src/nes_emu` and runtime headers
  under `nes_emu/include/nes_emu`.
- Move native C++ tests into `nes_emu/test/nes_emu/*`.
- Move native C++ benchmarks into `nes_emu/benchmark/nes_emu/*`.
- Add Catch2 through CMake `FetchContent` with a pinned Catch2 v3 tag. Do not
  vendor Catch2 into the repository.
- Add explicit CMake options/targets for native tests and benchmarks. They
  should be off for normal Python package builds and enabled only when requested.
- Link C++ tests and benchmarks against the native emulator implementation
  without routing through the Python extension or Cython bindings.
- Keep `lib_nes_env.cpp` focused on runtime glue needed by the Cython extension.
- Remove C++ test, characterization, and benchmark exports from the runtime C
  ABI.
- Remove Cython declarations and Python wrappers whose only purpose is native
  C++ testing, characterization, or microbenchmarking.
- Move any Python test coverage that depends on native internals into Catch2
  tests, preserving the behavioral assertions at the appropriate layer.
- Keep Python tests focused on the public package behavior that users exercise:
  constructing environments, resetting, stepping, rendering, closing, ROM
  validation visible through supported APIs, and the supported speedtest CLI/API.
- Keep public Python API names and runtime behavior stable unless a name exists
  only for native internals or test/benchmark plumbing.

## Target Layout

After spec 022, use this shape for native-only verification code:

```text
nes_emu/
  CMakeLists.txt
  include/nes_emu/...
  src/nes_emu/...
  test/nes_emu/
    test_cartridge.cpp
    test_cpu.cpp
    test_main_bus.cpp
    test_mapper_hooks.cpp
    test_mapper_bank_helpers.cpp
    test_picture_bus.cpp
    test_ppu.cpp
    support/...
  benchmark/nes_emu/
    benchmark_cpu_dispatch.cpp
    benchmark_main_bus.cpp
    benchmark_mapper_hooks.cpp
    benchmark_frame_step.cpp
    support/...
```

Exact filenames may differ, but test fixtures and benchmark fixtures must live
under the native test or benchmark trees, not in runtime sources or Cython.

## Build Configuration Requirements

- Native tests are configured and run with a Debug build.
- Native benchmarks are configured and run with a Release build.
- Normal editable installs, wheel builds, and sdist builds do not build tests,
  benchmarks, or FetchContent dependencies by default.
- Test and benchmark targets should be discoverable from CMake target names,
  for example `nes_emu_tests` and `nes_emu_benchmarks`, or similarly clear
  project-scoped names.
- CTest should be wired for the Catch2 tests. Benchmark executables may be
  runnable directly and should not impose machine-specific pass/fail timing
  thresholds.

## Non-Goals

- Do not change emulator behavior except to fix a real issue exposed while
  moving tests to the correct layer.
- Do not rename the Python package, Cython extension module, or consumer-facing
  environment API.
- Do not replace the existing Python speedtest CLI for public `NESEnv`
  throughput measurement.
- Do not make Python tests cover native mapper, CPU, bus, PPU, or benchmark
  internals by adding new private hooks.
- Do not add commercial ROMs or external binary assets.
- Do not commit generated build trees, FetchContent downloads, compiled
  binaries, wheels, sdists, caches, or local virtual environments.

## Acceptance Criteria

- [ ] Native runtime sources no longer define test-only mapper classes,
  characterization smoke suites, or microbenchmark runners.
- [ ] `lib_nes_env.cpp` contains only C ABI/runtime glue needed by the Cython
  extension and no test or benchmark fixtures.
- [ ] C++ tests that need native internals live under `nes_emu/test/nes_emu/*`
  and are implemented with Catch2.
- [ ] C++ benchmarks that need native internals live under
  `nes_emu/benchmark/nes_emu/*` and are implemented with Catch2 benchmark
  support or another Catch2-compatible benchmark executable.
- [ ] Catch2 is added with CMake `FetchContent` using a pinned tag and is
  fetched only when native tests or benchmarks are enabled.
- [ ] Native test targets build and run from a Debug CMake configuration.
- [ ] Native benchmark targets build and run from a Release CMake
  configuration.
- [ ] The Python extension build does not link C++ test or benchmark sources.
- [ ] The Python extension's exported C ABI no longer includes smoke,
  characterization, or benchmark functions.
- [ ] `nes_py/_native.pyx` no longer declares or exposes native smoke,
  characterization, or benchmark functions.
- [ ] `nes_py/nes_env.py` no longer re-exports private native characterization
  helpers for Python tests.
- [ ] Python tests do not import `_native` or `nes_env` helper functions solely
  to test C++ internals.
- [ ] Python tests do not use private PRG/CHR mapper read/write hooks to
  characterize native mapper implementation details; equivalent coverage lives
  in Catch2 tests.
- [ ] Python benchmark code keeps public `NESEnv` throughput measurement but no
  longer invokes C++ microbenchmarks through Cython.
- [ ] Existing public Python behavior for environment construction, reset,
  step, render, close, backup/restore behavior exposed through existing package
  workflows, and speedtest operation is preserved.
- [ ] Source distribution configuration includes the native test and benchmark
  source files if they are part of the repository, while wheels do not install
  them as Python package data.
- [ ] Stale references to native smoke/characterization/benchmark wrappers are
  removed from active docs and tests.
- [ ] `rg "SmokeTest|CharacterizationSmoke|Native.*Benchmark|ProgramTestMapper|IRQTestMapper|ExpansionTestMapper|PRGRAMTestMapper|PictureBusTestMapper" nes-py/nes_emu/src nes-py/nes_py/_native.pyx nes-py/nes_py/nes_env.py` finds no hits.
- [ ] `rg "_native_.*smoke|characterization_smoke|native_.*benchmark|_read_prg|_write_prg|_read_chr|_write_chr" nes-py/nes_py/tests nes-py/nes_py/speedtest.py` finds no Python tests or benchmark code reaching into removed native internals.
- [ ] Editable install, wheel build, and sdist build still succeed without
  enabling native tests or benchmarks.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository
  records the updated submodule pointer.

## Verification

Run focused checks inside the submodule after spec 022 has established the
`nes_emu` layout:

```sh
cd nes-py

cmake -S . -B build/nes-emu-debug \
  -DCMAKE_BUILD_TYPE=Debug \
  -DNES_EMU_BUILD_TESTS=ON \
  -DNES_EMU_BUILD_BENCHMARKS=OFF
cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests
ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure

cmake -S . -B build/nes-emu-release \
  -DCMAKE_BUILD_TYPE=Release \
  -DNES_EMU_BUILD_TESTS=OFF \
  -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks
```

Run the benchmark executable directly with a small, portable iteration/sample
count and record the command in the completion log. Benchmark output is
informational and should not use a machine-specific timing threshold as a pass
or fail condition.

Then verify the Python package still builds and behaves through public paths:

```sh
cd nes-py
python -m pip install --upgrade pip build
python -m pip install -e .
python -m unittest discover nes_py/tests
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 10 --json --no-progress
python -m build
python -m pip install dist/*.whl --force-reinstall
python -c "import nes_py; import nes_py._native; print(nes_py.__name__)"
python -m zipfile -l dist/*.whl
python -m tarfile -l dist/*.tar.gz
rg "SmokeTest|CharacterizationSmoke|Native.*Benchmark|ProgramTestMapper|IRQTestMapper|ExpansionTestMapper|PRGRAMTestMapper|PictureBusTestMapper" nes_emu/src nes_py/_native.pyx nes_py/nes_env.py
rg "_native_.*smoke|characterization_smoke|native_.*benchmark|_read_prg|_write_prg|_read_chr|_write_chr" nes_py/tests nes_py/speedtest.py
```

Inspect the wheel listing to confirm tests, benchmarks, FetchContent downloads,
and native source trees are not installed as Python package data. Inspect the
sdist listing to confirm the source files needed to build and run optional
native tests and benchmarks are present.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink and this
  spec if it is still active.
- Append the required one-line summary to `history.md`.
- Add the required
  `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-native-test-benchmark-api-separation.md`
  file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 1 -->

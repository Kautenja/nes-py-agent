# Completion Log: nes-py Vectorized Native Emulator

## Summary

Completed work item 050 by adding an opt-in `VectorNESEmulator` API backed by a
Cython `NativeVectorEmulator` that owns same-ROM native emulator instances and
supports batched reset, reset-one, step, step-one, zero-copy per-slot screen/RAM
views, contiguous RGB and grayscale batch copies, RAM readback, close semantics,
and per-slot opaque snapshots. The kept prototype is intentionally serial and
GIL-released during native stepping; worker threads, busy waits, and CPU
affinity are left to future evidence-driven work.

## Verification

- `nes-py`: `.venv/bin/python -m pip install -e .`
- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_vector_env nes_py.tests.test_ram_reads nes_py.tests.test_speedtest nes_py.tests.test_nes_env` (`50 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest discover .` (`246 tests`, `OK`)
- `nes-py`: `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON`
- `nes-py`: `cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks`
- `nes-py`: `build/nes-emu-release/nes_emu_tests` (`819 assertions in 71 test cases`, `OK`)
- `nes-py`: `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --vector-profile --steps 10 --warmup-steps 2 --runs 2 --env-counts 1,2,4 --action-policy noop --vector-backend scalar_loop --vector-backend gym_sync_vector_env --vector-backend native_vector --vector-observation step_only --vector-observation native_grayscale --vector-observation ram_info --instrumentation --json --no-progress`
- `nes-py`: `git diff --check`

## Notes

The vector benchmark report in `docs/vector-native-emulator.md` records five
runs across 1, 2, 4, 8, and 16 envs. The serial native vector prototype did not
meet the 10% / 15% throughput threshold, but it showed no meaningful regression
and is kept as a simpler same-ROM native API plus a stable baseline for future
threaded experiments.

## Commits

- `nes-py`: `61862c9` (`p90`, pushed to `origin/p90`)
- Umbrella: included in the umbrella commit that records this completion log

# nes-py Native Test and Benchmark API Separation

## Summary

- Moved native smoke, characterization, mapper-bank, mapper implementation, and hot-path benchmark coverage into opt-in Catch2 CMake targets under `nes_emu/test/nes_emu` and `nes_emu/benchmark/nes_emu`.
- Removed native smoke/characterization/benchmark C ABI exports from the runtime source and removed matching Cython/Python wrappers.
- Removed Python tests and speedtest paths that reached into native internals, keeping Python coverage focused on public `NESEnv`, ROM metadata, and packaged speedtest behavior.
- Kept optional native tests and benchmarks out of normal Python extension builds while including their source files in the sdist.

## Verification

- `cmake -S . -B build/nes-emu-debug -DCMAKE_BUILD_TYPE=Debug -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=OFF`
- `cmake --build build/nes-emu-debug --config Debug --target nes_emu_tests`
- `ctest --test-dir build/nes-emu-debug -C Debug --output-on-failure`
- `cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=OFF -DNES_EMU_BUILD_BENCHMARKS=ON`
- `cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks`
- `./build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1 --benchmark-warmup-time 0 --durations yes`
- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest discover nes_py/tests`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 10 --json --no-progress`
- `.venv/bin/python -m build`
- `.venv/bin/python -m pip install dist/*.whl --force-reinstall`
- `nes-py/.venv/bin/python -c "import nes_py; import nes_py._native; print(nes_py.__name__)"`
- `.venv/bin/python -m zipfile -l dist/*.whl`
- `.venv/bin/python -m tarfile -l dist/*.tar.gz`
- `rg "SmokeTest|CharacterizationSmoke|Native.*Benchmark|ProgramTestMapper|IRQTestMapper|ExpansionTestMapper|PRGRAMTestMapper|PictureBusTestMapper" nes_emu/src nes_py/_native.pyx nes_py/nes_env.py`
- `rg "_native_.*smoke|characterization_smoke|native_.*benchmark|_read_prg|_write_prg|_read_chr|_write_chr" nes_py/tests nes_py/speedtest.py`
- `git diff --check`

Notes:

- `python` is not on PATH in this environment, so package verification used `.venv/bin/python`.
- The system `python3` is PEP 668-managed, so a local venv was used instead of installing into the Homebrew-managed interpreter.
- Gym emitted its existing unmaintained/NumPy 2 warning during Python test and speedtest runs.

## Commits

- `nes-py` child submodule: `13952a9abc1782cea7d743bed5fd5dd7e8d21c89` (`Separate native tests and benchmarks`), pushed to `origin/ralph-dev`.
- Umbrella repository: this completion commit records the `nes-py` gitlink update, archive summary, history entry, and completion log.

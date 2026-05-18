# nes-py ML Observation Fast Paths

## Summary

- Added explicit `NESEnv.observation(...)` modes for the existing zero-copy
  screen view, reusable native C-contiguous RGB copies, and reusable native
  grayscale copies.
- Kept `NESEnv.step` and `render` in `rgb_array` mode backward compatible:
  both still expose the default `(240, 256, 3)` `uint8` screen view.
- Added a packaged observation benchmark profile that measures step-only,
  `step + copy`, `step + contiguous`, NumPy grayscale, native RGB, and native
  grayscale loops.
- Added Python coverage for shape, dtype, contiguity, buffer reuse, reset,
  render, buffer lifetime, close behavior, invalid outputs, and CLI JSON
  benchmark output.
- Documented intended ML usage and benchmark tradeoffs in `README.md` and
  `docs/ml-observation-fast-paths.md`.

## Benchmark Notes

Command run in `nes-py`:

- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress`

Local smoke profile, CPython 3.14.2 on macOS:

- Before `8e33e74`: `step` 1106.94 steps/s, `step_copy` 1114.20 steps/s,
  `step_contiguous` 1112.28 steps/s, `step_python_grayscale`
  1257.46 steps/s.
- After `4f55cf8`: `step` 1440.57 steps/s, `step_copy` 1117.23 steps/s,
  `step_contiguous` 1120.66 steps/s, `step_python_grayscale`
  1261.50 steps/s, `step_native_rgb_contiguous` 1420.08 steps/s,
  `step_native_grayscale` 1403.44 steps/s.

Treat the profile as local direction rather than a portable threshold. Native
RGB and grayscale copy helpers are kept because they avoid the NumPy
post-processing cost in this measured training-loop-style smoke test.

## Verification

Commands run in `nes-py`:

- `.venv/bin/python -m pip install -e .` passed.
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env` passed: 27 tests.
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest` passed: 7 tests.
- `.venv/bin/python -m unittest discover .` passed: 230 tests.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress` passed: 1507.62 steps/s.
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress` passed and produced all six observation operations.
- `git diff --check` passed in `nes-py`.

No C++ observation helper was added, so no new native Catch2 target was required
for this spec.

## Commits

- `nes-py`: `4f55cf8` (`Add ML observation fast paths`), pushed to
  `origin/ralph-dev`.
- Umbrella repository: this commit records the `nes-py` submodule pointer,
  completion log, history entry, and archived spec.

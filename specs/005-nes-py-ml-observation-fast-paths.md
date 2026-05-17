# Specification: nes-py ML Observation Fast Paths

## Problem

Raw emulator stepping is only one part of ML training throughput. The current
public screen view is zero-copy, but it is a 24-bit RGB NumPy view over a
32-bit native pixel buffer with non-contiguous strides and a negative channel
stride on little-endian platforms. Downstream training pipelines often copy,
crop, grayscale, downsample, stack, or otherwise transform observations after
every step. Local probes showed that `step + screen.copy()` and simple Python
grayscale conversion can cost hundreds of fps.

This spec adds measured native observation fast paths for deep Q-learning style
pipelines without changing the default `NESEnv.step` contract.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Preserve the existing default observation shape `(240, 256, 3)` and dtype
  `uint8`.
- Explore opt-in observation modes or helper APIs for one or more of:
  - contiguous RGB output
  - grayscale output
  - cropped viewport output
  - downsampled output
  - combined crop/grayscale/downsample output suitable for DQN pipelines
- Keep modes explicit and documented so existing users are not surprised.
- Benchmark actual `step + observation consumption` loops, not just raw
  emulator stepping.

## Non-Goals

- Do not change rewards, done semantics, Gymnasium reset/step tuple shape, or
  default render modes.
- Do not introduce heavyweight image-processing dependencies.
- Do not make game-specific preprocessing decisions in `nes-py`; game-specific
  wrappers can build on generic modes later.

## Experiment Rule

Each observation mode is optional. If a mode adds API complexity without a
clear training-loop speedup, document the result and drop that mode. It is
acceptable for this spec to finish with only benchmark documentation if no
generic API is worth keeping.

## Acceptance Criteria

- [ ] Benchmarks measure default step-only, `step + copy`, `step + contiguous`,
  `step + grayscale`, and any new native fast-path modes.
- [ ] Any kept mode has tests for shape, dtype, contiguity where promised,
  buffer lifetime, reset behavior, render behavior, and close behavior.
- [ ] The default `NESEnv.step` and `render('rgb_array')` behavior remains
  backward compatible.
- [ ] Documentation describes intended ML usage and tradeoffs without claiming
  universal speedups.
- [ ] Existing Python environment, wrapper, mapper, and speedtest tests pass.
- [ ] Before/after training-loop-style benchmark output is recorded in a
  developer note or completion log.
- [ ] No generated benchmark output, build artifact, cache, wheel, or virtual
  environment is committed.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
git diff --check
```

If native C++ observation helpers are added, also run the relevant native test
target.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-ml-observation-fast-paths.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 0 -->

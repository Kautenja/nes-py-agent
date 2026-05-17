# Specification: nes-py Background Tile Row Batching

## Problem

The current renderer caches background tile-row and attribute bytes, but still
emits background pixels one at a time inside `PPU::cycle`. For normal gameplay,
background rendering is the dominant cost: synthetic probes showed background
rendering costs far more than render-off stepping, and full background-plus-
sprite rendering remains below the desired `2000` fps target.

The next likely high-yield path is to decode and emit background tile rows in
small batches, while preserving scrolling, palette lookup, mapper hooks, and
sprite compositing.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Depend on the benchmark suite from
  `001-nes-py-ppu-benchmark-suite.md`, or add missing background-specific
  benchmark coverage first.
- Explore an 8-pixel tile-row decode/cache, a scanline segment cache, or a
  shift-register-like local pipeline.
- Keep mapper-observed PPU reads and address sequencing correct. If batching
  would change mapper-visible behavior for hooked mappers, gate it to mappers
  without PPU address/read/write observers.
- Preserve fine X scroll, coarse X wrapping, nametable switching, attribute
  quadrant selection, edge masking, and palette output.

## Non-Goals

- Do not rewrite CPU scheduling.
- Do not change public observation layout or render modes.
- Do not add new mapper implementations.

## Experiment Rule

This is an experiment. If the batch renderer becomes too hard to prove correct,
or if it only moves noise-level benchmark numbers, document the result and
throw out the optimization instead of carrying fragile renderer complexity.

## Acceptance Criteria

- [ ] Tests cover fine X scroll, nametable horizontal wrapping, vertical
  increment behavior, attribute quadrant selection, left-edge background mask,
  and mapper-hook gating.
- [ ] Frame smoke tests continue to pass for mapper 0, mapper 1, mapper 2, and
  mapper 3 representative fixtures where available.
- [ ] Background-only and full-frame ROM benchmarks are recorded before and
  after the change.
- [ ] The optimized path is either mapper-hook safe or disabled for mappers that
  need exact PPU address/read/write observation.
- [ ] Existing Python environment, mapper, speedtest, and native tests pass.
- [ ] Any no-op or abandoned implementation records why it was not kept.
- [ ] No generated benchmark output, profiling dump, build artifact, cache,
  wheel, or virtual environment is committed.

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_mappers
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_TESTS=ON -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_tests nes_emu_benchmarks
build/nes-emu-release/nes_emu_tests
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress
git diff --check
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-background-tile-row-batching.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 0 -->

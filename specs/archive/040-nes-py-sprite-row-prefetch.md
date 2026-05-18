# Specification: nes-py Sprite Row Prefetch

## Problem

Synthetic profiling shows sprite-only rendering is much faster than full
background-plus-sprite rendering, but sprite composition still performs
per-pixel sprite metadata work and CHR reads inside the visible pixel loop.
`PPU::cycle` currently walks scanline sprites for each pixel, recomputes sprite
row addressing, and reads pattern bytes at the point of composition.

Prefetching each visible sprite row once per scanline should reduce repeated
work while preserving sprite priority, sprite-zero hit behavior, flipping, and
mapper-visible PPU read semantics.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Depend on the PPU benchmark suite from
  `001-nes-py-ppu-benchmark-suite.md`, or create the smallest missing benchmark
  coverage needed to measure this change honestly.
- Add a fixed-size per-scanline sprite row cache for up to 8 visible sprites.
- Cache sprite X, attributes, foreground priority, sprite index, decoded row
  bytes, and any other data needed to avoid per-pixel recomputation.
- Preserve mapper PPU read/address side effects. If exact per-pixel CHR read
  timing is required for some mapper class, gate the prefetch path behind
  mapper capability flags.
- Preserve current public observation shape, dtype, and Gymnasium behavior.

## Non-Goals

- Do not rewrite the whole PPU renderer.
- Do not change CPU/PPU frame scheduling.
- Do not add support for new mappers as part of this spec.

## Experiment Rule

This optimization is disposable. If benchmarks show no meaningful improvement,
or if mapper timing/correctness becomes fragile, document the attempted design
and close the spec without keeping the risky prefetch path.

## Acceptance Criteria

- [x] Native PPU or mapper-hook tests cover sprite prefetch behavior for
  horizontal flip, vertical flip, priority, transparent pixels, long sprites if
  currently supported, and sprite-zero hit behavior.
- [x] Tests or benchmark fixtures cover the mapper PPU hook sequence when the
  optimized path is enabled or prove the optimized path is disabled for hooked
  mappers.
- [x] The sprite-heavy benchmark profile shows no meaningful regression and a
  documented improvement if the optimization is kept.
- [x] Full-frame Mario and at least one mapper 1 or mapper 2 ROM profile are
  benchmarked before and after the change.
- [x] Existing Python environment, mapper, and speedtest tests pass.
- [x] No generated benchmark output, build artifacts, caches, wheels, or
  virtual environments are committed.

## Status: COMPLETE

## Verification

Run inside `nes-py`:

```sh
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest nes_py.tests.test_mappers
.venv/bin/python -m unittest nes_py.tests.test_nes_env
.venv/bin/python -m unittest nes_py.tests.test_speedtest
.venv/bin/python -m unittest discover .
cmake -S . -B build/nes-emu-release -DCMAKE_BUILD_TYPE=Release -DNES_EMU_BUILD_BENCHMARKS=ON
cmake --build build/nes-emu-release --config Release --target nes_emu_benchmarks
build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1
.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
git diff --check
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-sprite-row-prefetch.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 1 -->

# Specification: nes-py PPU Addressing and Render Pipeline Optimization

## Status: COMPLETE

## Problem

The PPU and picture-bus path contains both correctness risks and likely performance wins. `PictureBus` branches through raw address ranges instead of normalizing PPU addresses once, which makes nametable and palette mirroring hard to audit. `PPU::get_data` checks the incremented address when deciding whether buffered reads apply. The renderer fetches background tile, pattern, and attribute data per pixel instead of per tile or through a shift-register style pipeline, and sprite bookkeeping uses dynamic vectors for fixed-size OAM data.

This spec targets PPU address correctness and render-path simplification as a prerequisite for mapper work that depends on precise PPU reads, including MMC3 IRQs and MMC2/MMC4 CHR latches.

## Current Findings

- `PictureBus::read` and `write` mask to `$3FFF` and use broad nametable/palette ranges, but still branch on raw mirrored addresses instead of normalizing PPU addresses once.
- `$3000-$3EFF` nametable mirrors are not normalized before selecting a name table.
- Palette mirroring only special-cases `$3F10`, not `$3F14`, `$3F18`, `$3F1C`, or repeated palette mirrors.
- `PPU::get_data` increments `data_address` before deciding whether to use the buffered-read path.
- Background rendering fetches nametable, two pattern bytes, and attribute data per visible pixel.
- OAM and scanline sprite data have fixed maximum sizes but are stored in vectors with resize/push operations.
- PPU reset leaves some observable buffers and latch-like fields easy to miss in deterministic reset tests, such as the read buffer and rendered screen memory.
- Mapper PPU address/read/write hooks from spec 012 now make render-path caching sensitive to the sequence of mapper-visible PPU accesses.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Add picture-bus and PPU register tests before changing address behavior.
- Normalize PPU address decoding for pattern tables, nametables, nametable mirrors, and palettes.
- Fix PPUDATA buffering behavior if tests confirm the current increment-before-check logic is wrong.
- Replace fixed-size PPU memory vectors with fixed-size storage where appropriate.
- Reduce background and sprite render overhead with a measured tile-row cache, shift-register pipeline, or equivalent local simplification.
- Preserve mapper PPU hook behavior from spec 012 when caching or batching picture-bus reads.
- Preserve frame output for existing fixtures except where tests identify a correctness bug.

## Non-Goals

- Do not implement new mappers in this spec.
- Do not attempt a full cycle-accurate PPU rewrite unless the smaller render-path refactor proves insufficient.
- Do not change the public Python observation shape or dtype.

## Acceptance Criteria

- [x] Picture-bus tests cover pattern-table reads/writes, nametable mirroring, four-screen behavior when available, one-screen mapper mirroring, palette mirroring, and `$3FFF` handling.
- [x] `$3000-$3EFF` mirrors normalize to their `$2000-$2EFF` nametable equivalents.
- [x] Palette addresses normalize through `$3F00-$3F1F`, including universal background mirrors at `$3F10`, `$3F14`, `$3F18`, and `$3F1C`.
- [x] PPUDATA buffered reads use the original read address to decide whether the delayed-buffer path applies.
- [x] PPU reset initializes latch-like state and fixed buffers needed for deterministic reset, backup, and render tests.
- [x] PPU fixed-size memory such as OAM, scanline sprite indexes, palette RAM, and nametable RAM uses fixed-size storage unless a vector remains justified.
- [x] Background rendering avoids repeated per-pixel fetches of the same tile-row and attribute data where that can be done without breaking scroll or mapper read side effects.
- [x] Sprite evaluation avoids dynamic allocation or resize/push operations in the per-scanline path.
- [x] Mapper-visible PPU address/read/write side effects from spec 012 preserve their required address sequence and timing after render-path caching.
- [x] Existing frame smoke tests pass for mapper 0 and mapper 1 fixtures, and any changed frame hashes/screenshots are explained by a documented correctness fix.
- [x] Before/after benchmark output covers render-heavy and normal step-heavy profiles.
- [x] No generated screenshots, profiling dumps, build artifacts, wheels, caches, or local virtual environments are committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_nes_env
python -m unittest discover .
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress
```

If native C++ tests are added for picture-bus/PPU internals, run the documented native test command for the active build system.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-ppu-addressing-and-render-pipeline-optimization.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

## Completion Log

Completed in `nes-py` commit `fca0c10` with normalized picture-bus address decoding, fixed-size PPU/PictureBus storage, corrected PPUDATA buffering, render-cache guarded by mapper PPU hook visibility, fixed-size sprite evaluation, native PPU smoke coverage, and benchmark documentation.

Verification used `.venv/bin/python` because `python` is not on PATH in this shell:

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_native_ppu`
- `.venv/bin/python -m unittest nes_py.tests.test_native_cpu_bus`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest nes_py.tests.test_speedtest`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --render-mode rgb_array --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --render-mode rgb_array --json --no-progress`

<!-- NR_OF_TRIES: 1 -->

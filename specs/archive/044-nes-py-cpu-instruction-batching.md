# Specification: nes-py CPU Instruction Batching

## Status: COMPLETE

## Problem

`Emulator::step` currently advances one CPU cycle at a time and calls the PPU
three times per CPU cycle for an entire frame. This is straightforward and has
kept timing behavior understandable, but it forces the frame loop through
roughly 29,780 CPU-cycle iterations and 89,340 PPU-cycle calls per NTSC frame.

Executing one CPU instruction at a time, returning consumed cycles, and
advancing PPU/mapper timing in larger batches may reduce loop overhead enough
to cross the `2000` fps target. This is also the riskiest optimization because
DMA, NMI, IRQ, mapper CPU-cycle hooks, and PPU status timing are sensitive.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Treat this as an experiment after lower-risk PPU and mapper fast paths have
  been measured.
- Add an instruction-level CPU API that can execute one opcode and report the
  consumed CPU cycles, including page-crossing penalties, branches, interrupts,
  and DMA stalls.
- Update or prototype `Emulator::step` to preserve the existing CPU/PPU/mapper
  ordering model as closely as possible.
- Preserve mapper CPU-cycle hooks. If batching cannot preserve a mapper's
  per-cycle behavior, gate batching to mappers that do not observe CPU cycles.
- Preserve NMI/IRQ behavior, OAM DMA cycle penalties, controller reads, and
  save-state determinism.

## Non-Goals

- Do not combine this with PPU renderer rewrites.
- Do not remove the current cycle-by-cycle path until the batched path is
  proven correct.
- Do not enable batching for timing-sensitive mappers without tests.

## Experiment Rule

This optimization is explicitly allowed to fail. If behavior diverges in ways
that are hard to reason about, or benchmarks do not justify the complexity,
keep only the tests/benchmarks and discard the batched execution path.

## Acceptance Criteria

- [x] Native CPU tests cover instruction cycle counts, branch penalties,
  page-cross penalties, stack operations, interrupt entry, DMA cycle skipping,
  and representative addressing modes through the new instruction-level API.
- [x] Frame-level tests compare cycle-by-cycle and batched stepping for
  deterministic ROM fixtures across reset, multiple steps, backup, restore,
  and continuation.
- [x] Mapper CPU-cycle hook behavior is preserved or batching is disabled for
  hooked mappers.
- [x] Public Python behavior remains unchanged for `NESEnv.reset`, `step`,
  `render`, backup, restore, and RAM/controller/screen buffers.
- [x] Benchmarks compare old and new frame stepping for render-off, full-frame
  Mario, Zelda, and at least one mapper 2 or mapper 3 fixture.
- [x] Any abandoned prototype records the correctness or performance reason it
  was thrown out.
- [x] No generated benchmark output, build artifact, cache, wheel, or virtual
  environment is committed.

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
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-cpu-instruction-batching.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 1 -->

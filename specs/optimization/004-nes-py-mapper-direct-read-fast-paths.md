# Specification: nes-py Mapper Direct Read Fast Paths

## Problem

The current CPU and PPU hot paths still read PRG and CHR data through virtual
mapper methods and shared bank-window helpers. That design is clear and safe,
but full-frame rendering performs many CHR reads per frame and CPU execution
performs many PRG reads per frame. Common mappers with simple fixed or
switchable windows may be able to expose direct active-bank pointers for reads
without sacrificing mapper correctness.

This spec explores direct-read fast paths for common mapper windows so PPU and
CPU hot paths spend less time in virtual dispatch, modulo arithmetic, and
generic bank helper logic.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is
  required.
- Start with mappers 0-3 only: NROM, SxROM/MMC1, UxROM, and CNROM.
- Add mapper APIs or cached bus-side state for direct PRG/CHR read windows when
  a mapper can prove the address range is directly backed by stable memory.
- Update direct pointers whenever a mapper bank register changes.
- Preserve CHR RAM writes, PRG RAM routing, bus-conflict behavior, mapper PPU
  hooks, mapper CPU hooks, and nametable mapping behavior.
- Benchmark mapper direct-read stress, background-only rendering, and full ROM
  stepping before and after the change.

## Non-Goals

- Do not optimize complex mappers that are not yet implemented.
- Do not bypass mapper methods for writes unless a later benchmark proves that
  write fast paths matter.
- Do not change cartridge loading or public Python APIs.

## Experiment Rule

This spec may be thrown out. If direct pointers make mapper state harder to
reason about or do not improve measured stepping/rendering, keep the tests or
benchmark coverage and close without the optimization.

## Acceptance Criteria

- [ ] Native mapper tests cover direct-read behavior for NROM, SxROM, UxROM,
  and CNROM, including bank-switching and backup/restore state where relevant.
- [ ] Direct-read state invalidates or updates correctly after mapper writes.
- [ ] Direct reads are disabled or safely bypassed for CHR RAM writes,
  mapper-visible PPU hooks, nametable mapping, expansion routing, and any mapper
  mode where direct memory cannot represent the active mapping.
- [ ] Mapper direct-read and full-frame benchmarks are recorded before and
  after the change.
- [ ] Existing mapper, environment, backup/restore, speedtest, and native tests
  pass.
- [ ] Any rejected direct-read design records why it was not kept.
- [ ] No generated benchmark output, build artifact, cache, wheel, or virtual
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
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-direct-read-fast-paths.md` file.
- Output `DONE` only after all local verification passes and any required
  remote checks are green.

<!-- NR_OF_TRIES: 0 -->

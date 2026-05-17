# Specification: nes-py CPU, Bus Dispatch, and Frame Timing Optimization

## Problem

The native CPU and main-bus path has several obvious sources of overhead and portability risk now that mapper timing hooks have landed. `Emulator::step` runs a fixed `CYCLES_PER_FRAME` loop and calls `cpu.cycle` once per CPU cycle. Most of those calls only decrement `skip_cycles`, while actual opcode execution re-decodes each opcode by trying several helper families. Main-bus I/O register reads and writes go through `unordered_map` lookups and `std::function` callbacks even though the register set is fixed. CPU flags are stored in a bitfield union over a byte, which is implementation-defined and harder to reason about across compilers.

This spec targets the CPU/bus/frame-time hot path as its own measured refactor.

## Current Findings

- `Emulator::step` calls three PPU cycles and one CPU cycle inside a hard-coded frame loop, with optional mapper CPU-cycle hooks and mirroring synchronization in that loop.
- `CPU::cycle` increments `cycles`, pays a skip-cycle branch, then tries `implied`, `branch`, `type1`, `type2`, and `type0` until one accepts the opcode.
- `MainBus::read` and `MainBus::write` use callback maps with `count` plus `at`, producing two hash lookups for fixed I/O registers.
- `CPU_Flags` uses bool bitfields in a union with `NES_Byte`, which depends on compiler bitfield layout.
- Mapper IRQ, CPU-cycle hooks, and DMA behavior are now timing-sensitive after spec 012, so the timebase needs tests before aggressive optimization.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Add focused CPU and bus characterization tests before changing dispatch.
- Benchmark CPU-heavy, bus-heavy, mapper-hook-heavy, and normal Cython `NESEnv.step` frame stepping paths before and after each optimization.
- Replace dynamic fixed-register dispatch with a simpler direct dispatch strategy when benchmarks confirm it is beneficial.
- Consider replacing the per-cycle skip model with an instruction-level execution path that returns consumed CPU cycles, while preserving PPU, DMA, NMI, IRQ, mapper CPU-cycle hooks, and mapper mirroring synchronization.
- Replace implementation-defined CPU flag storage with portable byte-mask helpers if tests and benchmarks support the change.
- Keep public Python behavior compatible.

## Non-Goals

- Do not implement new mappers in this spec.
- Do not rewrite the CPU core around a third-party emulator.
- Do not change visible emulator timing without characterization tests that justify the correction.

## Acceptance Criteria

- [ ] CPU characterization tests cover reset vectors, stack pushes/pops, representative addressing modes, branch page crossing, interrupt entry, DMA cycle skipping, and flag behavior.
- [ ] Main-bus tests cover RAM mirroring, PPU register mirroring, controller reads, OAM DMA page access, expansion-area delegation or default behavior, PRG RAM access, and mapper PRG reads/writes.
- [ ] A benchmark profile isolates CPU dispatch cost, main-bus I/O dispatch cost, mapper-hook overhead for hooked versus unhooked mapper paths, and normal `NESEnv.step` throughput.
- [ ] Fixed I/O register dispatch no longer uses `unordered_map` and `std::function` in the hot path unless benchmarks prove the old approach is competitive.
- [ ] Any replacement for `CPU::cycle` preserves CPU/PPU ordering, DMA stall behavior, NMI delivery, IRQ delivery, and current mapper per-cycle hooks.
- [ ] If an instruction-level CPU API is introduced, it returns consumed cycles and has tests for instructions with base cycles plus page-crossing cycles.
- [ ] `Emulator::step` either remains cycle-count based with documented timing tests or advances until a PPU frame-complete signal with tests for even/odd frame behavior, mapper CPU-cycle hooks, and mirroring synchronization.
- [ ] CPU flags no longer rely on implementation-defined bitfield layout, or the completion log documents why replacing them was deferred.
- [ ] Current ROM, mapper, environment, backup/restore, and speedtest tests pass.
- [ ] Before/after benchmark output is included in the completion log, and any regression is investigated or explicitly accepted for a correctness reason.
- [ ] No generated profiling dumps, build artifacts, wheels, caches, or local virtual environments are committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_rom
python -m unittest nes_py.tests.test_mappers
python -m unittest nes_py.tests.test_nes_env
python -m unittest discover .
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress
```

If native C++ tests are added for CPU and bus internals, run the documented native test command for the active build system.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-cpu-bus-dispatch-and-frame-timing-optimization.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

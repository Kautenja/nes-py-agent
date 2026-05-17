# Specification: nes-py Native Hot Path Optimization Benchmarks

## Problem

The native emulator hot paths were written for clarity and small mapper coverage. Specs 012 and 015 have now added mapper timing hooks and a Cython binding layer, and the mapper queue will continue to increase dispatch, timing, and memory-map complexity. Current performance needs to be measured and improved deliberately. Optimizations should be benchmark-driven and must not trade away deterministic emulator behavior.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Use the benchmark baseline from spec 010, the packaged benchmark CLI/API from spec 006, and the current post-spec-012/post-spec-015 branch state.
- Profile native hot paths before changing them.
- Optimize only code paths where profiling or benchmarks show meaningful cost.
- Keep behavior covered by mapper, environment, and ROM tests.
- Treat this as the broad benchmark/profiling and non-overlapping optimization track. If specs 017 and 018 are still incomplete, do not consume their full CPU/bus or PPU/render refactors here; establish current baselines, improve benchmark coverage, and only land additional small measured optimizations outside those targeted specs.

## Candidate Areas

Investigate these areas and optimize only when evidence supports it:

- `MainBus` I/O register dispatch currently uses unordered maps and `std::function` callbacks on a hot path.
- `CPU::cycle` pays a skip-cycle branch on every CPU cycle and re-decodes every opcode through several helper probes; a measured instruction-level execution path may reduce overhead.
- `Emulator::step` uses a hard-coded CPU-cycle count per frame; a PPU frame-completion loop may improve correctness and simplify DMA/NMI/IRQ timing work.
- `CPU_Flags` uses a bitfield union over a byte, which is implementation-defined and can be replaced by portable bit masks/accessors if benchmarks and tests support it.
- Mapper timing hooks from spec 012 add CPU-cycle and PPU hook checks; profile hooked and unhooked mapper paths and mirroring synchronization overhead.
- `PictureBus` nametable and palette address handling repeats branch-heavy logic.
- PPU address normalization has correctness and simplification risks around `$3000-$3EFF` nametable mirrors, palette mirrors, and `$3FFF` coverage; fixing this may also remove branches.
- PPU rendering repeatedly performs per-pixel bus reads and sprite scans with vector bookkeeping.
- Fixed-size memory such as CPU RAM, palette RAM, nametable RAM, sprite memory, and controller bytes could use `std::array` where ownership is fixed.
- Mapper bank reads can use precomputed bank base pointers or helper windows after the mapper API refactor.
- The Cython step path now writes the controller action natively and releases the GIL around `Emulator::step`; profile the remaining Python/native boundary, render access, and backup/restore overhead before changing it.
- The native screen buffer is 32-bit while the Cython API exposes a no-copy RGB24 view with a negative channel stride on little-endian systems; measure whether a different native/export layout is worth the compatibility risk.
- Logging and error reporting should remain out of hot paths in release builds.

## Non-Goals

- Do not rewrite the emulator around a different core.
- Do not sacrifice mapper correctness for speed.
- Do not claim a speedup without benchmark evidence.
- Do not make benchmark numbers machine-specific pass/fail thresholds.

## Acceptance Criteria

- [ ] A benchmark report captures before/after results for at least reset-heavy, step-heavy, render-heavy, and backup/restore-heavy profiles.
- [ ] Profiling evidence is recorded in the completion log or a linked developer note for every non-trivial optimization.
- [ ] At least one measured hot path is optimized or the spec documents that profiling found no safe optimization worth landing.
- [ ] Behavior tests for ROM parsing, current mappers, environment stepping, rendering, and backup/restore pass after each optimization set.
- [ ] Mapper timing and IRQ hooks from spec 012 are included in the benchmark profile.
- [ ] CPU/bus/frame-timing benchmarks from spec 017 are included if that spec has landed.
- [ ] PPU address/rendering benchmarks from spec 018 are included if that spec has landed.
- [ ] Current Cython binding benchmarks from spec 015 are included, including frame stepping, render/view access, and backup/restore where relevant.
- [ ] Optimizations prefer fixed-size arrays, direct dispatch, precomputed windows, and small local helpers over broad rewrites.
- [ ] Any measurable regression is either fixed or explicitly accepted with a correctness reason and follow-up spec.
- [ ] Benchmark code remains informational and portable; CI does not fail because a runner is slower than a developer machine.
- [ ] No generated profiling dumps, caches, build artifacts, wheels, or local virtual environments are committed.
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
python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 1000 --warmup-steps 100 --backup-interval 200 --restore-interval 350 --json --no-progress
```

If profiling tools are platform-specific, document the platform and exact command in the completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-native-hot-path-optimization-benchmarks.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

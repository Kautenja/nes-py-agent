# History

Append one-line summaries here after each completed Ralph spec. Put longer notes in `history/YYYY-MM-DD--spec-name.md`.

2026-05-17: Completed nes-py GitHub Actions CI migration with Python 3.13 packaging builds across Linux, Windows, and macOS runner matrix.
2026-05-17: Completed nes-py backup/restore cleanup by replacing root scripts with regression coverage and a packaged speedtest CLI.
2026-05-17: Completed gym-super-mario-bros GitHub Actions CI migration with Python 3.13 matrix builds and tag-gated release artifacts.
2026-05-17: Completed gym-zelda-1 GitHub Actions CI migration with Python 3.13 matrix builds and tag-gated release artifacts.
2026-05-17: Completed gym-tetris GitHub Actions CI migration with Python 3.13 matrix builds and tag-gated release artifacts.
2026-05-17: Completed nes-py native mapper characterization with synthetic ROM coverage, mapper-state backup/restore, and current-mapper benchmark profiling.
2026-05-17: Completed nes-py cartridge header and memory map metadata with aligned Python/native parsing, NES 2.0 fields, RAM separation, and synthetic edge coverage.
2026-05-17: Completed nes-py mapper API lifecycle and timing hooks with RAII mapper ownership, state-only snapshots, IRQ/PPU/expansion/PRG-RAM/nametable hooks, and regression coverage.
2026-05-17: Completed nes-py mapper bank helpers and current mapper cleanup with shared PRG/CHR windows, CHR RAM ownership, MMC1 fixes, safe bank masking, and benchmark documentation.
2026-05-17: Completed nes-py pyproject build modernization with canonical PEP 621 metadata, deterministic native source discovery, packaged C++ sources/headers, and verified install/build workflows.
2026-05-17: Completed nes-py Cython binding migration with direct Emulator ownership, no-copy native buffers, GIL-released frame stepping, ctypes loader removal, and verified package builds.
2026-05-17: Completed nes-py native hot-path benchmark pass with main-bus direct device dispatch, fixed RAM storage, portable mapper hook profiling, and before/after benchmark documentation.
2026-05-17: Completed nes-py CPU, bus dispatch, and frame timing optimization with portable CPU flags, opcode-family dispatch, native CPU/main-bus characterization, and hot-path benchmark profiling.
2026-05-17: Completed nes-py PPU addressing and render pipeline optimization with normalized picture-bus mirroring, fixed-size PPU storage, corrected PPUDATA buffering, mapper-safe tile-row caching, and native smoke coverage.
2026-05-17: Completed gym-super-mario-bros pyproject distribution modernization with canonical PEP 621 metadata, preserved ROM package data, console script metadata, and verified install/build workflows.
2026-05-17: Completed gym-zelda-1 pyproject distribution modernization with canonical PEP 621 metadata, preserved ROM package data, console script metadata, and verified install/build workflows.
2026-05-17: Completed gym-tetris pyproject distribution modernization with canonical PEP 621 metadata, preserved ROM package data, console script metadata, and verified install/build workflows.
2026-05-17: Completed nes-py native emulator root layout migration with the C++ tree moved to nes_emu, scoped includes, updated CMake/Cython packaging, and verified install/build workflows.
2026-05-17: Completed nes-py mapper test package refactor with per-mapper modules, shared mapper helpers, separated registry/lifecycle smoke coverage, and deterministic unittest discovery.
2026-05-17: Completed nes-py native test and benchmark API separation with opt-in Catch2 targets, Cython smoke/benchmark wrapper removal, public Python benchmark cleanup, and verified native/package builds.
2026-05-17: Completed nes-py Python application test coverage review with public ROM/env/speedtest coverage, native cartridge Catch2 coverage, and private native-helper cleanup.
2026-05-17: Completed nes-py Gymnasium API migration with Gymnasium dependency metadata, v0.26 reset/step/render contracts, JoypadSpace forwarding, CLI/helper updates, and focused API coverage.
2026-05-17: Completed gym-super-mario-bros Gymnasium API migration with modern reset/step/render contracts, random-stage seeding, Gymnasium registration, CLI/docs updates, and focused wrapper coverage.
2026-05-17: Completed gym-tetris Gymnasium API migration with modern reset/step/render contracts, preserved reward modes and info fields, Gymnasium registration, CLI/docs updates, and focused wrapper coverage.
2026-05-17: Completed gym-zelda-1 Gymnasium API migration with modern reset/step/render contracts, preserved placeholder rewards and info fields, Gymnasium registration, CLI/docs updates, and focused wrapper coverage.
2026-05-17: Completed nes-py mapper 001 MMC1/SxROM representative coverage with Zelda application workflow tests and emulator save-state native coverage.
2026-05-17: Completed nes-py mapper 002 UxROM representative coverage with Mega Man application workflow tests and emulator save-state PRG-bank/CHR-RAM coverage.
2026-05-17: Completed nes-py mapper 000 NROM representative coverage with Super Mario Bros. application workflow tests and emulator save-state PRG-RAM coverage.
2026-05-17: Completed nes-py mapper 003 CNROM representative coverage with Adventure Island application workflow tests and emulator save-state CHR-bank coverage.
2026-05-17: Completed nes-py mapper 007 AxROM implementation with 32 KiB PRG banking, CHR RAM, one-screen mirroring, NES 2.0 bus-conflict coverage, and Battletoads application workflow tests.

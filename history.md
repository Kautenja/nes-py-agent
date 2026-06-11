# History

Append one-line summaries here after each completed automation item. Put longer
notes in `history/YYYY-MM-DD--name.md`, and keep release-facing rollups in
`CHANGELOG.md`.

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
2026-05-17: Completed nes-py mapper 004 MMC3 implementation with 8 KiB PRG banking, 1/2 KiB CHR banking, mirroring, PRG RAM protection, filtered A12 IRQs, and SMB3 public fixture coverage.
2026-05-17: Completed nes-py mapper 005 MMC5 first-pass implementation with PRG/CHR banking, ExRAM/nametable/fill mapping, IRQ/multiplier support, and Castlevania III public smoke coverage.
2026-05-17: Completed nes-py mapper 007 AxROM implementation with 32 KiB PRG banking, CHR RAM, one-screen mirroring, NES 2.0 bus-conflict coverage, and Battletoads application workflow tests.
2026-05-17: Completed nes-py mapper 009 MMC2 support with PRG banking, PPU-read CHR latches, mirroring, native save-state coverage, and Punch-Out application smoke coverage.
2026-05-17: Completed nes-py mapper 069 Sunsoft FME-7 support with native command/banking/IRQ coverage and Batman Return of the Joker public smoke coverage.
2026-05-17: Completed nes-py PPU benchmark suite with deterministic native render-mode, CHR-read stress, representative ROM frame profiles, and baseline speedtest documentation.
2026-05-17: Completed wrapper Python and CI dependency parity across Mario, Tetris, and Zelda with Python 3.13/3.14 matrices, shared nes-py bootstrap policy, and green remote CI.
2026-05-17: Completed nes-py sprite row prefetch with mapper-gated scanline sprite row caching, native sprite behavior coverage, and benchmarked sprite-heavy improvement.
2026-05-17: Completed nes-py background tile row batching with mapper-gated bitplane decode caching, focused PPU scroll/mask/hook coverage, and benchmarked background/full-frame samples.
2026-05-17: Completed wrapper CLI playback parity across Mario, Tetris, and Zelda with headless random playback, first-reset seeding, action-space selection, README examples, and focused CLI coverage.
2026-05-17: Completed wrapper registration and Gymnasium policy parity across Mario, Tetris, and Zelda with shared registration-module layout, explicit env-checker/truncation policy coverage, and representative rgb_array smoke checks.
2026-05-17: Completed wrapper documentation and metadata parity across Mario, Tetris, and Zelda with CI Python version docs, CLI/Gymnasium README cleanup, modernized proprietary license metadata, and successful wrapper package builds/tests.
2026-05-17: Completed nes-py mapper direct-read fast paths with cached PRG/CHR bus pages for mappers 0-3, direct-read regression coverage, and before/after benchmark documentation.
2026-05-17: Completed nes-py ML observation fast paths with reusable native contiguous RGB/grayscale helpers, observation benchmark profiling, compatibility coverage, and conservative usage documentation.
2026-05-17: Completed nes-py CPU instruction batching with an instruction-level CPU API, mapper-hook-gated frame stepping, deterministic old/new frame coverage, and benchmark comparisons.
2026-05-17: Completed Zelda RL contract parity with `Zelda1-v0` documented and tested as a zero-reward navigation/state-inspection sandbox with non-terminal death recovery.
2026-05-17: Completed nes-py vectorized native emulator prototype with same-ROM vector ownership, batched reset/step/observation/RAM/snapshot APIs, determinism coverage, and benchmarked no-regression serial vector results.
2026-05-17: Completed nes-py native batch RAM info reads with generic scalar/vector descriptors, reusable uint32 outputs, validation coverage, and wrapper-style profiling that kept the helper as a shared primitive.
2026-05-17: Completed nes-py vector throughput instrumentation with repeated vector speedtest profiles, timing breakdowns, CPU-affinity experiment labels, and documented instrumentation overhead.
2026-05-17: Completed nes-py explicit state snapshot API with opaque mapper-aware snapshot ownership, scalar/vector restore paths, mapper-wide continuation coverage, and latency benchmarks.
2026-06-09: Completed Playing Mario modern dependency baseline with pyproject metadata, a lightweight `mario_rl` package, modern Gymnasium/PyTorch/Lightning dependencies, editable submodule install docs, and focused dependency/layout tests.
2026-06-09: Completed Playing Mario Gymnasium environment pipeline with a `mario_rl.envs` factory, JoypadSpace action sets, channel-first preprocessing wrappers, deterministic Mario smoke tests, and optional OpenCV video recording.
2026-06-09: Completed Playing Mario config CLI project layout with typed dataclass configs, packaged YAML discovery, import-safe train/play/random entrypoints, TISV-style `main.sh` routing, and focused config/entrypoint tests.
2026-06-09: Completed Playing Mario PyTorch DQN core with native DQN/DuelingDQN modules, selected-action TD loss helpers, uniform replay batches, epsilon schedules, and focused PyTorch/replay coverage.
2026-06-09: Completed Playing Mario Lightning training and device smoke with a Lightning DQN module, bounded replay-driven smoke training, checkpoint evaluation, CPU/MPS verification, and artifact documentation.
2026-06-10: Completed Playing Mario MacBook trainability guardrails with a documented `verify-macbook` gate, bounded real-environment CPU/MPS mini train/eval runs, artifact checks, warning budgets, and benchmark summaries.
2026-06-10: Completed Playing Mario task conditioning with a deterministic MarioTask feature encoder, optional DQN/DuelingDQN task inputs, replay task feature batches, train/eval wiring, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario task-suite curriculum with metadata-only TaskSuite sampling, balanced family weights, episode-boundary task switching, SMB3 catalog reporting, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario universal action-space sizing with native NES 256-action support, right/right_only aliasing, automatic model-head resolution, mismatch validation, action metadata artifacts, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario reward transform pipeline with explicit env/sign/unclipped/clipped/component-weight modes, replay reward diagnostics, frame-skip diagnostic aggregation, artifact metadata, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario task metrics with typed step/episode accumulation, global/per-family/per-task summaries, structured train/eval JSON artifacts, Lightning scalar logs, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario recurrent actor-critic training with a task-conditioned GRU policy/value model, rollout/GAE storage, clipped PPO optimization, algorithm-selectable train CLI, fake-env coverage, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario evaluation matrix with filtered task selection, deterministic seed expansion, SMB3 catalog metadata, per-task JSON/CSV artifacts, fake-env coverage, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario auxiliary losses with optional PPO heads for progress, clear/death, transformed reward, and game-family targets, explicit missing-value masks, durable loss artifacts, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario vectorized PPO rollouts with two-environment fast-dev training, per-slot recurrent state resets, multi-active task metrics, PPO checkpoint play support, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario adaptive curriculum with frontier-based task progression, serializable mastery state, Lost Levels gating, curriculum artifacts, checkpoint/artifact resume coverage, and CPU/MPS gate verification.
2026-06-10: Completed Playing Mario emulator snapshot curriculum with process-local opaque snapshots, compatibility metadata, DQN/PPO reset sampling, snapshot-start metrics, metadata-only artifacts, and CPU/MPS gate verification.
2026-06-11: Completed Playing Mario pixel fidelity with explicit grayscale/RGB observation profiles, automatic replay/model shape resolution, RGB PPO fast-dev training, artifact metadata, and CPU/MPS gate verification.
2026-06-11: Completed Playing Mario curiosity exploration with disabled-by-default pixel-only PPO RND, separate intrinsic reward metrics, a real RND smoke config, and CPU/MPS gate verification.
2026-06-11: Completed Playing Mario prioritized replay with opt-in proportional DQN sampling, importance-weighted TD loss, deterministic priority updates, replay artifacts/checkpoint metadata, and CPU/MPS gate verification.
2026-06-11: Completed Playing Mario action abstractions with opt-in Joypad macro actions, macro-aware model sizing/artifacts, real macro PPO smoke training, and CPU/MPS gate verification.

# Changelog

## 2026-06 Playing Mario Modernization

- Started the Mario learner modernization queue by adding PEP 621 package
  metadata, a lightweight `mario_rl` namespace, modern Gymnasium/PyTorch/
  Lightning dependency floors, and documented editable install paths for the
  umbrella `nes-py` and `gym-super-mario-bros` submodules.
- Added dependency and package-layout unittest coverage so the modern package
  imports without TensorFlow or Keras, while legacy Keras model tests are kept
  skipped until the PyTorch port owns them.
- Added `mario_rl.envs` with a Gymnasium Mario factory, JoypadSpace action-set
  selection, channel-first downsampling/frame-stack preprocessing, reward
  accounting, record-statistics integration, optional OpenCV MP4 recording, and
  deterministic fake-env plus real Mario smoke coverage.
- Added `mario_rl.config` with a single typed dataclass config tree, packaged
  YAML configs, nested CLI overrides, import-safe train/play/random entrypoints,
  and `main.sh` routes for config discovery, training, play, random rollout, and
  unittest workflows.
- Added the native PyTorch DQN core with `DQN` and `DuelingDQN` modules,
  selected-action SmoothL1 TD-loss helpers, Double-DQN target selection, typed
  uniform replay batches, seeded epsilon-greedy scheduling, and focused CPU
  optimizer-step coverage.
- Added the Lightning DQN training and evaluation path with manual
  replay-driven optimization, checkpointed schedule/counter state, resolved
  config/log/checkpoint/metrics artifacts, CPU and MPS smoke verification, and
  README commands for CPU, MPS, CUDA, and checkpoint play.

## 2026-05 Coordinated Release Preparation

This entry consolidates the completed development archive that previously lived
under `specs/archive/`. Keep future completed-work context here, in
`history.md`, and in focused files under `history/` so `specs/` stays a live
planning queue instead of a long-term storage area.

### Release Train

- Prepared `nes-py` `9.0.0` as the emulator foundation for the next wrapper
  releases.
- Prepared `gym-super-mario-bros` `8.0.0`, `gym-tetris` `4.0.0`, and
  `gym-zelda-1` `0.3.0` for Gymnasium-era usage.
- Standardized package metadata, editable installs, GitHub Actions, and
  tag-gated publishing flows across the maintained projects.
- Raised the maintained Python baseline to the current release line and aligned
  runtime dependencies on Gymnasium.

### `nes-py`

- Modernized packaging with PEP 621 metadata, deterministic native source
  discovery, packaged C++ sources and headers, and verified source/wheel builds.
- Migrated the native binding layer to Cython-owned emulator instances with
  no-copy buffers, GIL-released frame stepping, and removal of the legacy ctypes
  loader.
- Moved the native emulator tree into `nes_emu`, tightened include boundaries,
  and separated native tests, benchmarks, and Python application coverage.
- Added cartridge header and memory-map metadata, NES 2.0 field support, RAM
  separation, and aligned Python/native parsing coverage.
- Reworked mapper ownership, lifecycle hooks, IRQ/PPU/expansion hooks,
  state-only snapshots, bank helpers, and CHR RAM handling.
- Added or hardened mapper coverage for NROM, MMC1/SxROM, UxROM, CNROM, MMC3,
  MMC5, AxROM, MMC2, and Sunsoft FME-7.
- Added direct-read mapper fast paths, reusable observation helpers, native
  batch RAM reads, an explicit state snapshot API, and the prototype
  `VectorNESEmulator`.
- Improved CPU, bus dispatch, frame timing, PPU addressing, sprite prefetch,
  background tile batching, and instruction batching with focused regression
  coverage and benchmark notes.
- Added packaged speedtest flows, native mapper profiling, PPU benchmark
  profiles, vector throughput instrumentation, and public application-level
  smoke coverage.

### Wrappers

- Migrated Mario, Tetris, and Zelda environments to Gymnasium reset, step, and
  render contracts while preserving game-specific reward, termination, and info
  behavior.
- Moved wrappers to modern `pyproject.toml` metadata while preserving ROM
  package data, console scripts, license metadata, and documented install paths.
- Aligned wrapper CI, dependency bootstrap policy, CLI playback behavior,
  registration modules, env-checker policy, truncation policy, and README
  examples.
- Documented `Zelda1-v0` as a zero-reward navigation and state-inspection
  sandbox with non-terminal death recovery, leaving future reward design for a
  stabilization pass.

### Archive Notes

- `history.md` keeps the one-line chronological record for each completed work
  item.
- `completion_log/` keeps verification notes and pushed commit references.
- `specs/archive/` is now a lightweight pointer instead of a pile of completed
  task bodies.

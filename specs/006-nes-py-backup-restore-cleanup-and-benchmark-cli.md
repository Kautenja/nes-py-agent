# Specification: nes-py Backup/Restore Cleanup and Benchmark CLI

## Problem

`nes-py/backup_restore.py` and `nes-py/speedtest.py` are root-level ad hoc scripts that were kept around after old debugging and performance work. `backup_restore.py` was introduced alongside a C++ backup/restore implementation change and behaves like a manual stress test, but the behavior it was protecting is only partly captured by the current unit test. `speedtest.py` came from the backend performance comparison around the `nes-py` 3.0.0 work and is useful, but it is not packaged as a reusable benchmark tool or API.

The cleanup should preserve the value of both scripts: turn the backup/restore script into focused regression coverage for the original graphics/save-state bug, and move speed measurement into a package-supported benchmark module with a command line entry point such as `python -m nes_py.speedtest`.

## Issue Context

- `Kautenja/gym-super-mario-bros#49` reported reset-driven graphics corruption where backgrounds failed while sprites continued working. The proposed fix was a `nes-py` save/restore state feature, and the issue was closed after backup/restore support landed.
- `Kautenja/gym-super-mario-bros#72` reported a later graphical glitch after many resets, with a reproducible seeded policy and concerns that the rendered frame and returned observation might be corrupted after repeated resets.
- `Kautenja/nes-py#36` tracked the underlying emulator issue as "Graphical Glitch After backup" and states the expected behavior: the emulator should behave the same after many resets and restore perfectly to its frozen point in time.
- The `speedtest.py` script appears in the issue discussion as the quick throughput comparison that measured the backend update from roughly 456 to 537 iterations per second.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Remove or replace the root-level `nes-py/backup_restore.py` script with automated tests that exercise the original save-state regression.
- Remove or replace the root-level `nes-py/speedtest.py` script with a packaged benchmark module and CLI.
- Keep backup/restore semantics private unless the implementation deliberately introduces a public state API. If a public API is introduced, document and test it explicitly.
- Preserve emulator behavior, observation frames, RAM layout, reward calculations, render output, and Gym/Gymnasium API compatibility expected by the active branch at implementation time.
- Do not add ROM assets, redistribute external game assets, or make benchmark results part of pass/fail correctness thresholds.

## Benchmark API Direction

Provide a reusable benchmark API under the `nes_py` package, for example `nes_py.speedtest`, with a command that can be run as:

```sh
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 5000
```

The exact API shape may follow the codebase's style, but it should expose structured inputs and outputs rather than burying the benchmark in top-level script globals. A good target is:

- A config object or keyword-based function for ROM path, step count, warmup steps, seed, action policy, render mode, progress display, backup interval, restore interval, and output format.
- A result object or dictionary with total steps, resets, elapsed seconds, steps per second, frames per second if different, and any backup/restore stress settings used.
- A CLI that can print human-readable results by default and machine-readable JSON when requested.
- A small programmatic API that downstream wrappers can import without spawning a subprocess.

Interpret any old reference to `ney_py.speedtest` as the package name typo `nes_py.speedtest`.

## Acceptance Criteria

- [ ] `nes-py/backup_restore.py` is removed from the repository root.
- [ ] The behavior that justified `backup_restore.py` is represented by automated tests rather than a manual script.
- [ ] Backup/restore tests cover more than the immediate post-restore screen equality check already present in `nes_py/tests/test_nes_env.py`.
- [ ] A deterministic regression test advances to a backup point, records screen and RAM, mutates emulator state through additional steps, restores, and verifies that screen and RAM return to the recorded backup state.
- [ ] A deterministic continuation test restores from a backup and then runs a fixed action sequence, verifying that observations, rewards, done/termination flags, and info dictionaries match the same sequence from the original backed-up state.
- [ ] A stress test performs repeated backup/restore/reset cycles without human rendering and verifies that frames remain valid `uint8` arrays with the expected shape and that no crash, hang, or corrupted observation occurs.
- [ ] The stress test captures the intent of `gym-super-mario-bros#49`, `gym-super-mario-bros#72`, and `nes-py#36`: repeated reset/restore behavior must not corrupt background graphics, returned observations, or emulator state.
- [ ] Any modulo-based backup/restore loop translated from `backup_restore.py` uses explicit interval semantics, and the implementation documents whether the old script's truthy modulo behavior was preserved or corrected.
- [ ] `nes-py/speedtest.py` is removed from the repository root.
- [ ] A packaged benchmark module exists under `nes_py`, runnable with `python -m nes_py.speedtest` or an equivalent package module path documented in the spec completion log.
- [ ] The benchmark module exposes a programmatic API that can be imported and called from tests or downstream packages.
- [ ] The benchmark CLI accepts at least `--rom`, `--steps`, `--seed`, `--warmup-steps`, `--json`, `--no-progress`, `--backup-interval`, and `--restore-interval`.
- [ ] The benchmark closes environments reliably on normal exit and on interruption.
- [ ] The benchmark supports the active reset/step API on the branch. If the Gymnasium migration has landed, it handles `(observation, info)` resets and five-value step results; otherwise it remains compatible with the current legacy Gym tuple contract.
- [ ] The benchmark API and CLI are covered by focused tests that run a tiny benchmark against the existing test ROM without asserting machine-specific throughput.
- [ ] Documentation or README developer notes mention the benchmark command and clarify that benchmark numbers are informational, not correctness criteria.
- [ ] No root-level one-off emulator scripts remain unless they are intentionally documented developer tools.
- [ ] No generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, or local virtual environments are committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused local checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_nes_env
python -m unittest discover .
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --seed 1 --no-progress
python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 25 --warmup-steps 5 --seed 1 --backup-interval 12 --restore-interval 27 --json --no-progress
```

If the active branch has already migrated to Gymnasium, also run the Gymnasium-focused checks from the Gymnasium migration spec after updating the benchmark and backup/restore tests.

Benchmark verification should assert command success, structured output shape, and sane positive timing fields. It must not require a specific steps-per-second value because that will vary by machine, compiler, and CI runner.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-backup-restore-cleanup-and-benchmark-cli.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

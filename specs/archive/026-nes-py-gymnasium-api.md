# Specification: nes-py Gymnasium API Migration

## Status: COMPLETE

## Problem

`nes-py` exposes the old OpenAI Gym API. Environments currently import `gym`, use `Env.seed()`, return only an observation from `reset()`, return `(observation, reward, done, info)` from `step()`, and select render mode through `render(mode=...)`. Modern Gym-compatible reinforcement learning tooling expects the Gymnasium/v0.26+ contract: `reset()` returns `(observation, info)`, `step()` returns `(observation, reward, terminated, truncated, info)`, render mode is selected when the environment is constructed, and seeding happens through `reset(seed=...)`.

`nes-py` is the base environment layer for the game-specific submodules, so this migration must land before the wrapper repositories can be updated cleanly.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Replace runtime use of the legacy `gym` package with Gymnasium.
- Update `NESEnv`, wrappers, tests, console helpers, examples, package metadata, and documentation to the Gymnasium API.
- Preserve emulator behavior, memory layout, reward calculations, backup/restore behavior, action meanings, and observation data.
- Do not add ROM assets, redistribute external assets, or change emulator determinism except where required to use Gymnasium seeding correctly.
- Do not migrate game-specific environment logic in this spec; that belongs to the dependent wrapper specs.

## Migration Target

Use the current Gymnasium API at implementation time. Reference the official Gymnasium migration guide: https://gymnasium.farama.org/main/introduction/migration_guide/

As of 2026-05-17, the relevant migration points are:

- `import gymnasium as gym` replaces `import gym`.
- `Env.reset(self, *, seed=None, options=None)` returns `(observation, info)`.
- `Env.step(action)` returns `(observation, reward, terminated, truncated, info)`.
- `Env.seed()` is removed from the supported API; seeding is done through `reset(seed=...)`.
- Render mode is fixed at construction, for example `gym.make(id, render_mode="human")`, and `render()` uses `self.render_mode`.
- `metadata` uses keys such as `render_modes` and `render_fps`.

## Acceptance Criteria

- [ ] `nes-py` depends on Gymnasium instead of legacy `gym`; direct imports of the legacy `gym` package are removed from package code, tests, examples, and docs.
- [ ] `NESEnv` subclasses `gymnasium.Env` and has a Gymnasium-compatible constructor that accepts `render_mode=None`.
- [ ] `NESEnv.metadata` uses Gymnasium render metadata keys and exposes the supported modes `human` and `rgb_array`.
- [ ] `NESEnv.reset()` has the Gymnasium signature, initializes or updates the Gymnasium RNG through the supported seeding path, preserves existing emulator reset/restore behavior, and returns `(self.screen, info)`.
- [ ] `NESEnv.step()` returns `(self.screen, reward, terminated, truncated, info)`.
- [ ] The old `_get_done()` subclass hook is migrated to a Gymnasium-appropriate termination hook, or is kept only as a documented compatibility bridge while the returned API uses `terminated` and `truncated`.
- [ ] `NESEnv` never reports truncation for its own game logic unless a concrete truncation condition is implemented and tested; otherwise truncation is left to Gymnasium wrappers such as `TimeLimit`.
- [ ] The environment cannot be stepped after `terminated or truncated` until reset, and tests cover this guard with the new tuple contract.
- [ ] `NESEnv.render()` uses `self.render_mode` and takes no required mode argument in supported code paths.
- [ ] `rgb_array` rendering returns the current NES screen array without opening a viewer.
- [ ] `human` rendering opens and reuses the existing image viewer behavior without changing frame contents.
- [ ] `JoypadSpace.reset()` forwards `seed` and `options`, returns the Gymnasium reset tuple, and no longer drops reset metadata.
- [ ] `JoypadSpace.step()` preserves the discrete-to-byte action mapping and forwards the Gymnasium five-value step tuple.
- [ ] `play_human`, `play_random`, `speedtest.py`, `scripts/run.py`, `backup_restore.py`, README examples, and tests use `reset(seed=...)`, `terminated`, `truncated`, and `done = terminated or truncated` where a loop still needs a combined episode flag.
- [ ] No supported documentation or test tells users to call `env.seed(...)`.
- [ ] If a deprecated `seed()` shim remains for downstream compatibility, it is clearly marked as deprecated, delegates to the same RNG state used by `reset(seed=...)`, and is not used by `nes-py` tests or docs.
- [ ] Package metadata reflects the new Gymnasium dependency and no longer advertises unsupported Python versions unless those versions are still tested.
- [ ] A breaking-change version bump is applied if the project version is updated as part of this migration.
- [ ] Existing emulator tests are updated for the new API without weakening their behavioral assertions.
- [ ] New focused tests cover reset tuple shape, step tuple shape, render-mode behavior, seeding determinism, and `JoypadSpace` forwarding.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd nes-py
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install build
python -m unittest discover .
python -m build
```

Run a focused Gymnasium API smoke check after installation:

```sh
cd nes-py
python -m unittest nes_py.tests.test_nes_env nes_py.tests.test_multiple_makes
```

If `gymnasium.utils.env_checker.check_env` can run against an available test ROM without adding new assets, add or run that check. If it cannot run because the repository intentionally does not ship a generic test ROM, document that limitation in the completion log and cover the API contract with unit tests instead.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-gymnasium-api.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

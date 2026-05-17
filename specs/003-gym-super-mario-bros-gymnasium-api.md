# Specification: gym-super-mario-bros Gymnasium API Migration

## Problem

`gym-super-mario-bros` still presents old OpenAI Gym examples and runtime behavior. It imports `gym`, registers environments through the legacy package, uses old reset and step tuple shapes in tests and docs, and contains `SuperMarioBrosRandomStagesEnv`, a direct `gym.Env` subclass that still implements `seed()` and `reset(..., return_info=None)`.

After `nes-py` migrates to Gymnasium, this wrapper must expose the same modern API while preserving the existing Mario environment IDs, ROM modes, rewards, random-stage behavior, and action spaces.

## Scope

- Work inside the `gym-super-mario-bros` submodule unless an umbrella gitlink update is required after committing the submodule.
- Start this spec only after `specs/002-nes-py-gymnasium-api.md` is complete and the wrapper can depend on a pushed `nes-py` commit with the new API.
- Replace runtime use of legacy `gym` with Gymnasium.
- Update registration, `SuperMarioBrosEnv`, `SuperMarioBrosRandomStagesEnv`, tests, CLI, speed tests, examples, README snippets, and package metadata.
- Preserve all public environment IDs, ROM mode names, stage IDs, action sets, reward semantics, info keys, and ROM package data.
- Do not add, remove, or modify ROM assets.

## Migration Target

Use the Gymnasium/v0.26+ environment contract:

- Users import Gymnasium as `gym` and create environments with `gym.make(..., render_mode=...)`.
- `reset(seed=..., options=...)` returns `(observation, info)`.
- `step(action)` returns `(observation, reward, terminated, truncated, info)`.
- `terminated` represents Mario game or stage-ending conditions.
- `truncated` is `False` for internal Mario logic unless a wrapper such as Gymnasium `TimeLimit` ends the episode.
- Random-stage selection remains controlled by `reset(seed=...)` and `options`.

## Acceptance Criteria

- [ ] The package imports `gymnasium` instead of legacy `gym` in registration code, CLI code, direct environment subclasses, tests, and documentation examples.
- [ ] `install_requires` includes a Gymnasium dependency directly if this package imports Gymnasium directly, and the `nes-py` dependency points to a version or branch that contains the completed base migration.
- [ ] `SuperMarioBrosEnv.__init__()` accepts `render_mode=None`, passes it to `NESEnv`, and preserves `rom_mode`, `lost_levels`, and `target` behavior.
- [ ] Initialization logic that resets, skips start screens, and creates backup states is updated for the Gymnasium reset tuple without changing emulator state.
- [ ] Mario termination logic formerly exposed through `_get_done()` is migrated to the new base hook or compatibility bridge required by the completed `nes-py` spec.
- [ ] `SuperMarioBrosRandomStagesEnv` subclasses `gymnasium.Env`, accepts `render_mode=None`, uses Gymnasium seeding, and no longer uses a supported `Env.seed()` flow.
- [ ] `SuperMarioBrosRandomStagesEnv.reset(seed=..., options=...)` returns `(observation, info)`, preserves deterministic random-stage selection for a fixed seed, and still supports `options={"stages": [...]}`.
- [ ] `SuperMarioBrosRandomStagesEnv.step(action)` returns the Gymnasium five-value tuple from the selected child environment.
- [ ] `SuperMarioBrosRandomStagesEnv.render()` uses the selected render mode without requiring a mode argument.
- [ ] All existing environment IDs remain registered, including `SuperMarioBros-v0` through `SuperMarioBros-v3`, `SuperMarioBrosRandomStages-v0` through `SuperMarioBrosRandomStages-v3`, `SuperMarioBros2-v0` through `SuperMarioBros2-v1`, and per-stage IDs.
- [ ] Registered environments can be created with `gymnasium.make(id, render_mode="rgb_array")`.
- [ ] `max_episode_steps` registration still works through Gymnasium and produces `truncated=True` only when the Gymnasium time limit ends an episode.
- [ ] README examples, CLI playback, and `speedtest.py` use `reset(seed=...)`, unpack `(observation, info)`, unpack `(observation, reward, terminated, truncated, info)`, and compute `done = terminated or truncated` only for local control flow.
- [ ] No supported documentation or test tells users to call `env.seed(...)`.
- [ ] Tests assert the new tuple lengths and types for at least one standard Mario env, one random-stage env, and one per-stage env.
- [ ] Tests verify that random-stage selection remains reproducible under a fixed seed and configurable with `options["stages"]`.
- [ ] Package metadata no longer advertises unsupported Python versions unless those versions remain tested.
- [ ] A breaking-change version bump is applied if the project version is updated as part of this migration.
- [ ] Generated artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [ ] The `gym-super-mario-bros` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd gym-super-mario-bros
python -m pip install --upgrade pip
python -m pip install -e ../nes-py
python -m pip install -e .
python -m unittest discover .
```

Run a focused Gymnasium smoke check:

```sh
cd gym-super-mario-bros
python - <<'PY'
import gymnasium as gym
import gym_super_mario_bros

for env_id in ("SuperMarioBros-v0", "SuperMarioBrosRandomStages-v0", "SuperMarioBros1-1-v0"):
    env = gym.make(env_id, render_mode="rgb_array")
    observation, info = env.reset(seed=123)
    result = env.step(env.action_space.sample())
    assert len(result) == 5
    observation, reward, terminated, truncated, info = result
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    frame = env.render()
    assert frame is not None
    env.close()
PY
```

If `gymnasium.utils.env_checker.check_env` can run without false positives from emulator side effects, add it to the test suite or document why the focused smoke checks are the better verification path.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-super-mario-bros` submodule changes.
- Commit and push the umbrella repository's updated `gym-super-mario-bros` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--gym-super-mario-bros-gymnasium-api.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

# Specification: gym-zelda-1 Gymnasium API Migration

## Problem

`gym-zelda-1` still registers and documents a legacy OpenAI Gym environment. It imports `gym`, exposes `gym_zelda_1.make` from the old package, uses `env.seed(...)` in tests, and shows old reset and step tuple shapes in examples. The project is less mature than the other wrappers, but it should still follow the same modern Gymnasium API once `nes-py` provides the base contract.

## Scope

- Work inside the `gym-zelda-1` submodule unless an umbrella gitlink update is required after committing the submodule.
- Start this spec only after `specs/002-nes-py-gymnasium-api.md` is complete and the wrapper can depend on a pushed `nes-py` commit with the new API.
- Replace runtime use of legacy `gym` with Gymnasium.
- Update registration, `Zelda1Env`, tests, CLI or run examples, README snippets, and package metadata.
- Preserve the public environment ID `Zelda1-v0`, action space, observation space, info keys, current placeholder reward behavior, and ROM package data.
- Do not add, remove, or modify ROM assets.
- Do not expand Zelda reward shaping or gameplay objectives beyond what is necessary for the API migration.

## Migration Target

Use the Gymnasium/v0.26+ environment contract:

- Users import Gymnasium as `gym` and create the environment with `gym.make("Zelda1-v0", render_mode=...)`.
- `reset(seed=..., options=...)` returns `(observation, info)`.
- `step(action)` returns `(observation, reward, terminated, truncated, info)`.
- `terminated` represents Zelda game-ending logic. If no game-ending condition is implemented yet, it remains `False` and that limitation is documented in tests and completion notes.
- `truncated` is `False` for internal Zelda logic unless a Gymnasium wrapper imposes a time limit.
- Seeding is performed through `reset(seed=...)`, not `env.seed(...)`.

## Acceptance Criteria

- [ ] The package imports `gymnasium` instead of legacy `gym` in registration code, CLI or run code, tests, and documentation examples.
- [ ] `install_requires` includes a Gymnasium dependency directly if this package imports Gymnasium directly, and the `nes-py` dependency points to a version or branch that contains the completed base migration.
- [ ] `gym_zelda_1.make` remains available as an alias to `gymnasium.make`.
- [ ] `Zelda1Env.__init__()` accepts `render_mode=None`, passes it to `NESEnv`, and preserves current reset, start-screen skip, and backup setup behavior.
- [ ] Initialization logic is updated for the Gymnasium reset tuple without changing emulator state.
- [ ] Zelda termination logic formerly exposed through `_get_done()` is migrated to the new base hook or compatibility bridge required by the completed `nes-py` spec.
- [ ] `Zelda1-v0` remains registered and can be created with `gymnasium.make("Zelda1-v0", render_mode="rgb_array")`.
- [ ] `reset(seed=...)` returns `(observation, info)` and uses the same seeding path as the migrated `NESEnv`.
- [ ] `step(action)` returns `(observation, reward, terminated, truncated, info)`.
- [ ] Current reward behavior is preserved unless a separate Zelda reward spec explicitly changes it.
- [ ] Info keys remain stable for currently exposed Zelda state, including level and position fields.
- [ ] README examples, `run.py`, and CLI flows use `reset(seed=...)`, unpack `(observation, info)`, unpack `(observation, reward, terminated, truncated, info)`, and compute `done = terminated or truncated` only for local control flow.
- [ ] No supported documentation or test tells users to call `env.seed(...)`.
- [ ] Tests assert the new tuple lengths and types for `Zelda1-v0`.
- [ ] Any currently commented-out API tests that can run reliably are either restored under the new API or replaced by equivalent active coverage.
- [ ] Package metadata no longer advertises unsupported Python versions unless those versions remain tested.
- [ ] Package metadata touched by this work no longer describes the project as Super Mario Bros. or links to the Mario repository.
- [ ] A breaking-change pre-1.0 version bump is applied if the project version is updated as part of this migration.
- [ ] Generated artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [ ] The `gym-zelda-1` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd gym-zelda-1
python -m pip install --upgrade pip
python -m pip install -e ../nes-py
python -m pip install -e .
python -m unittest discover .
```

Run a focused Gymnasium smoke check:

```sh
cd gym-zelda-1
python - <<'PY'
import gymnasium as gym
import gym_zelda_1

env = gym.make("Zelda1-v0", render_mode="rgb_array")
observation, info = env.reset(seed=123)
result = env.step(env.action_space.sample())
assert len(result) == 5
observation, reward, terminated, truncated, info = result
assert isinstance(terminated, bool)
assert isinstance(truncated, bool)
assert "x_pos" in info
assert "y_pos" in info
frame = env.render()
assert frame is not None
env.close()
PY
```

If `gymnasium.utils.env_checker.check_env` can run without false positives from emulator side effects, add it to the test suite or document why the focused smoke checks are the better verification path.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-zelda-1` submodule changes.
- Commit and push the umbrella repository's updated `gym-zelda-1` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--gym-zelda-1-gymnasium-api.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

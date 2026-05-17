# Specification: gym-tetris Gymnasium API Migration

## Problem

`gym-tetris` still uses the old OpenAI Gym API in registration, tests, CLI flows, and documentation. It expects `env.seed(...)`, `reset()` returning only an observation, and `step()` returning `(observation, reward, done, info)`. After `nes-py` moves to Gymnasium, `gym-tetris` must expose the modern API while preserving existing Tetris modes, reward options, deterministic-start behavior, and info fields.

## Scope

- Work inside the `gym-tetris` submodule unless an umbrella gitlink update is required after committing the submodule.
- Start this spec only after `specs/002-nes-py-gymnasium-api.md` is complete and the wrapper can depend on a pushed `nes-py` commit with the new API.
- Replace runtime use of legacy `gym` with Gymnasium.
- Update registration, `TetrisEnv`, tests, CLI, speed or run examples, README snippets, and package metadata.
- Preserve all public environment IDs, constructor options, reward calculations, info keys, deterministic behavior, action spaces, and ROM package data.
- Do not add, remove, or modify ROM assets.

## Migration Target

Use the Gymnasium/v0.26+ environment contract:

- Users import Gymnasium as `gym` and create environments with `gym.make(..., render_mode=...)`.
- `reset(seed=..., options=...)` returns `(observation, info)`.
- `step(action)` returns `(observation, reward, terminated, truncated, info)`.
- `terminated` represents Tetris game-ending or win conditions.
- `truncated` is `False` for internal Tetris logic unless a Gymnasium wrapper imposes a time limit.
- Seeding is performed through `reset(seed=...)`, not `env.seed(...)`.

## Acceptance Criteria

- [ ] The package imports `gymnasium` instead of legacy `gym` in registration code, CLI code, tests, and documentation examples.
- [ ] `install_requires` includes a Gymnasium dependency directly if this package imports Gymnasium directly, and the `nes-py` dependency points to a version or branch that contains the completed base migration.
- [ ] `TetrisEnv.__init__()` accepts `render_mode=None`, passes it to `NESEnv`, and preserves `b_type`, `reward_score`, `reward_lines`, `penalize_height`, and `deterministic` behavior.
- [ ] Initialization logic that resets, skips the start screen, creates backup state, and restores deterministic setup is updated for the Gymnasium reset tuple without changing emulator state.
- [ ] Tetris termination logic formerly exposed through `_get_done()` is migrated to the new base hook or compatibility bridge required by the completed `nes-py` spec.
- [ ] All registered IDs remain available through Gymnasium: `TetrisA-v0` through `TetrisA-v3` and `TetrisB-v0` through `TetrisB-v3`.
- [ ] Registered environments can be created with `gymnasium.make(id, render_mode="rgb_array")`.
- [ ] `reset(seed=...)` returns `(observation, info)` and preserves reproducible starts for both deterministic and non-deterministic modes according to the existing semantics.
- [ ] `step(action)` returns `(observation, reward, terminated, truncated, info)`, where `terminated` is true when the game is over or the game is won.
- [ ] Reward calculations for score, lines, and height penalty are unchanged except for tuple unpacking and termination naming.
- [ ] Info keys remain stable, including `current_piece`, `number_of_lines`, `score`, `next_piece`, `statistics`, and `board_height`.
- [ ] README examples and CLI flows use `reset(seed=...)`, unpack `(observation, info)`, unpack `(observation, reward, terminated, truncated, info)`, and compute `done = terminated or truncated` only for local control flow.
- [ ] No supported documentation or test tells users to call `env.seed(...)`.
- [ ] Tests assert the new tuple lengths and types for at least one A-type env and one B-type env.
- [ ] Tests cover the existing reward modes after the API migration.
- [ ] Package metadata no longer advertises unsupported Python versions unless those versions remain tested.
- [ ] A breaking-change version bump is applied if the project version is updated as part of this migration.
- [ ] Generated artifacts, caches, `.DS_Store`, eggs, wheels, and compiled objects are not committed.
- [ ] The `gym-tetris` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run the strongest feasible local checks before pushing:

```sh
cd gym-tetris
python -m pip install --upgrade pip
python -m pip install -e ../nes-py
python -m pip install -e .
python -m unittest discover .
```

Run a focused Gymnasium smoke check:

```sh
cd gym-tetris
python - <<'PY'
import gymnasium as gym
import gym_tetris

for env_id in ("TetrisA-v0", "TetrisB-v0"):
    env = gym.make(env_id, render_mode="rgb_array")
    observation, info = env.reset(seed=123)
    result = env.step(env.action_space.sample())
    assert len(result) == 5
    observation, reward, terminated, truncated, info = result
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert "score" in info
    frame = env.render()
    assert frame is not None
    env.close()
PY
```

If `gymnasium.utils.env_checker.check_env` can run without false positives from emulator side effects, add it to the test suite or document why the focused smoke checks are the better verification path.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-tetris` submodule changes.
- Commit and push the umbrella repository's updated `gym-tetris` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--gym-tetris-gymnasium-api.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

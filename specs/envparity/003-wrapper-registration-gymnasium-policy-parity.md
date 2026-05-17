# Specification: Wrapper Registration and Gymnasium Policy Parity

## Problem

The wrappers expose Gymnasium environments, but their registration layout and
Gymnasium policy are inconsistent:

- Mario and Tetris isolate registration in `_registration.py`; Zelda registers
  directly from `gym_zelda_1/__init__.py`.
- Mario and Zelda disable the Gymnasium env checker on registered environments;
  Tetris does not.
- Mario sets a large `max_episode_steps` and has a truncation regression test;
  Tetris and Zelda do not document or test their registration-level truncation
  policy.
- Some comments still mention old `gym` wording even though runtime imports
  use Gymnasium.

The result is not a runtime disaster, but it makes the wrappers harder to
compare and raises ambiguity about which Gymnasium warnings are expected.

## Scope

- Work inside `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1`.
- Keep public environment IDs stable.
- Keep `gym_super_mario_bros.make`, `gym_tetris.make`, and
  `gym_zelda_1.make` available as convenience aliases to `gymnasium.make`.
- Preserve wrapper-specific kwargs, action spaces, reward semantics, and info
  keys.
- Do not add, remove, or modify ROM assets.

## Acceptance Criteria

- [ ] Each wrapper has a `_registration.py` module that owns environment
      registration and the `make = gymnasium.make` alias.
- [ ] Each package `__init__.py` imports its public environment class or
      classes and imports `make` from `_registration.py`.
- [ ] Public `__all__` definitions are stable and consistent across wrappers.
- [ ] The registered IDs remain unchanged:
      `SuperMarioBros-v0` through `SuperMarioBros-v3`,
      `SuperMarioBrosRandomStages-v0` through
      `SuperMarioBrosRandomStages-v3`, `SuperMarioBros2-v0` through
      `SuperMarioBros2-v1`, Mario per-stage IDs and aliases,
      `TetrisA-v0` through `TetrisA-v3`, `TetrisB-v0` through
      `TetrisB-v3`, and `Zelda1-v0`.
- [ ] The env-checker policy is explicit for each wrapper: either the checker
      runs cleanly in tests, or `disable_env_checker=True` remains with a
      comment and test coverage explaining why the registered environment
      disables it.
- [ ] Registration-level `max_episode_steps` and truncation behavior are
      documented and tested where a wrapper sets or relies on them.
- [ ] Tests assert each package-level `make` alias is `gymnasium.make`.
- [ ] Tests assert each representative registered environment can be made with
      `render_mode="rgb_array"`, reset with `seed=...`, stepped once, rendered,
      and closed.
- [ ] Old comments that refer to "Gym" registration are updated to
      "Gymnasium" where they describe current behavior.
- [ ] No generated artifacts, caches, build outputs, or local virtual
      environments are committed.

## Verification

Run each wrapper test suite:

```sh
cd gym-super-mario-bros
python -m unittest discover .
```

```sh
cd gym-tetris
python -m unittest discover .
```

```sh
cd gym-zelda-1
python -m unittest discover .
```

Run representative smoke checks:

```sh
cd gym-super-mario-bros
python - <<'PY'
import gymnasium as gym
import gym_super_mario_bros

for env_id in ("SuperMarioBros-v0", "SuperMarioBrosRandomStages-v0", "SuperMarioBros1-1-v0"):
    env = gym.make(env_id, render_mode="rgb_array")
    env.reset(seed=123)
    assert len(env.step(env.action_space.sample())) == 5
    assert env.render() is not None
    env.close()
PY
```

```sh
cd gym-tetris
python - <<'PY'
import gymnasium as gym
import gym_tetris

for env_id in ("TetrisA-v0", "TetrisB-v0"):
    env = gym.make(env_id, render_mode="rgb_array")
    env.reset(seed=123)
    assert len(env.step(env.action_space.sample())) == 5
    assert env.render() is not None
    env.close()
PY
```

```sh
cd gym-zelda-1
python - <<'PY'
import gymnasium as gym
import gym_zelda_1

env = gym.make("Zelda1-v0", render_mode="rgb_array")
env.reset(seed=123)
assert len(env.step(env.action_space.sample())) == 5
assert env.render() is not None
env.close()
PY
```

## Completion Signal

When all acceptance criteria are met:

- Commit and push each changed wrapper submodule.
- Commit and push the umbrella repository's updated submodule pointers.
- Append the required one-line summary to `history.md`.
- Add a completion log for this spec.
- Output `DONE` only after local verification passes and required remote checks
  are green.

<!-- NR_OF_TRIES: 0 -->

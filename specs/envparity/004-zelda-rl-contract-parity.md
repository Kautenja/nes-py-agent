# Specification: Zelda RL Contract Parity

## Problem

`gym-zelda-1` follows the modern Gymnasium tuple shapes, but its core
environment contract is still much less explicit than `nes-py`,
`gym-super-mario-bros`, or `gym-tetris`:

- `_get_reward()` returns `0` with a TODO.
- `_get_terminated()` always returns `False` with a TODO.
- The README describes reward behavior as a work in progress, but the test
  suite only verifies the current placeholder behavior.
- `_did_step()` advances through death, scrolling, text, cave, and inventory
  waits without a documented episode lifecycle policy.

Zelda does not need Mario's large feature set, but it should have an explicit
and tested baseline RL contract so users know whether `Zelda1-v0` is a
playable task, a navigation sandbox, or a state-inspection environment.

## Scope

- Work inside `gym-zelda-1` unless an umbrella gitlink update is required.
- Keep the public environment ID `Zelda1-v0`.
- Preserve the public action space, observation shape, render modes, and
  existing info keys unless a change is documented as a deliberate breaking
  change.
- Do not add new Zelda maps, screenshots, ROMs, or external game assets.
- Keep the first pass modest: characterize reliable RAM signals, then define a
  minimal v0 contract rather than attempting a full game-completion reward.

## Acceptance Criteria

- [ ] A short design note in the spec completion log explains whether
      `Zelda1-v0` is treated as a baseline task, navigation sandbox, or
      state-inspection environment.
- [ ] The reward function is no longer a TODO-only placeholder. It either
      implements a minimal documented signal or deliberately returns zero with
      a named rationale in code and docs.
- [ ] The termination function is no longer a TODO-only placeholder. It either
      detects a reliable Zelda terminal condition or deliberately documents why
      `Zelda1-v0` has no internal terminal condition yet.
- [ ] Death, low-health, continue-screen, and post-death behavior are
      characterized with focused tests or documented as unreliable RAM signals.
- [ ] `_did_step()` does not silently erase a terminal condition before
      `_get_terminated()` can report it, unless the v0 contract explicitly
      defines death recovery as non-terminal.
- [ ] README reward and termination sections describe the implemented contract
      without unresolved TODO wording.
- [ ] Tests cover reset, step, reward, terminated, truncated, render, and info
      keys for the selected contract.
- [ ] If the public semantics change, apply an appropriate version bump and
      note the change in release-facing documentation.
- [ ] No generated artifacts, caches, build outputs, or local virtual
      environments are committed.

## Verification

Run the Zelda test suite:

```sh
cd gym-zelda-1
python -m unittest discover .
```

Run a focused gameplay smoke check:

```sh
cd gym-zelda-1
python - <<'PY'
import gymnasium as gym
import gym_zelda_1

env = gym.make("Zelda1-v0", render_mode="rgb_array")
observation, info = env.reset(seed=123)
for _ in range(120):
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert "hearts" in info
    if terminated or truncated:
        break
assert env.render() is not None
env.close()
PY
```

If a full Gymnasium env checker run is retained, document any suppressed
warnings and why they are expected for a NES emulator environment.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `gym-zelda-1` submodule changes.
- Commit and push the umbrella repository's updated `gym-zelda-1` gitlink.
- Append the required one-line summary to `history.md`.
- Add a completion log for this spec.
- Output `DONE` only after local verification passes and required remote checks
  are green.

<!-- NR_OF_TRIES: 0 -->

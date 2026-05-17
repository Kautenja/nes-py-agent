# Specification: Wrapper CLI Playback Parity

## Problem

`nes_py.play` has a clear Gymnasium-era playback contract: human or random
mode, configurable step counts, optional rendering for random runs, and
render-mode handling that supports headless smoke tests. The wrapper CLIs are
close but uneven:

- `gym-tetris` has the strongest wrapper CLI parity: `--seed`,
  `--render/--no-render`, and action-space selection are present.
- `gym-super-mario-bros` supports action-space selection and random-stage
  subsets, but random mode always creates a human-rendering environment and has
  no `--no-render` or CLI seed path.
- `gym-zelda-1` exposes only environment, mode, and steps even though its
  README documents `JoypadSpace` and `MOVEMENT`; it lacks action-space
  selection, seed injection, and `--no-render` support.

These are user-facing parity gaps with the shared `nes-py` tooling. They also
make quick CI or local smoke runs harder than they need to be.

## Scope

- Work inside `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1`.
- Preserve each wrapper's existing console script entry point.
- Preserve Mario-specific CLI features such as `--stages`.
- Do not require Tetris or Zelda to gain Mario's stage or ROM-mode feature set.
- Do not add, remove, or modify ROM assets.

## Acceptance Criteria

- [ ] Each wrapper CLI supports `--mode human|random`, `--steps`, and
      `--render/--no-render` with semantics compatible with `nes_py.play`.
- [ ] Human mode rejects `--no-render` with an argparse error.
- [ ] Random mode can run headlessly without constructing a human render
      window.
- [ ] Each wrapper CLI supports an optional seed path that applies to the first
      Gymnasium reset without reintroducing `env.seed(...)`.
- [ ] Each wrapper CLI exposes action-space selection when the package has a
      public `actions.py` preset suitable for `nes_py.wrappers.JoypadSpace`.
- [ ] Mario keeps `--stages/-S` behavior limited to random-stage environments.
- [ ] Zelda can use `gym_zelda_1.actions.MOVEMENT` from the CLI, matching its
      README guidance.
- [ ] CLI parsing and playback helpers are covered by tests that do not require
      a graphical window.
- [ ] README command-line examples match the implemented options.
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

Run focused headless CLI smoke checks:

```sh
cd gym-super-mario-bros
python -m gym_super_mario_bros._app.cli --mode random --steps 5 --no-render --seed 123
```

```sh
cd gym-tetris
python -m gym_tetris._app.cli --mode random --steps 5 --no-render --seed 123
```

```sh
cd gym-zelda-1
python -m gym_zelda_1._app.cli --mode random --steps 5 --no-render --seed 123 --actionspace movement
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

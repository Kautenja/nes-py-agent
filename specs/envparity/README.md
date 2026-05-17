# Environment Parity Backlog

This directory tracks parity work discovered by comparing the game wrapper
repositories against the current `nes-py` baseline.

These specs are planning backlog items, not the active Ralph queue. Promote or
explicitly target one of them when it should be implemented.

## Parity Principle

Parity does not mean every wrapper should become `gym-super-mario-bros`.
`gym-super-mario-bros` is the flagship project and reasonably has more stage
IDs, ROM modes, action presets, tests, and user-facing features than
`gym-tetris` or `gym-zelda-1`.

The goal here is narrower:

- keep all wrappers aligned with the supported `nes-py` Python, Gymnasium, CI,
  release, and CLI contracts;
- keep wrapper-specific game logic in the wrapper repositories;
- avoid adding new ROM assets or redistributing external game assets;
- treat Zelda's lower maturity as an explicit product state rather than an
  accidental drift from the shared environment contract.

## Backlog

| Prefix | Spec | Summary |
| --- | --- | --- |
| `001` | Wrapper Python, CI, and dependency parity | Align supported Python versions, CI matrices, and development dependency policy with `nes-py`. |
| `002` | Wrapper CLI playback parity | Bring wrapper CLIs in line with `nes_py.play` ergonomics for random/headless playback, seeding, and action-space selection. |
| `003` | Wrapper registration and Gymnasium policy parity | Normalize registration layout, `make` aliases, env-checker policy, and truncation behavior. |
| `004` | Zelda RL contract parity | Turn Zelda's placeholder reward/termination behavior into an explicit, tested environment contract. |
| `005` | Wrapper documentation and metadata parity | Clean up cross-wrapper docs, pyproject metadata, and stale comments that conflict with the `nes-py` baseline. |

# gym-nes Constitution

> Umbrella project for coordinated development on `nes-py`, the NES emulator and OpenAI Gym interface, plus game-specific Gym wrappers such as Super Mario Bros., Tetris, and The Legend of Zelda.

---

## Ralph Source

Ralph Wiggum scripts were copied from `https://github.com/fstandhartinger/ralph-wiggum` at commit `3f15f0fb83b8c2e0ac8d11abdae0e83ab8204981`.

---

## Context Detection

### Ralph Loop Mode

You are in Ralph Loop Mode when started by `scripts/ralph-loop*.sh`, when the prompt says to implement specs, or when the prompt says to work through the project queue autonomously.

In this mode:

- Read this constitution before doing anything else.
- Read `history.md`, `CHANGELOG.md`, and relevant files in `history/` before
  selecting work.
- Pick the highest priority incomplete root Markdown spec from `specs/`.
- Implement all acceptance criteria for that spec.
- Verify with focused tests, smoke checks, or build commands appropriate to the changed submodule.
- Commit and push changes inside child submodules first.
- Commit and push the umbrella submodule pointer and root-level workflow changes second.
- Output `DONE` only after all acceptance criteria are verified, tests pass, and required commits/pushes are complete.
- Output `ALL_DONE` only when there are no incomplete specs, after re-checking that state.

### Interactive Mode

When not in Ralph Loop Mode, collaborate normally: answer questions, refine specs, make requested edits, and keep the user in the loop.

---

## Core Principles

1. Respect submodule boundaries. `nes-py`, `gym-super-mario-bros`, and `gym-tetris` must remain independently buildable, testable, and releasable.
2. Prefer reproducible emulator behavior over cleverness. Determinism, testability, and clear environment registration matter more than speculative abstractions.
3. Keep wrappers game-aware. Game-dependent APIs, ROM handling, action spaces, rewards, and tests should live in the relevant wrapper repo unless they truly belong in `nes-py`.
4. Use specs as contracts. Every Ralph task should have concrete acceptance criteria and a clear verification path.
5. Preserve licensing and ROM sensitivity. Do not add new ROM assets, redistribute external game assets, or change license text without explicit user direction.

---

## Technical Stack

- Python packages using setuptools.
- `nes-py` includes a native C++ NES emulator extension.
- Any C++-level tests for native emulator code must use Catch2.
- Game wrappers depend on `nes-py` and expose OpenAI Gym environments.
- The umbrella repo uses Git submodules pinned to the active development branch of each child project.
- Ralph Wiggum scripts live in `scripts/`; generated runtime logs live in `logs/`.

---

## Submodules

| Path | Purpose | Remote | Branch |
| --- | --- | --- | --- |
| `nes-py` | NES emulator and Gym interface | `git@github.com:Kautenja/nes-py` | `ralph-dev` |
| `gym-super-mario-bros` | Super Mario Bros. Gym wrapper | `git@github.com:Kautenja/gym-super-mario-bros.git` | `ralph-dev` |
| `gym-tetris` | Tetris Gym wrapper | `git@github.com:Kautenja/gym-tetris.git` | `ralph-dev` |
| `gym-zelda-1` | The Legend of Zelda Gym wrapper | `git@github.com:Kautenja/gym-zelda-1.git` | `master` |

Submodule work must be committed inside the child repository before the umbrella repo records the updated gitlink. Do not treat a dirty submodule as complete work.

---

## Autonomy

YOLO Mode: ENABLED

Git Autonomy: ENABLED

Ralph may run commands, edit files, test, commit, and push without asking for per-command approval when running in loop mode. Interactive sessions should still use normal judgment and respect user intent.

---

## Specs

Active specs live in `specs/` as root Markdown files. Lower numeric prefixes are higher priority, for example `001-fix-reset-determinism.md`.

A spec is incomplete unless it contains `## Status: COMPLETE`.

Completed specs must be retired from the active queue after the completion log
and history entry are written, before the final queue re-check. Keep durable
context in `history.md`, `CHANGELOG.md`, and focused files under `history/`.
Use `specs/archive/` only as a short-term or pointer archive; do not let full
completed task bodies pile up there.

Each spec should include:

- Problem or goal
- Scope
- Acceptance criteria
- Verification commands or checks
- Completion signal expectations

Track attempts per spec with an `<!-- NR_OF_TRIES: N -->` comment at the bottom of the file. Increment it on each Ralph attempt. If a spec reaches 10 attempts, split it into smaller specs before continuing.

---

## History

Append a one-line summary to `history.md` after each completed spec. For larger
decisions or lessons learned, create `history/YYYY-MM-DD--spec-name.md`. Update
`CHANGELOG.md` when the completed work changes release notes or durable project
context.

---

## Completion Logs

After each completed spec, create `completion_log/YYYY-MM-DD--HH-MM-SS--spec-name.md` with a brief summary, the verification performed, and the commits pushed.

---

## Completion Signal

All acceptance criteria verified, tests pass, child submodule changes committed and pushed, umbrella gitlink committed and pushed -> output `DONE`.

No incomplete specs remain after re-checking the queue -> output `ALL_DONE`.

Never output either completion signal early.

# gym-nes

Umbrella repository for coordinated development across the NES emulator and game-specific OpenAI Gym wrappers.

This repo tracks the child projects as git submodules:

| Path | Repository | Branch |
| --- | --- | --- |
| `nes-py` | `git@github.com:Kautenja/nes-py` | `ralph-dev` |
| `gym-super-mario-bros` | `git@github.com:Kautenja/gym-super-mario-bros.git` | `ralph-dev` |
| `gym-tetris` | `git@github.com:Kautenja/gym-tetris.git` | `ralph-dev` |
| `gym-zelda-1` | `git@github.com:Kautenja/gym-zelda-1.git` | `ralph-dev` |

## Clone

```bash
git clone --recurse-submodules <this-repo-url>
cd gym-nes
```

For an existing clone:

```bash
git submodule update --init --recursive
```

To pull the latest `ralph-dev` branch tips into the submodules:

```bash
git submodule update --remote --merge
```

## Development

Create a local environment from the umbrella root and install each package in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./nes-py -e ./gym-super-mario-bros -e ./gym-tetris -e ./gym-zelda-1
```

Run tests from the project that changed:

```bash
cd nes-py
python -m pytest
```

When a child project changes, commit and push inside that submodule first. Then return to the umbrella repo, stage the updated submodule pointer, and commit the umbrella update:

```bash
git -C nes-py status
git -C nes-py add ...
git -C nes-py commit -m "..."
git -C nes-py push

git add nes-py
git commit -m "Update nes-py submodule"
```

## Ralph Wiggum Workflow

This repo includes the Ralph Wiggum loop scripts from `fstandhartinger/ralph-wiggum` at commit `3f15f0fb83b8c2e0ac8d11abdae0e83ab8204981`.

Work items live in `specs/` as Markdown specs. In build mode, Ralph picks the highest priority incomplete spec, implements it, verifies the acceptance criteria, commits and pushes, then emits the completion signal.

Useful commands:

```bash
./scripts/ralph-loop-codex.sh plan
./scripts/ralph-loop-codex.sh
./scripts/ralph-loop-codex.sh 20
```

The loop reads `.specify/memory/constitution.md` each iteration. Keep that file aligned with the intended project rules before starting long-running work.

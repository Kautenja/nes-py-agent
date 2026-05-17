# Wrapper Python, CI, and Dependency Parity

## Summary

Aligned `gym-super-mario-bros`, `gym-tetris`, and `gym-zelda-1` with the
current `nes-py` Python support baseline. Each wrapper now advertises Python
3.13 and 3.14 support, runs CI across both Python versions on the existing
Linux, Windows, and macOS runner set, includes the Python version in CI artifact
names, and uses a consistent `requirements.txt` bootstrap policy for
`nes-py @ ralph-dev` while keeping canonical runtime metadata in
`pyproject.toml`.

## Verification

- `gym-super-mario-bros`: `.venv/bin/python -m pip install -r requirements.txt`,
  `.venv/bin/python -m pip install -e .`, `.venv/bin/python -m unittest discover .`
  (`50 tests`), and `.venv/bin/python -m build --outdir /private/tmp/gym-super-mario-bros-envparity-dist-final`.
- `gym-tetris`: `.venv/bin/python -m pip install -r requirements.txt`,
  `.venv/bin/python -m pip install -e .`, `.venv/bin/python -m unittest discover .`
  (`16 tests`), and `.venv/bin/python -m build --outdir /private/tmp/gym-tetris-envparity-dist-final`.
- `gym-zelda-1`: `.venv/bin/python -m pip install -r requirements.txt`,
  `.venv/bin/python -m pip install -e .`, `.venv/bin/python -m unittest discover .`
  (`5 tests`), and `.venv/bin/python -m build --outdir /private/tmp/gym-zelda-1-envparity-dist-final`.
- Direct `python -m ...` verification was not available locally because
  `python` is not on PATH; the local wrapper virtual environments use Python
  3.13 and exercised the same commands.
- GitHub Actions PR CI completed successfully with the expanded 10-job matrix
  for each wrapper:
  - `gym-super-mario-bros` PR #140, run `26005593445`.
  - `gym-tetris` PR #28, run `26005593653`.
  - `gym-zelda-1` PR #3, run `26005593523`.

## Commits

- `gym-super-mario-bros`: `bed6152e55bc99d758d8fbedd83f3366ad9adda6`,
  `47e4ad08136914df92738ffac86aa6e808196295`.
- `gym-tetris`: `516b26142c2b8ba23cddb2879918ee9704617541`,
  `b06f439e2496c243405244877b9c2f35d288c1ae`.
- `gym-zelda-1`: `e2f9e3aa473bd124ca7b25455d927518610d68bb`,
  `fe3baff35497dbb7da5bb5a355706bb3edf1ebc4`.
- Umbrella repository: this commit records the wrapper submodule pointers,
  completion log, history entry, and archived spec.

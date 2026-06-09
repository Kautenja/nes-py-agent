# Completion Log: Playing Mario Modern Dependency Baseline

## Summary

Completed the Playing Mario dependency baseline by adding modern setuptools
metadata, a lightweight `mario_rl` package, current Gymnasium/PyTorch/Lightning
runtime dependencies, local editable install documentation for the umbrella
`nes-py` and `gym-super-mario-bros` submodules, and focused dependency/layout
contract tests.

The legacy `src` package remains present for later migration specs, but package
imports are now lazy so unittest discovery does not import Gym, Keras, or
plotting frameworks just by walking packages. Legacy Keras model tests are
skipped when Keras is absent, matching this spec's out-of-scope PyTorch port.

## Red Checks

- `python3 -m unittest discover .` before implementation failed with import
  errors for missing `numpy`, `gym`, `keras`, and `matplotlib`.
- After adding contract tests, `python3 -m unittest discover tests` failed
  because `pyproject.toml`, `mario_rl`, and modern runtime dependencies were
  absent.
- First editable install attempt failed on a stale MIT license classifier under
  current setuptools; removing the classifier fixed the metadata.

## Verification

Run from `playing-mario-with-deep-reinforcement-learning/` with a fresh
Python 3.13 venv at `/tmp/gym-nes-ralph-001-venv`.

- `python3.13 -m venv /tmp/gym-nes-ralph-001-venv`
- `python -m pip install --upgrade pip setuptools wheel`
- `python -m pip install -e ../nes-py -e ../gym-super-mario-bros`
- `python -m pip install -e .`
- `python3 -m pip check` with venv on `PATH`: `No broken requirements found.`
- `python3 -m unittest discover .` with venv on `PATH`: `17 tests`, `OK`
  (`skipped=2`)
- `./main.sh unittest` with venv on `PATH`: `17 tests`, `OK` (`skipped=2`)
- Import smoke:

  ```text
  gymnasium 1.3.0
  torch 2.12.0
  lightning 2.6.5
  ```

## Installed Versions

- `playing-mario-with-deep-reinforcement-learning==6.0.0.dev0`
- `gym_super_mario_bros==8.0.0`
- `nes_py==9.0.0`
- `gymnasium==1.3.0`
- `torch==2.12.0`
- `lightning==2.6.5`
- `numpy==2.4.6`
- `opencv-python==4.13.0.92`
- `pillow==12.2.0`
- `pandas==3.0.3`
- `matplotlib==3.10.9`
- `tqdm==4.68.2`
- `PyYAML==6.0.3`
- `jsonargparse==4.49.0`

## Commits

- `playing-mario-with-deep-reinforcement-learning`: `483823f`
  (`Modernize Mario dependency baseline`), pushed to `origin/pytorch`
- Umbrella: included in the umbrella commit that records this completion log

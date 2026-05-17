# Completion Log: nes-py Mapper API Lifecycle and Timing Hooks

## Summary

Implemented the mapper lifecycle and hook architecture in `nes-py`: RAII mapper ownership, registration-based mapper factory, state-only bus/PPU snapshots, mapper-owned PRG RAM, IRQ callback routing, CPU/PPU hook points, expansion-area routing, nametable delegation, and focused native smoke checks exposed through Python tests.

Documented the tiny before/after mapper profile in `nes-py/docs/native-mapper-api-performance-follow-up.md`.

## Verification

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 20 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --profile-rom nes_py/tests/games/super-mario-bros-1.nes --profile-rom nes_py/tests/games/the-legend-of-zelda.nes --steps 20 --warmup-steps 5 --json --no-progress`

## Commits Pushed

- `nes-py`: `0d7cc09` (`Add mapper lifecycle hooks`)

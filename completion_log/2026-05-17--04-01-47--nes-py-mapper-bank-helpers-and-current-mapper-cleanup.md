# Completion Log: nes-py Mapper Bank Helpers and Current Mapper Cleanup

## Summary

Added shared native mapper bank helpers for PRG/CHR window selection, fixed
first/final banks, safe masked bank selection, bus-conflict value resolution,
and mapper-owned CHR RAM. Refactored NROM, SxROM/MMC1, UxROM, and CNROM to use
the helpers, removed normal mapper hot-path logging, fixed MMC1 8 KiB CHR
low-bit masking, and made UxROM/CNROM bank selection safe.

Recorded before/after speedtest results in
`nes-py/docs/mapper-bank-helper-performance.md`.

## Verification

- `.venv/bin/python -m pip install -e .`
- `.venv/bin/python -m unittest nes_py.tests.test_mappers`
- `.venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `.venv/bin/python -m unittest discover .`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 100 --warmup-steps 20 --json --no-progress`
- `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/the-legend-of-zelda.nes --steps 100 --warmup-steps 20 --json --no-progress`

## Commits Pushed

- `nes-py`: `cc193bd` (`Add mapper bank helper windows`)

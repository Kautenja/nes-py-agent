# nes-py Cartridge Header and Memory Map Model

Completed work item `011-nes-py-cartridge-header-and-memory-map-model.md`.

## Summary

- Added Python and native cartridge metadata for mapper/submapper, NES 2.0 detection, PRG/CHR ROM sizes and banks, PRG/CHR RAM sizes, battery-backed RAM sizes, trainer offsets, mirroring, VS, PlayChoice, and PAL flags.
- Reworked native `Cartridge` validation to reject invalid magic, truncated headers, truncated payloads, trainer ROMs, and PAL ROMs deterministically during emulator loads.
- Widened native mapper storage beyond `NES_Byte`, separated battery-backed RAM metadata from ordinary RAM, allocated PRG RAM from header/default metadata, and represented four-screen mirroring distinctly.
- Added synthetic-header coverage without adding ROM assets.

## Verification

- `/tmp/gym-nes-ralph-venv/bin/python -m pip install -e .`
- `/tmp/gym-nes-ralph-venv/bin/python -m unittest nes_py.tests.test_cartridge_metadata`
- `/tmp/gym-nes-ralph-venv/bin/python -m unittest nes_py.tests.test_rom`
- `/tmp/gym-nes-ralph-venv/bin/python -m unittest nes_py.tests.test_nes_env`
- `/tmp/gym-nes-ralph-venv/bin/python -m unittest nes_py.tests.test_mappers`
- `/tmp/gym-nes-ralph-venv/bin/python -m unittest discover .`

The requested `python -m pip install -e .` command was run as `python3` in a temporary virtual environment because this machine has no `python` executable and the Homebrew-managed system Python rejects direct package installs.

## Commits

- `nes-py`: `1dc4313 Add cartridge header metadata model` pushed to `origin/ralph-dev`.

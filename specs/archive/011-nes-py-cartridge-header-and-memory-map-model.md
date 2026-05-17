# Specification: nes-py Cartridge Header and Memory Map Model

## Status: COMPLETE

## Problem

The native `Cartridge` parser and memory model are too small for the mapper queue. Future mapper specs require reliable iNES parsing, NES 2.0/submapper metadata where available, PRG RAM and save RAM sizes, trainer-aware offsets, CHR RAM sizing, four-screen mirroring, one-screen mapper mirroring, VS/PlayChoice flags, and variant data that both Python and C++ can agree on.

Today the Python `ROM` class validates more than the C++ `Cartridge`, while the native code trusts Python and keeps only PRG ROM, CHR ROM, a byte-sized mapper number, a mirroring byte, and a battery-derived `has_extended_ram` flag. This split makes Cython binding work harder and lets mapper implementations duplicate or guess header details.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required.
- Introduce a native cartridge metadata model that captures all header fields needed by the current mapper specs.
- Keep Python and native ROM parsing behavior aligned through shared tests and, where practical, shared constants.
- Fix PRG RAM modeling so RAM presence, RAM size, battery-backed persistence, and mapper-level write protection are separate concerns.
- Fix mirroring metadata so four-screen mirroring is not confused with mapper-defined one-screen modes.
- Preserve the existing user-facing rejection policy for unsupported ROM features unless this spec explicitly adds support and tests it.

## Required Metadata

The cartridge model should expose at least:

- mapper number with room for NES 2.0 expansion;
- submapper when the header is NES 2.0;
- PRG ROM byte size and bank count;
- CHR ROM byte size and bank count;
- CHR RAM byte size and battery-backed CHR RAM size when available;
- PRG RAM byte size and battery-backed PRG RAM byte size;
- trainer presence and data offset;
- mirroring mode from the header, with four-screen handled as its own mode;
- VS Unisystem, PlayChoice-10, PAL/NTSC, and NES 2.0 detection flags.

## Non-Goals

- Do not implement mapper-specific battery save files in this spec unless needed to separate RAM metadata safely.
- Do not add external ROM assets.
- Do not change game wrapper APIs.

## Acceptance Criteria

- [x] C++ `Cartridge` rejects invalid magic, truncated headers, truncated PRG/CHR payloads, and unsupported trainer/PAL cases with deterministic errors instead of relying only on Python prevalidation.
- [x] Python `ROM` and native `Cartridge` agree on mapper number, submapper, PRG/CHR sizes, RAM sizes, mirroring, trainer, battery, VS, PlayChoice, PAL, and NES 2.0 status for existing fixtures and synthetic headers.
- [x] Mapper number storage is widened beyond `NES_Byte` so mapper registration is not capped by the old byte-sized API.
- [x] PRG RAM allocation is based on header/default RAM size and mapper policy, not only battery-backed RAM.
- [x] Battery-backed RAM is represented separately from ordinary PRG RAM.
- [x] CHR RAM is represented as cartridge metadata, with default iNES CHR RAM behavior covered by tests.
- [x] Four-screen mirroring is represented distinctly and cannot fall through to one-screen lower mirroring when header bits combine.
- [x] Trainer offsets are parsed correctly in tests even if trainers remain unsupported by `NESEnv`.
- [x] The user-facing `NESEnv` validation remains clear and names the unsupported feature when rejecting a ROM.
- [x] Existing ROM tests still pass, and new synthetic-header tests cover edge cases without adding ROM assets.
- [x] No generated binaries, wheels, caches, or local virtual environments are committed.
- [x] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest nes_py.tests.test_rom
python -m unittest nes_py.tests.test_nes_env
python -m unittest nes_py.tests.test_mappers
python -m unittest discover .
```

If native C++ tests are added, also run the documented native test command for the active build system.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-cartridge-header-and-memory-map-model.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 1 -->

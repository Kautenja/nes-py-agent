# Specs

Ralph Wiggum reads root-level Markdown files in this directory.

Topic-specific queues such as `mappers/` and `gymapi/` are planning backlogs.
Promote or copy one of those specs to this root directory, or explicitly target
it in the Ralph prompt, when it should become active loop work.

Use numeric prefixes to express priority:

```text
001-first-important-task.md
002-next-task.md
```

Each spec should include concrete acceptance criteria and verification commands. A spec is complete only when it contains:

```markdown
## Status: COMPLETE
```

## Parallel Mapper Specs

Specs `031`, `032`, and `033` are intentionally scoped so they can run in
parallel when each run keeps to its mapper-specific files:

- `031` owns UxROM coverage in `nes-py/nes_emu/test/nes_emu/mappers/test_mapper_UxROM.cpp` and `nes-py/nes_py/tests/mappers/test_mapper_002_uxrom.py`.
- `032` owns NROM coverage in `nes-py/nes_emu/test/nes_emu/mappers/test_mapper_NROM.cpp` and `nes-py/nes_py/tests/mappers/test_mapper_000_nrom.py`.
- `033` owns CNROM coverage in `nes-py/nes_emu/test/nes_emu/mappers/test_mapper_CNROM.cpp` and `nes-py/nes_py/tests/mappers/test_mapper_003_cnrom.py`.

Shared native support helpers, mapper factory/registry wiring, build files,
history, completion logs, and the umbrella submodule pointer are coordination
points. Merge and push those sequentially after the mapper-specific submodule
work is complete.

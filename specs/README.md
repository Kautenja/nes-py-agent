# Specs

Ralph Wiggum reads root-level Markdown files in this directory.

Topic-specific queues such as `mappers/` and `envparity/` are planning
backlogs. Promote or copy one of those specs to this root directory, or
explicitly target it in the Ralph prompt, when it should become active loop
work.

Use numeric prefixes to express priority:

```text
001-first-important-task.md
002-next-task.md
```

Each spec should include concrete acceptance criteria and verification commands. A spec is complete only when it contains:

```markdown
## Status: COMPLETE
```

## Completion Archive

Completed root-level work should be retired from the live queue after its
history entry and completion log are written. Keep the durable context in
`history.md`, `CHANGELOG.md`, and focused notes under `history/` rather than
letting completed task bodies accumulate here.

`specs/archive/` is now intentionally lightweight. It exists as a pointer for
old archive context, not as the primary historical record.

## Active Root Queue

There are currently no incomplete root-level specs. Promote or copy a backlog
item into this directory when the next autonomous Ralph loop should work it.

## Active Mapper Queue

The mapper backlog remains available under `specs/mappers/`. Those specs are
not active root work unless promoted or explicitly targeted in the Ralph
prompt. The previously active mapper queue promoted the popular unsupported NES
mappers identified from the mapper backlog, excluding mapper 24 / VRC6:

| Prefix | Mapper | Anchor title |
| --- | --- | --- |
| `034` | MMC3 | `Super Mario Bros. 3 (USA)` |
| `035` | AxROM / AOROM | `Battletoads (USA)` |
| `036` | MMC5 | `Castlevania III - Dracula's Curse (USA)` |
| `037` | MMC2 | `Mike Tyson's Punch-Out!! (USA)` |
| `038` | Sunsoft FME-7 / Sunsoft 5B | `Batman - Return of the Joker (USA)` |

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

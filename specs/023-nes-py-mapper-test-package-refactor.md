# Specification: nes-py Mapper Test Package Refactor

## Problem

`nes-py/nes_py/tests/test_mappers.py` currently mixes mapper registry checks, native mapper lifecycle smoke tests, and mapper-specific characterization coverage for every supported mapper. That structure is already dense with mappers 0-3, and it will become difficult to review, navigate, and extend as the mapper implementation queue adds more console boards.

Mapper tests should be organized as a package where each canonical mapper test module owns exactly one mapper class/family. Shared test infrastructure should remain reusable, but mapper behavior should no longer accumulate in one monolithic file.

## Scope

- Work inside the `nes-py` submodule unless an umbrella gitlink update is required after committing the submodule.
- Refactor tests only; do not change emulator, ROM, mapper, or environment behavior except to fix a real issue exposed by moving the tests.
- Create a `nes_py/tests/mappers/` test package.
- Move shared mapper test helpers, constants, and base classes into package-local support modules such as `common.py` or `base.py`.
- Split the existing mapper-specific coverage into one canonical module per mapper class/family:
  - Mapper 000 / NROM coverage in a mapper 000 test module.
  - Mapper 001 / SxROM / MMC1 coverage in a mapper 001 test module.
  - Mapper 002 / UxROM coverage in a mapper 002 test module.
  - Mapper 003 / CNROM coverage in a mapper 003 test module.
- Move non-mapper-specific coverage, such as native mapper support registration and lifecycle/hook smoke tests, into clearly named package modules that are not treated as mapper class files.
- Retire `nes_py/tests/test_mappers.py` as the canonical home for mapper tests. If a temporary compatibility shim is kept for old unittest paths, it must not cause duplicate test execution during normal discovery and must clearly point to the package modules.
- Keep existing synthetic ROM fixture helpers in `nes_py/tests/mapper_fixtures.py` unless there is a strong reason to move them; if moved, preserve import compatibility for unrelated tests.
- Update local test documentation or active spec references that describe the mapper test entry point so future mapper specs use the package layout instead of adding back to `test_mappers.py`.
- Do not edit archived specs solely to update old verification snippets.

## Target Layout

Exact filenames may follow the existing project style, but the finished layout should make the one-to-one mapping obvious. A suggested layout is:

```text
nes_py/tests/mappers/
  __init__.py
  common.py
  test_registry.py
  test_lifecycle_hooks.py
  test_mapper_000_nrom.py
  test_mapper_001_sxrom.py
  test_mapper_002_uxrom.py
  test_mapper_003_cnrom.py
```

Future mapper work should add a new `test_mapper_NNN_name.py` module for the new native mapper class/family instead of editing a central mapper test file.

## Non-Goals

- Do not add new mapper implementations.
- Do not broaden mapper behavior coverage beyond what is needed to preserve the existing tests under the new layout.
- Do not rename production mapper classes or native source files.
- Do not download or add ROM assets.
- Do not convert the project away from `unittest`.

## Acceptance Criteria

- [ ] `nes_py/tests/mappers/` is a real Python test package with an `__init__.py`.
- [ ] Each currently implemented native mapper class/family has one canonical mapper test module under `nes_py/tests/mappers/`.
- [ ] Existing mapper-specific test assertions from `test_mappers.py` are preserved or made stricter; no coverage is silently dropped.
- [ ] Registry/support checks and lifecycle/hook smoke tests live in clearly named package modules separate from per-mapper modules.
- [ ] Shared helpers such as `MapperTestCase`, `_write_mmc1_register`, mirroring constants, and temporary ROM handling are available without circular imports or duplicated fixture code.
- [ ] `nes_py/tests/test_mappers.py` is removed or reduced to a non-duplicating compatibility shim with an explanatory module docstring.
- [ ] Normal unittest discovery runs the mapper package tests exactly once; compatibility imports, if present, do not duplicate test cases.
- [ ] Focused unittest invocations exist for both the whole mapper package and individual mapper modules.
- [ ] Active documentation or specs that instruct developers where mapper tests live point at the new package layout.
- [ ] Existing non-mapper test modules continue to import fixture helpers successfully.
- [ ] Generated build artifacts, caches, `.DS_Store`, eggs, wheels, compiled objects, local virtual environments, and commercial ROM downloads are not committed.
- [ ] The `nes-py` submodule commit is pushed before the umbrella repository records the updated submodule pointer.

## Verification

Run focused checks inside the submodule:

```sh
cd nes-py
python -m pip install -e .
python -m unittest discover nes_py/tests/mappers
python -m unittest nes_py.tests.mappers.test_registry
python -m unittest nes_py.tests.mappers.test_lifecycle_hooks
python -m unittest nes_py.tests.mappers.test_mapper_000_nrom
python -m unittest nes_py.tests.mappers.test_mapper_001_sxrom
python -m unittest nes_py.tests.mappers.test_mapper_002_uxrom
python -m unittest nes_py.tests.mappers.test_mapper_003_cnrom
python -m unittest discover nes_py/tests
```

If a compatibility shim remains at `nes_py.tests.test_mappers`, also verify it does not duplicate discovery results and document the intended removal path in the completion log.

## Completion Signal

When all acceptance criteria are met:

- Commit and push the `nes-py` submodule changes.
- Commit and push the umbrella repository's updated `nes-py` gitlink and any spec/documentation updates.
- Append the required one-line summary to `history.md`.
- Add the required `completion_log/YYYY-MM-DD--HH-MM-SS--nes-py-mapper-test-package-refactor.md` file.
- Output `DONE` only after all local verification passes and any required remote checks are green.

<!-- NR_OF_TRIES: 0 -->

# Mapper Spec Conversion Notes

`nes-py/nesmapper.txt` was retired after the mapper queue was split into the
per-mapper specs in this directory. The legacy file was useful for mapping ROM
titles to iNES mapper IDs, but it was not a normative hardware reference.

## Source Caveats

- The legacy catalog was broad, not complete; its preface specifically warned
  that some scarce Japanese ROMs were missing.
- The legacy mirroring column is advisory. Implementations and tests should
  prefer iNES/NES 2.0 header data, mapper documentation, and behavior observed
  from legal fixtures. If a title renders incorrectly, re-check mirroring rather
  than trusting the old table.
- Famicom Disk System and disk-to-NES conversion entries in the source often
  require a sidecar `.sav` file. Do not use those entries as ordinary cartridge
  fixtures unless a spec deliberately covers that conversion behavior.
- Source rows marked as bad dumps, incomplete dumps, hacked conversions, or
  mapper hacks should not be used as canonical acceptance fixtures unless the
  spec explicitly targets that edge case.
- Continue to use NESdev mapper pages and legally supplied local ROMs or
  redistributable homebrew test ROMs for implementation and verification. Do not
  add ROM download steps or commercial ROM assets.

## Conversion Audit

- The legacy table contains 1,597 ROM rows across 50 mapper IDs.
- Every mapper ID in the legacy table has a corresponding spec in this
  directory, and there are no spec mapper IDs absent from the legacy table.
- The per-spec approximate entry counts were cross-checked during retirement.
  NROM and CNROM were corrected to include formatting outliers in the legacy
  table.
- One old row, `Pac-Man (Unlicensed Version)`, used `J` in the mirroring column;
  treat that as another source-data warning rather than a real mirroring mode.

## Current Native Baseline

The archived mapper cleanup specs changed the native mapper baseline after this
queue was first generated:

- Mappers 0-3 already have synthetic characterization coverage that must be
  preserved through the post-refactor native test layout.
- Mapper lifetime, backup/restore cloning, IRQ callbacks, CPU/PPU hooks,
  expansion-area routing, PRG RAM hooks, nametable delegation, bus-conflict
  helpers, and shared PRG/CHR bank helpers now exist in the native core.
- Python mapper validation delegates to native support through
  `_native.is_mapper_supported`; implementation specs should update the native
  registry and verify that `NESEnv` observes the new support through that path.
- New mapper specs should register implementations through the native mapper
  registry, `MapperFactory`, and `IsMapperSupported`; do not refer to a
  `MapperID` enum unless one is introduced by the implementation itself.
- Verification commands should run the actual native test targets and Python
  mapper package modules present in the tree. The old generated
  `TestMapperNNN` class names were placeholders and do not exist in the current
  suite.

## Post-023 Test Layering

Mapper work in this backlog is expected to run after the mapper test package
and native test separation specs. C++ mapper correctness, native-internal edge
cases, synthetic ROM characterization, IRQ timing, backup/restore internals,
and performance-sensitive hook behavior belong in native C++ test runners or
benchmarks under `nes_emu/test/nes_emu/*` and
`nes_emu/benchmark/nes_emu/*`. Do not add Python private hooks or Python tests
whose purpose is to characterize C++ internals.

Every mapper still needs a Python application-layer test based on the
representative title named in its spec. The test should use the listed expected
local fixture path so a legal ROM can be dropped in later, skip only that
ROM-backed integration case when the file is absent, and exercise public
package behavior such as ROM/header metadata, `NESEnv` construction, reset,
short deterministic stepping, `rgb_array` rendering, close, and public
backup/restore behavior if that remains part of the package workflow.

## Priority Ordering

The numeric filename prefixes in this directory are the mapper work queue. This
backlog is numbered after the root-level specs through `029`, so individual
mapper specs are ready to promote or target without colliding with the active
root queue. Current ordering policy:

- Specs for mappers already present in the native core come first. These protect
  the compatibility baseline before new mapper work broadens the surface.
- Missing mapper implementations are then ordered by a mix of approximate legacy
  catalog coverage, representative title desirability, and implementation
  leverage across related mapper families.
- Hacked conversions, bootlegs, multicarts, and one-off boards are later unless
  the representative title or mapper family has unusually high value.
- Approximate entry counts come from the retired `nesmapper.txt` catalog and are
  directional, not authoritative.

| Prefix | Mapper | Approx. entries | Anchor title | Priority reason |
| --- | --- | ---: | --- | --- |
| `030` | MMC1 / SxROM | 449 | `The Legend of Zelda (USA)` | Already supported; largest baseline coverage. |
| `031` | UxROM / UNROM | 203 | `Mega Man (USA)` | Already supported; broad high-value baseline. |
| `032` | NROM | 149 | `Super Mario Bros. (USA)` | Already supported; canonical fixed-mapper baseline. |
| `033` | CNROM | 122 | `Adventure Island (USA)` | Already supported; common CHR-switching baseline. |
| `034` | MMC3 | 437 | `Super Mario Bros. 3 (USA)` | Largest missing implementation and major-library blocker. |
| `035` | AxROM / AOROM | 43 | `Battletoads (USA)` | Highest remaining count after MMC3, with popular games. |
| `036` | MMC5 | 11 | `Castlevania III - Dracula's Curse (USA)` | Small count, but very high desirability and important hardware. |
| `037` | Sunsoft FME-7 / Sunsoft 5B | 6 | `Batman - Return of the Joker (USA)` | High-value Sunsoft board family and notable titles. |
| `038` | Konami VRC6 | 1 | `Akumajou Densetsu (Japan)` | Very high desirability and expansion-audio relevance. |
| `039` | Konami VRC6V | 1 | `Mouryou Senki Madara (Japan)` | Related VRC6 work, valuable Konami coverage. |
| `040` | Konami VRC7 | 1 | `Lagrange Point (Japan)` | Very high desirability and expansion-audio relevance. |
| `041` | Namco 163 / Namcot 106 | 16 | `Splatterhouse - Wanpaku Graffiti (Japan)` | Solid count plus important Namco mapper/audio family. |
| `042` | Bandai | 18 | `Akuma-kun - Makai no Wana (Japan)` | Highest remaining count in a licensed mapper family. |
| `043` | Color Dreams | 16 | `Bible Adventures (USA) (Unl)` | Broad unlicensed catalog footprint. |
| `044` | Camerica | 12 | `Dizzy the Adventurer (USA) (Unl)` | Meaningful Codemasters/Camerica coverage. |
| `045` | Jaleco SS8806 | 9 | `Jajamaru no Gekimaden (Japan)` | Mid-sized licensed mapper family. |
| `046` | AVE / NINA | 9 | `Double Strike (USA) (Unl)` | Mid-sized unlicensed mapper family. |
| `047` | GxROM / 74161/32 | 7 | `Dragon Power (USA)` | Discrete mapper with several commercial titles. |
| `048` | BNROM / NINA-001 | 6 | `The 3-D Battles of WorldRunner (USA)` | Modest count with recognizable commercial titles. |
| `049` | Taito TC0190/TC0350 | 6 | `Don Doko Don (Japan)` | Licensed Taito mapper coverage. |
| `050` | MMC2 | 3 | `Mike Tyson's Punch-Out!! (USA)` | Very high desirability despite small count. |
| `051` | MMC4 | 2 | `Fire Emblem (Japan)` | Small count, but notable Nintendo mapper family. |
| `052` | Konami VRC2b / VRC4 | 5 | `Contra (Japan)` | Konami family coverage and desirable anchor. |
| `053` | Konami VRC4 | 2 | `Gradius II (Japan)` | Desirable Konami VRC follow-up. |
| `054` | Konami VRC4-2A | 2 | `Wai Wai World 2 (Japan)` | Related VRC follow-up. |
| `055` | Konami VRC4-1B | 1 | `TwinBee 3 (Japan)` | Related VRC follow-up. |
| `056` | TQROM | 4 | `High Speed (USA)` | MMC3-adjacent compatibility work. |
| `057` | Irem G-101 | 4 | `Image Fight (Japan)` | Licensed Irem mapper coverage. |
| `058` | RAMBO-1 | 3 | `Klax (USA)` | MMC3-like board with a small commercial set. |
| `059` | Sunsoft 4 | 3 | `After Burner II (Japan)` | Licensed Sunsoft follow-up. |
| `060` | Bandai 74161/32 | 3 | `Kamen Rider Club (Japan)` | Related Bandai/discrete follow-up. |
| `061` | VS Unisystem | 3 | `Vs. Super Mario Bros. (Japan, USA)` | Arcade variant support with recognizable anchor. |
| `062` | Irem H3001 | 2 | `Daiku no Gensan 2 (Japan)` | Long-tail licensed Irem coverage. |
| `063` | Holy Diver / 74161/32 | 1 | `Holy Diver (Japan)` | One-off, but a cult title. |
| `064` | Namco 118 | 1 | `Dragon Spirit (Japan)` | Namco commercial follow-up. |
| `065` | Namco 1xx | 1 | `Dragon Buster (Japan)` | Namco commercial follow-up. |
| `066` | Taito X005 | 1 | `Taito Grand Prix (Japan)` | Taito commercial follow-up. |
| `067` | Taito X1-017 | 4 | `Kyuukyoku Harikiri Stadium (Japan)` | More entries, but narrower title appeal. |
| `068` | Irem 74161/32 | 1 | `Crazy Climber (Japan)` | One-off licensed mapper. |
| `069` | Taito TC190V | 1 | `Sangokushi - Chuugen no Hasha 2 (Hacked)` | Hacked/specialty Taito tail. |
| `070` | FFE F8xxx | 8 | `Dynamite Batman 2 (Hacked)` | Hacked conversion family, lower canonical value. |
| `071` | FFE F4xxx | 7 | `Arabian Dream Scheherazade (Hacked)` | Hacked conversion family, lower canonical value. |
| `072` | FFE F3xxx | 2 | `Doraemon Kaitakuhen (Hacked)` | Hacked conversion family, lower canonical value. |
| `073` | Mapper 015 multicart | 3 | `100 In 1 - Contra Function 16` | Multicart work after canonical boards. |
| `074` | Mapper 090 bootleg | 2 | `Mortal Kombat 3` | Bootleg mapper with novelty value. |
| `075` | Mapper 225 multicart | 2 | `58 In 1` | Multicart long tail. |
| `076` | Mapper 227 multicart | 1 | `1200 In 1` | Multicart long tail. |
| `077` | Mapper 228 | 1 | `Action 52 (USA) (Unl)` | Infamous one-off, but low compatibility yield. |
| `078` | PC-Cony | 1 | `Garou Densetsu Special` | Bootleg one-off tail. |
| `079` | HK-SF3 | 1 | `Street Fighter III` | Bootleg one-off tail. |

## Retained Source Entry Notes

These notes preserve the legacy table's per-ROM caveats without keeping the
full title-to-mapper catalog in the `nes-py` package.

| Mapper | Source title | Note for spec work |
| --- | --- | --- |
| 0 | `Back to the Future` | Marked as a bad dump. |
| 0 | `Clu Clu Land disk-to-nes conv.` | Uses a `.sav` file to load. |
| 0 | `Ice Climber (disk conversion)` | Uses a `.sav` file to load. |
| 0 | `Ice Hockey (disk coversion)` | Uses a `.sav` file to load. |
| 0 | `Othello (Disk conversion)` | Loads using a `.sav` file. |
| 0 | `Soccer (Disk Conversion)` | Uses a `.sav` file to load. |
| 0 | `Super Mario Bros (Disk Conv.)` | Loads using a `.sav` file. |
| 0 | `Twinbee (Disk Conversion)` | Loads using a `.sav` file. |
| 0 | `Volleyball (Disk Conversion)` | Loads using a `.sav` file. |
| 1 | `Bard's Tale, The` | Marked as a possible bad dump. |
| 1 | `Bart vs. the Space Mutants` | Source suggests the dump may be missing 128 KiB of PRG. |
| 1 | `Conflict` | Marked as a bad dump. |
| 1 | `Final Fantasy I/II` | Source says the PRG size should be 512 KiB. |
| 1 | `Thunder and Lightning` | Marked as a bad dump. |
| 1 | `Zelda 2 - The Adventure of Link` | Source says the dump is missing 16 KiB. |
| 3 | `Smash Ping Pong (Disk Conv.)` | Uses a `.sav` file to load. |
| 4 | `Adventures of Rocky & Bullwinkle` | Source says the dump is missing 8 KiB. |
| 4 | `Home Alone` | Marked as probably a bad dump. |
| 4 | `Mad Max` | Marked as probably a bad dump. |
| 4 | `Smash TV` | Marked as probably an incomplete dump. |
| 4 | `Spider-Man` | Marked as a probable bad dump. |
| 4 | `Startropics` | Source notes the proper chip is MMC6, which was unsupported by the catalog. |
| 4 | `Startropics 2` | Source notes the proper chip is MMC6, which was unsupported by the catalog. |
| 4 | `Super C` | Source says the dump is missing another 8 KiB CHR page. |
| 4 | `Super Spike V'Ball/Nintendo World Cup` | Source says the dump may be missing about 256 KiB. |
| 4 | `Tetris 2` | Source says the dump is missing 24 KiB. |
| 16 | `Blue Train Satsujin Jiken` | Source says this may be a hacked version, since Irem made the game. |
| 19 | `Mindseeker` | Marked as a bad dump. |
| 34 | `Takahasi Meijin no Bug Hunny` | Marked as probably a mapper hack. |
| 71 | `Bee 52` | Marked as a bad dump. |
| 119 | `Pinbot` | Marked as a bad dump. |

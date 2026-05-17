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

#!/usr/bin/env python3
"""Import local NES ROM fixtures for mapper specs.

This script does not download ROMs or access the network. It reads the mapper
specs in this repository, scans a user-provided directory of local ROM dumps,
matches files by expected fixture name, representative title, and iNES mapper
ID, then copies matching files into nes-py's test fixture directory when
`--copy` is passed.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SPEC_GLOB = "*-nes-py-mapper-*.md"


@dataclass(frozen=True)
class SpecFixture:
    spec_path: str
    mapper: int
    title: str
    fixture: str
    catalog: str | None

    @property
    def expected_name(self) -> str:
        return Path(self.fixture).name


@dataclass(frozen=True)
class RomCandidate:
    path: str
    mapper: int
    prg_kb: int
    chr_kb: int
    source_archive: str | None = None

    @property
    def name(self) -> str:
        return Path(self.path).name


@dataclass(frozen=True)
class Match:
    spec: SpecFixture
    candidate: RomCandidate | None
    score: int
    status: str
    reason: str
    destination: str


def normalize(value: str) -> str:
    """Return a punctuation-insensitive token string for loose matching."""
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"\([^)]*\)", " ", value)
    value = re.sub(r"\[[^]]*\]", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    tokens = [token for token in value.split() if token not in {"the", "a", "an"}]
    return " ".join(tokens)


def parse_mapper_specs(specs_dir: Path) -> list[SpecFixture]:
    """Parse mapper fixture metadata from spec Markdown files."""
    specs: list[SpecFixture] = []
    for path in sorted(specs_dir.glob(SPEC_GLOB)):
        text = path.read_text(encoding="utf-8")
        mapper = re.search(r"- Mapper ID: `(\d+)`", text)
        title = re.search(r"- Representative test title: `([^`]+)`", text)
        fixture = re.search(r"- Expected local fixture: `([^`]+)`", text)
        catalog = re.search(r"- Emuparadise catalog (?:link|search): (\S+)", text)
        if not (mapper and title and fixture):
            continue
        specs.append(
            SpecFixture(
                spec_path=str(path),
                mapper=int(mapper.group(1)),
                title=title.group(1),
                fixture=fixture.group(1),
                catalog=catalog.group(1) if catalog else None,
            )
        )
    return specs


def parse_ines_header(path: Path) -> tuple[int, int, int]:
    """Return mapper, PRG KB, and CHR KB from an iNES ROM header."""
    with path.open("rb") as handle:
        header = handle.read(16)
    if len(header) < 16 or header[:4] != b"NES\x1a":
        raise ValueError("not an iNES ROM")
    mapper = (header[7] & 0xF0) | (header[6] >> 4)
    prg_kb = header[4] * 16
    chr_kb = header[5] * 8
    return mapper, prg_kb, chr_kb


def extract_zip_roms(archive: Path, temp_dir: Path) -> Iterable[Path]:
    """Extract .nes entries from a ZIP archive into temp_dir."""
    with zipfile.ZipFile(archive) as zipped:
        for info in zipped.infolist():
            if info.is_dir() or not info.filename.lower().endswith(".nes"):
                continue
            target = temp_dir / archive.stem / Path(info.filename).name
            target.parent.mkdir(parents=True, exist_ok=True)
            with zipped.open(info) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)
            yield target


def scan_candidates(source_dir: Path, temp_dir: Path) -> list[RomCandidate]:
    """Scan source_dir recursively for .nes files and .zip archives."""
    candidates: list[RomCandidate] = []
    paths = sorted(source_dir.rglob("*"))
    for path in paths:
        if not path.is_file():
            continue
        rom_paths: list[tuple[Path, str | None]]
        if path.suffix.lower() == ".nes":
            rom_paths = [(path, None)]
        elif path.suffix.lower() == ".zip":
            rom_paths = [(rom, str(path)) for rom in extract_zip_roms(path, temp_dir)]
        else:
            continue
        for rom_path, archive in rom_paths:
            try:
                mapper, prg_kb, chr_kb = parse_ines_header(rom_path)
            except ValueError:
                continue
            candidates.append(
                RomCandidate(
                    path=str(rom_path),
                    mapper=mapper,
                    prg_kb=prg_kb,
                    chr_kb=chr_kb,
                    source_archive=archive,
                )
            )
    return candidates


def score_candidate(spec: SpecFixture, candidate: RomCandidate) -> int:
    """Score a ROM candidate for a spec. Zero means no useful match."""
    if spec.mapper != candidate.mapper:
        return 0

    source_name = normalize(Path(candidate.path).stem)
    expected_stem = normalize(Path(spec.expected_name).stem)
    title = normalize(spec.title)

    score = 10
    if Path(candidate.path).name == spec.expected_name:
        score += 100
    if source_name == expected_stem:
        score += 90
    if source_name == title:
        score += 80
    if expected_stem and expected_stem in source_name:
        score += 50
    if title and title in source_name:
        score += 45
    if source_name and source_name in title:
        score += 35
    if any(token and token in source_name for token in title.split()):
        score += 5
    return score


def choose_matches(
    specs: list[SpecFixture],
    candidates: list[RomCandidate],
    nes_py_dir: Path,
    min_score: int,
) -> list[Match]:
    """Choose the best candidate for each mapper spec."""
    matches: list[Match] = []
    for spec in specs:
        destination = str(nes_py_dir / spec.fixture)
        ranked = sorted(
            (
                (score_candidate(spec, candidate), candidate)
                for candidate in candidates
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        ranked = [(score, candidate) for score, candidate in ranked if score >= min_score]
        if not ranked:
            matches.append(
                Match(spec, None, 0, "missing", "no candidate matched title and mapper", destination)
            )
            continue
        best_score, best = ranked[0]
        if len(ranked) > 1 and ranked[1][0] == best_score:
            matches.append(
                Match(spec, None, best_score, "ambiguous", "multiple candidates tied", destination)
            )
            continue
        matches.append(Match(spec, best, best_score, "matched", "best candidate", destination))
    return matches


def copy_matches(matches: list[Match], overwrite: bool) -> None:
    """Copy matched candidates to destinations."""
    for match in matches:
        if match.status != "matched" or match.candidate is None:
            continue
        destination = Path(match.destination)
        if destination.exists() and not overwrite:
            print(f"skip existing: {destination}", file=sys.stderr)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(match.candidate.path, destination)


def print_report(matches: list[Match]) -> None:
    """Print a compact human-readable report."""
    for match in matches:
        spec = match.spec
        prefix = f"mapper {spec.mapper:03d} -> {spec.expected_name}"
        if match.status == "matched" and match.candidate:
            source = match.candidate.source_archive or match.candidate.path
            print(f"MATCH {prefix}: {source} (score={match.score})")
        elif match.status == "ambiguous":
            print(f"AMBIG {prefix}: {match.reason} (score={match.score})")
        else:
            print(f"MISS  {prefix}: {spec.title}")
            if spec.catalog:
                print(f"      catalog: {spec.catalog}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, help="Directory containing local .nes files or .zip archives.")
    parser.add_argument("--specs-dir", type=Path, default=Path("specs"), help="Directory containing mapper specs.")
    parser.add_argument("--nes-py-dir", type=Path, default=Path("nes-py"), help="Path to the nes-py submodule.")
    parser.add_argument("--copy", action="store_true", help="Copy matched ROMs. Omit for dry-run report only.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing destination files when copying.")
    parser.add_argument("--min-score", type=int, default=50, help="Minimum match score to accept.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a human report.")
    args = parser.parse_args(argv)

    source_dir = args.source_dir.expanduser().resolve()
    specs_dir = args.specs_dir.resolve()
    nes_py_dir = args.nes_py_dir.resolve()

    if not source_dir.is_dir():
        parser.error(f"source_dir is not a directory: {source_dir}")
    if not specs_dir.is_dir():
        parser.error(f"specs-dir is not a directory: {specs_dir}")
    if not nes_py_dir.is_dir():
        parser.error(f"nes-py-dir is not a directory: {nes_py_dir}")

    specs = parse_mapper_specs(specs_dir)
    if not specs:
        parser.error(f"no mapper specs found in {specs_dir}")

    with tempfile.TemporaryDirectory(prefix="mapper-rom-fixtures-") as temp:
        candidates = scan_candidates(source_dir, Path(temp))
        matches = choose_matches(specs, candidates, nes_py_dir, args.min_score)
        if args.copy:
            copy_matches(matches, args.overwrite)

        if args.json:
            print(json.dumps([asdict(match) for match in matches], indent=2))
        else:
            print_report(matches)
            if not args.copy:
                print("\nDry run only. Re-run with --copy to copy matched ROMs.")

    unmatched = sum(1 for match in matches if match.status != "matched")
    return 1 if unmatched else 0


if __name__ == "__main__":
    raise SystemExit(main())

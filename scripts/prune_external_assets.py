#!/usr/bin/env python3
"""Remove unreferenced files from output/ejemplos/external.

The script scans every HTML file under the given output directory, finds
references to files living under the external/ folder, and deletes any external
files that are not referenced. Run with --dry-run (default) to see what would be
removed, then re-run with --delete to actually clean up.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Iterable, Set
from urllib.parse import unquote

EXTERNAL_PATTERN = re.compile(r"external/[^\s\"'()<>]+")


def find_external_references(directory: pathlib.Path) -> Set[str]:
    """Return all external/* references found in HTML files under directory."""
    references: Set[str] = set()
    for html_file in directory.rglob("*.html"):
        try:
            text = html_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = html_file.read_text(errors="ignore")
        for match in EXTERNAL_PATTERN.finditer(text):
            raw = match.group(0)
            decoded = unquote(raw)
            # Normalize repeated slashes and resolve simple "./" segments.
            normalized = pathlib.PurePosixPath(decoded).as_posix()
            if not normalized.startswith("external/"):
                continue
            references.add(normalized)
    return references


def iter_external_files(external_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in external_dir.rglob("*"):
        if path.is_file():
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path("output/ejemplos"),
        help=(
            "Directory that contains index.html and the external folder. "
            "If a relative path is provided, it is resolved relative to the "
            "repository root (the parent of this script)."
        ),
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete unreferenced files. Without this flag the script only reports them.",
    )
    args = parser.parse_args()

    script_dir = pathlib.Path(__file__).resolve().parent
    repo_root = script_dir.parent
    base_dir = args.root
    if not base_dir.is_absolute():
        base_dir = (repo_root / base_dir).resolve()
    external_dir = base_dir / "external"
    if not external_dir.is_dir():
        print(f"External directory not found: {external_dir}", file=sys.stderr)
        return 1

    referenced = find_external_references(base_dir)
    unused_files = []
    for file_path in iter_external_files(external_dir):
        rel = file_path.relative_to(base_dir).as_posix()
        if rel not in referenced:
            unused_files.append(file_path)

    if not unused_files:
        print("No unreferenced files found.")
        return 0

    print("Unreferenced files:")
    for file_path in sorted(unused_files):
        print(f" - {file_path}")

    if args.delete:
        for file_path in unused_files:
            file_path.unlink()
        print(f"Deleted {len(unused_files)} file(s).")
    else:
        print("Re-run with --delete to remove these files.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

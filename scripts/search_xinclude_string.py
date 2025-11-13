#!/usr/bin/env python3
"""
Recursive xi:include-aware string search for PTX sources.

This script was created for the IllustrativeMath-GrupoLEMA project to help track
where a particular string appears when starting from a top-level PTX file that
pulls in additional content via xi:include.

Usage:
    python search_xinclude_string.py source/v00/gra0-uni2.ptx centro-cubosEncajables

Arguments:
    root_file   The starting PTX file whose xi:include graph will be traversed.
    needle      The literal string to search for in every discovered file.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Iterable, Iterator, List, Set, Tuple
import xml.etree.ElementTree as ET

XI_NAMESPACE = "http://www.w3.org/2001/XInclude"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search a PTX file and all xi:include targets for a literal string."
    )
    parser.add_argument("root_file", help="Path to the PTX file that kicks off the xi:include graph.")
    parser.add_argument("needle", help="Literal string to look for in every visited file.")
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding for reading PTX files (default: %(default)s).",
    )
    return parser.parse_args()


def iter_xinclude_tree(root: Path) -> Iterator[Path]:
    queue: Deque[Path] = deque([root.resolve()])
    seen: Set[Path] = set()

    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        yield current

        try:
            tree = ET.parse(current)
        except ET.ParseError as exc:
            print(f"Warning: could not parse {current}: {exc}", file=sys.stderr)
            continue

        includes = tree.findall(".//{http://www.w3.org/2001/XInclude}include")
        for include in includes:
            href = include.get("href")
            if not href:
                continue
            target = (current.parent / href).resolve()
            if target.exists():
                queue.append(target)
            else:
                print(f"Warning: include target not found ({href}) referenced from {current}", file=sys.stderr)


def find_literal_matches(path: Path, needle: str, encoding: str) -> List[Tuple[int, str]]:
    matches: List[Tuple[int, str]] = []
    try:
        with path.open(encoding=encoding) as handle:
            for line_no, line in enumerate(handle, start=1):
                if needle in line:
                    matches.append((line_no, line.rstrip()))
    except OSError as exc:
        print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
    return matches


def to_relative_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


def print_grouped_results(results: List[Tuple[Path, int, str]]) -> None:
    if not results:
        print("No matches found.")
        return

    grouped: defaultdict[Path, List[Tuple[str, int, str]]] = defaultdict(list)
    for file_path, line_no, content in results:
        rel_path = to_relative_path(file_path)
        parent = rel_path.parent if rel_path.parent != Path("") else Path(".")
        grouped[parent].append((rel_path.name, line_no, content))

    for directory in sorted(grouped, key=lambda p: str(p)):
        dir_display = "." if directory in (Path("."), Path("")) else str(directory)
        suffix = "/" if dir_display != "." else "/"
        print(f"{dir_display}{suffix}")
        for filename, line_no, content in sorted(grouped[directory], key=lambda item: (item[0], item[1])):
            cleaned = content.lstrip()
            print(f"  {filename}:{line_no}:")
            print(f"    | {cleaned}")
        print()


def main() -> None:
    args = parse_args()
    root = Path(args.root_file)

    if not root.exists():
        print(f"Error: {root} does not exist.", file=sys.stderr)
        sys.exit(1)

    matches: List[Tuple[Path, int, str]] = []
    for file_path in iter_xinclude_tree(root):
        for line_no, content in find_literal_matches(file_path, args.needle, args.encoding):
            matches.append((file_path, line_no, content))

    print_grouped_results(matches)


if __name__ == "__main__":
    main()

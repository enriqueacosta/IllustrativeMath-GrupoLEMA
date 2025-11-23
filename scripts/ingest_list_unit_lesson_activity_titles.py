#!/usr/bin/env python3
"""
Extract lesson and section titles for a unit.

For each lesson HTML file inside a unit directory, this script prints a
tab-delimited summary suitable for spreadsheet import:

    Lesson N<TAB>Lesson title
    Warm-up: ...<TAB>...
    Activity ...<TAB>...
    ...

Only Warm-up, Activity, and Cool-down headings are included. Every line is
split at the last colon so column 2 never contains ':'.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

from bs4 import BeautifulSoup  # type: ignore


HERO_CLASS = "im-c-hero__heading im-c-hero__heading--mdb"
SECTION_PREFIXES = ("Warm-up", "Activity", "Cool-down")
TIME_PATTERN = re.compile(r"\s*\(\d+\s+minutes?\)\s*$")


def extract_lessons(unit_dir: Path) -> List[List[Tuple[str, str]]]:
    """
    Return a list of lessons, where each lesson is a list of (col1, col2) rows.
    """
    lessons: List[List[Tuple[str, str]]] = []
    for lesson_dir in sorted(unit_dir.glob("lesson-*")):
        lesson_file = lesson_dir / "lesson.html"
        if not lesson_file.exists():
            continue
        lesson_rows = parse_lesson(lesson_file)
        if lesson_rows:
            lessons.append(lesson_rows)
    return lessons


def parse_lesson(html_path: Path) -> List[Tuple[str, str]]:
    """Parse a lesson.html and return rows for the spreadsheet."""
    text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    rows: List[Tuple[str, str]] = []
    title_heading = soup.find("h1")
    if title_heading:
        lesson_label = title_heading.get_text(strip=True)
        title = ""
        title_para = title_heading.find_next("p", class_="im-c-heading im-c-heading--xlb")
        if title_para:
            title = title_para.get_text(strip=True)
        rows.append((lesson_label, title))

    for heading in soup.find_all("h2", class_=HERO_CLASS):
        text_content = heading.get_text(strip=True)
        text_content = TIME_PATTERN.sub("", text_content)
        if not text_content.startswith(SECTION_PREFIXES):
            continue
        left, right = split_last_colon(text_content)
        rows.append((left, right))

    return rows


def split_last_colon(text: str) -> Tuple[str, str]:
    """Return text split at the last colon; second value is empty if none."""
    if ":" not in text:
        return text.strip(), ""
    left, right = text.rsplit(":", 1)
    return left.strip(), right.strip()


def format_rows(lessons: Sequence[Sequence[Tuple[str, str]]]) -> str:
    """Format rows with blank lines between lessons."""
    lines: List[str] = []
    for idx, lesson_rows in enumerate(lessons):
        if idx > 0:
            lines.append("")
        for col1, col2 in lesson_rows:
            lines.append(f"{col1}\t{col2}")
    return "\n".join(lines)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract tab-delimited lesson summaries for an Illustrative Math unit."
    )
    parser.add_argument(
        "unit_dir",
        type=Path,
        help="Path to the unit directory (contains lesson-*/lesson.html).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional file to write the summary to instead of stdout.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    if not args.unit_dir.exists():
        raise SystemExit(f"Unit directory not found: {args.unit_dir}")

    lessons = extract_lessons(args.unit_dir)
    if not lessons:
        raise SystemExit(f"No lesson files found in {args.unit_dir}")

    output_text = format_rows(lessons)

    if args.output:
        args.output.write_text(output_text, encoding="utf-8")
    else:
        print(output_text)


if __name__ == "__main__":
    main()

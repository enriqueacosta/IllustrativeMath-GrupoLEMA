#!/usr/bin/env python3
"""
update_lec_ccss.py
==================

Utility script to update the CCSS list inside a ``lec-*.ptx`` lesson file.
It inspects the warm-up and activity files that the lesson includes and
collects their Addressing and Building standards.  The script then replaces
the lesson's CCSS paragraph with the aggregated list so that the lesson
summary accurately reflects its content.

Usage
-----

    python SCRIPTS/update_lec_ccss.py source/content/lec-explicarConteo.ptx
"""

from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, Sequence


# --------------------------------------------------------------------------- #
# Regular-expression helpers
# --------------------------------------------------------------------------- #

# The CCSS block we will replace inside the lesson.
CCSS_BLOCK_PATTERN = re.compile(
    r"<!-- Estándares CCSS asociados -->.*?</paragraphs>", re.S
)

# ``<xi:include href="./filename.ptx"/>`` tags inside the lesson.
INCLUDE_PATTERN = re.compile(r'<xi:include href="\./([^"]+)"')

# Addressing / Building list items inside a warm-up or activity.
ADDRESSING_PATTERN = re.compile(
    r'<li>\s*<custom ref="ccss-addressing"\s*/>(.*?)</li>', re.S
)
BUILDING_PATTERN = re.compile(
    r'<li>\s*<custom ref="ccss-building"\s*/>(.*?)</li>', re.S
)

# ``<xref ...>K.CC.B.4</xref>`` tags from which we extract the actual codes.
XREF_PATTERN = re.compile(r'<xref[^>]*>([^<]+)</xref>')

# Some lesson includes (materials, center wrappers, etc.) do not contain CCSS
# metadata.  We skip them entirely to avoid polluting the results.
SKIP_SUFFIXES = ("-mat.ptx", "-matCentros.ptx", "-reto.ptx")
SKIP_PREFIXES = ("cool-", "PP-")
SKIP_CONTAINS = ("centros-escoger",)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def parse_args() -> Path:
    """Parse the command-line arguments and return the lesson path."""
    parser = argparse.ArgumentParser(
        description="Update the CCSS section in a lec-*.ptx file."
    )
    parser.add_argument("lesson", type=Path, help="Path to the lec-*.ptx file.")
    args = parser.parse_args()

    if not args.lesson.exists():
        raise FileNotFoundError(f"Lesson file not found: {args.lesson}")
    return args.lesson


def unique(seq: Iterable[str]) -> list[str]:
    """Return values in *seq* preserving their first occurrence."""
    ordered: OrderedDict[str, None] = OrderedDict()
    for value in seq:
        clean = value.strip()
        if clean and clean not in ordered:
            ordered[clean] = None
    return list(ordered.keys())


def gather_codes(text: str, pattern: re.Pattern[str]) -> list[str]:
    """Extract CCSS codes from warm-up/activity text using *pattern*."""
    codes: list[str] = []
    for block in pattern.findall(text):
        codes.extend(XREF_PATTERN.findall(block))
    return codes


def code_to_ref(code: str) -> str:
    """
    Convert a CCSS code (e.g. ``K.CC.B.4``) to the ``ccss-...`` reference id
    used within the project.
    """
    cleaned = code.replace("\u2013", "-").replace("–", "-").replace(" ", "")
    return "ccss-" + cleaned.replace(".", "-").replace("/", "-")


def should_skip(filename: str) -> bool:
    """Return True if *filename* should not be considered for CCSS data."""
    if filename.endswith(SKIP_SUFFIXES):
        return True
    if filename.startswith(SKIP_PREFIXES):
        return True
    return any(token in filename for token in SKIP_CONTAINS)


def collect_included_files(lesson_text: str) -> list[str]:
    """Return the list of included warm-up/activity filenames to inspect."""
    includes = []
    for fname in INCLUDE_PATTERN.findall(lesson_text):
        if should_skip(fname):
            continue
        includes.append(fname)
    return includes


def collect_codes_from_includes(
    base_dir: Path, filenames: Sequence[str]
) -> tuple[list[str], list[str]]:
    """
    Read each include in *filenames* (relative to *base_dir*) and collect the
    Addressing and Building codes present in their CCSS blocks.
    """
    addressing: list[str] = []
    building: list[str] = []

    for fname in filenames:
        include_path = base_dir / fname
        if not include_path.exists():
            print(f"Warning: included file not found (skipping) -> {include_path}")
            continue

        text = include_path.read_text(encoding="utf-8")
        addressing.extend(gather_codes(text, ADDRESSING_PATTERN))
        building.extend(gather_codes(text, BUILDING_PATTERN))

    return unique(addressing), unique(building)


def build_ccss_block(addressing: list[str], building: list[str]) -> str:
    """
    Construct the new CCSS paragraph block using the aggregated Addressing and
    Building lists.
    """
    lines = [
        "  <!-- Estándares CCSS asociados -->",
        "  <paragraphs>",
        '    <title><custom ref="ccss-leccion-titulo"/></title> ',
        "    <ul>",
    ]

    if addressing:
        joined = ", ".join(
            f'<xref ref="{code_to_ref(code)}" text="custom">{code}</xref>'
            for code in addressing
        )
        lines.extend(
            [
                "      <li>",
                '        <custom ref="ccss-addressing"/>',
                f"        {joined}",
                "      </li>",
            ]
        )

    if building:
        joined = ", ".join(
            f'<xref ref="{code_to_ref(code)}" text="custom">{code}</xref>'
            for code in building
        )
        lines.extend(
            [
                "      <li>",
                '        <custom ref="ccss-building"/>',
                f"        {joined}",
                "      </li>",
            ]
        )

    lines.extend(["    </ul>", "  </paragraphs>"])
    return "\n".join(lines)


def update_lesson_ccss(lesson_path: Path) -> None:
    """
    Aggregate CCSS codes from the lesson's includes and replace the lesson's
    CCSS paragraph with the updated content.
    """
    lesson_text = lesson_path.read_text(encoding="utf-8")
    base_dir = lesson_path.parent

    include_files = collect_included_files(lesson_text)
    addressing, building = collect_codes_from_includes(base_dir, include_files)

    if not addressing and not building:
        print("No CCSS codes found in included files; nothing to update.")
        return

    new_block = build_ccss_block(addressing, building)

    updated_text, count = CCSS_BLOCK_PATTERN.subn(new_block, lesson_text)
    if count == 0:
        # The lesson did not previously have a CCSS block; insert a new one
        # immediately after the introduction tag.
        intro_tag = '<introduction component="profesor">'
        if intro_tag not in lesson_text:
            raise ValueError(
                "Could not find existing CCSS block or introduction tag to insert into."
            )
        updated_text = lesson_text.replace(f"{intro_tag}", f"{intro_tag}\n{new_block}", 1)

    lesson_path.write_text(updated_text, encoding="utf-8")

    # Provide a concise summary for the caller.
    print(f"Updated CCSS block in {lesson_path}")
    if addressing:
        print("  Addressing:", ", ".join(addressing))
    if building:
        print("  Building:", ", ".join(building))


def main() -> None:
    lesson_path = parse_args()
    update_lesson_ccss(lesson_path)


if __name__ == "__main__":
    main()

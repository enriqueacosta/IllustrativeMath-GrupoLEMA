#!/usr/bin/env python3
"""Import practice problems for a K-5 unit practice.html into PreTeXt.

This script automates the steps  performed manually for sections A–D of
gra0-uni2:

  * Parse the archived `practice.html` file.
  * Extract each “Problem/Solution” pair beneath a given section header.
  * Copy every referenced figure into the local `source/assets` tree.
  * Emit brand-new `PP-*.ptx` files containing the statement/solution content,
    flagging every solution with `[++++++++++++++]` at the top.
  * Refresh the list of `<xi:include>` entries inside the section-level
    `gra0-uni2-secX-ProblemasPractica.ptx` wrappers so they include the
    newly-generated problems (when the wrapper exists and is empty).

Usage
=====
    python3 scripts/ingest_unit_PPs.py \
        --html /path/to/practice.html \
        --sections A,B,C,D

Arguments:
  --html          Absolute path to the archived practice.html file.
  --sections      Comma-separated list of section letters to import.
  --project-root  (optional) Root of the repository; defaults to cwd.

Assumptions / Limitations
=========================
  * The HTML structure matches what is observed for gra0-uni2:
    each Section header is followed by alternating “Problem” and “Solution”
    rows, with content inside `div.im-c-content`.
  * All figures referenced in the HTML point into the downloaded `figures/`
    directory tree (either SVG or PNG/JPG). The script copies those files
    verbatim into `source/assets/{svg,png,jpg}-source/` and refuses to run if
    an asset with the same filename already exists (to avoid clobbering art).
  * The script always creates NEW PreTeXt files with fresh UUID-derived IDs.
    It does not attempt to reuse or update existing PP files.
  * Solutions always get a `[++++++++++++++]` flag inserted as the first
    paragraph, regardless of language. Adjust here if you need a different
    marker.
  * Section wrappers must still contain the placeholder comments (i.e. no
    existing `<xi:include>` entries). The script bails out rather than
    overwriting hand-curated lists. If a wrapper file is missing (common for
    Section A in early units), the script simply skips that section.
  * All extracted text is wrapped in `<p>` tags; list items become
    `<li><p>…</p></li>`. Tweak `_render_element` if more control is needed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from bs4 import BeautifulSoup, NavigableString, Tag

SOLUTION_FLAG = "[++++++++++++++++++++]"

ASSET_DIR_MAP = {
    ".svg": "svg-source",
    ".png": "png-source",
    ".jpg": "jpg-source",
    ".jpeg": "jpg-source",
}
"""Mapping from file extension to destination assets subdirectory."""

SECTION_FILES = {
    "A": "source/v00/gra0-uni2-secA-ProblemasPractica.ptx",
    "B": "source/v00/gra0-uni2-secB-ProblemasPractica.ptx",
    "C": "source/v00/gra0-uni2-secC-ProblemasPractica.ptx",
    "D": "source/v00/gra0-uni2-secD-ProblemasPractica.ptx",
}
"""Section letter to relative section-wrapper path."""


@dataclass
class ProblemBlock:
    section: str
    number: str
    statement: Tag
    solution: Tag


class PracticeImporter:
    """Driver for parsing HTML and emitting PP files for selected sections."""

    def __init__(self, html_path: Path, project_root: Path, sections: Sequence[str]):
        self.html_path = html_path
        self.project_root = project_root
        self.sections = sections
        self.soup = BeautifulSoup(self.html_path.read_text(), "html.parser")
        self.asset_cache: dict[str, str] = {}

    def run(self) -> None:
        for section in self.sections:
            print(f"Processing Section {section} …")
            problems = self._extract_section(section)
            if not problems:
                print(f"  No problems found for Section {section}. Skipping.")
                continue

            include_ids: List[str] = []
            for block in problems:
                xml_id = self._write_exercise(block)
                include_ids.append(xml_id)
                print(f"    Wrote {xml_id}.ptx")

            if self._update_section_file(section, include_ids):
                print(f"  Updated section file with {len(include_ids)} includes.")
            else:
                print("  Skipped section wrapper update (see warning above).")

    # ------------------------------------------------------------------
    # Extraction helpers

    def _extract_section(self, section: str) -> List[ProblemBlock]:
        """Collect Problem/Solution pairs from a Section header."""
        header = self.soup.find(
            "h3",
            class_="im-c-row-header__heading",
            string=lambda text: text and text.strip().startswith(f"Section {section}:"),
        )
        if not header:
            return []

        row_header = header.parent.parent  # div.im-c-row-header
        rows: List[Tag] = []
        node = row_header.next_sibling
        while node:
            if isinstance(node, NavigableString):
                node = node.next_sibling
                continue
            classes = node.get("class", [])
            if node.name == "div" and "im-c-row-header" in classes:
                break
            if node.name == "div" and any(cls.startswith("im-c-row") for cls in classes):
                rows.append(node)
            node = node.next_sibling

        problems: List[ProblemBlock] = []
        for idx in range(0, len(rows), 2):
            try:
                problem_row = rows[idx]
                solution_row = rows[idx + 1]
            except IndexError:
                break

            title_tag = problem_row.find("h3", class_="im-c-heading--xsb")
            number = title_tag.get_text(strip=True) if title_tag else f"Problem {idx // 2 + 1}"

            statement = problem_row.find("div", class_="im-c-content")
            solution = solution_row.find("div", class_="im-c-content")
            if not statement or not solution:
                continue

            problems.append(
                ProblemBlock(
                    section=section,
                    number=number,
                    statement=statement,
                    solution=solution,
                )
            )

        return problems

    # ------------------------------------------------------------------
    # Rendering helpers

    def _write_exercise(self, block: ProblemBlock) -> str:
        code = uuid.uuid4().hex[:16]
        xml_id = f"PP-{code}"
        statement_lines = self._render_children(block.statement, indent="  ")
        solution_lines = self._render_children(block.solution, indent="  ")
        solution_lines.insert(0, f"  <p>{SOLUTION_FLAG}</p>")

        statement_body = "\n".join(statement_lines) if statement_lines else "  <p></p>"
        solution_body = "\n".join(solution_lines) if solution_lines else f"  <p>{SOLUTION_FLAG}</p>"

        content = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            f"<exercise xml:id=\"{xml_id}\" xmlns:xi=\"http://www.w3.org/2001/XInclude\">\n"
            "<!-- ============================================ \n"
            "  Problema asociado a una sección (no lección)\n"
            "=================================================  -->\n\n"
            "<!-- <title>Previo a la unidad</title> -->\n"
            "<!-- <title>Exploración</title> -->\n"
            "<!-- <title component=\"metadata\">Alineado con <xref ref=\"graVV-uniYY-secZZ\" text=\"title\"/></title> -->\n"
            "<title component=\"metadata\">Alineado con <xref ref=\"lec-VVVVVV\" text=\"title\"/></title>\n\n"
            "<statement>\n"
            f"{statement_body}\n"
            "</statement>\n\n"
            "<solution>\n"
            f"{solution_body}\n"
            "</solution>\n\n"
            "</exercise>\n"
        )

        dest = self.project_root / "source" / "content" / f"{xml_id}.ptx"
        dest.write_text(content)
        return xml_id

    def _render_children(self, container: Tag, indent: str) -> List[str]:
        """Traverse all DOM children, emitting strings of PreTeXt markup."""
        lines: List[str] = []
        buffer: List[str] = []

        def flush_buffer() -> None:
            if not buffer:
                return
            text = self._normalize_whitespace(" ".join(buffer))
            if text:
                lines.append(f"{indent}<p>{text}</p>")
            buffer.clear()

        for child in container.children:
            if isinstance(child, NavigableString):
                text = self._normalize_whitespace(str(child))
                if text:
                    buffer.append(text)
                continue

            if not isinstance(child, Tag):
                continue

            if child.name in {"div", "span"}:
                lines.extend(self._render_children(child, indent))
                continue

            flush_buffer()
            lines.extend(self._render_element(child, indent))

        flush_buffer()
        return lines

    def _render_element(self, node: Tag, indent: str) -> List[str]:
        """Render a single DOM node into PreTeXt markup."""
        if node.name == "p":
            text = self._extract_inline_text(node)
            if not text:
                return []
            return [f"{indent}<p>{text}</p>"]

        if node.name == "ol":
            lines = [f"{indent}<ol>"]
            for li in node.find_all("li", recursive=False):
                lines.append(f"{indent}  <li>")
                lines.extend(self._render_children(li, indent + "    "))
                lines.append(f"{indent}  </li>")
            lines.append(f"{indent}</ol>")
            return lines

        if node.name == "ul":
            lines = [f"{indent}<ul>"]
            for li in node.find_all("li", recursive=False):
                lines.append(f"{indent}  <li>")
                lines.extend(self._render_children(li, indent + "    "))
                lines.append(f"{indent}  </li>")
            lines.append(f"{indent}</ul>")
            return lines

        if node.name == "figure" or node.name == "image" or node.name == "img":
            image_lines = self._render_image(node, indent)
            return image_lines

        if node.name == "br":
            return []

        # Fallback: render its children.
        return self._render_children(node, indent)

    def _render_image(self, node: Tag, indent: str) -> List[str]:
        img = node if node.name == "img" else node.find("img")
        if not img:
            return []
        src = img.get("src")
        if not src:
            return []
        asset_path = self._copy_asset(src)
        alt = img.get("alt", "").strip()
        lines = [f"{indent}<image source=\"{asset_path}\">"]
        if alt:
            lines.append(f"{indent}  <shortdescription>{alt}</shortdescription>")
        lines.append(f"{indent}</image>")
        return lines

    def _extract_inline_text(self, node: Tag) -> str:
        parts: List[str] = []
        for child in node.children:
            if isinstance(child, NavigableString):
                parts.append(str(child))
            elif isinstance(child, Tag):
                if child.name == "br":
                    parts.append(" ")
                else:
                    parts.append(self._extract_inline_text(child))
        return self._normalize_whitespace("".join(parts))

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        cleaned = " ".join(text.replace("\xa0", " ").split())
        return cleaned

    # ------------------------------------------------------------------
    # Assets and includes

    def _copy_asset(self, src: str) -> str:
        if "figures" not in src:
            return ""
        cached = self.asset_cache.get(src)
        if cached:
            return cached

        source_path = (self.html_path.parent / src).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"Asset not found: {source_path}")

        ext = source_path.suffix.lower()
        subdir = ASSET_DIR_MAP.get(ext)
        if not subdir:
            raise ValueError(f"Unsupported asset extension: {source_path.name}")

        dest_dir = self.project_root / "source" / "assets" / subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / source_path.name
        if dest_path.exists():
            raise FileExistsError(
                f"Asset already exists: {dest_path}\n"
                "Refusing to overwrite. Delete or move the existing file, then rerun."
            )
        shutil.copy2(source_path, dest_path)
        rel_path = f"{subdir}/{dest_path.name}"
        self.asset_cache[src] = rel_path
        return rel_path

    def _update_section_file(self, section: str, include_ids: Sequence[str]) -> bool:
        section_rel = SECTION_FILES.get(section)
        if not section_rel:
            print(f"  !! No wrapper configured for Section {section}.")
            return False
        section_path = self.project_root / section_rel
        if not section_path.exists():
            print(f"  !! Wrapper file missing: {section_path}.")
            return False
        text = section_path.read_text()

        pattern = re.compile(
            r"(<!--\s*=========================================\s*\n\s*  Practica de las lecciones de la sección\s*\n\s*  ============================================== -->)([\s\S]*?)(\n\s*<!--\s*=========================================\s*\n\s*  Exploración)",
            re.MULTILINE,
        )
        match = pattern.search(text)
        if not match:
            raise RuntimeError(f"Unable to locate practice block in {section_path}")

        existing_block = match.group(2)
        if "<xi:include" in existing_block:
            raise RuntimeError(
                f"{section_path} already contains practice problem includes. "
                "Remove them (or explicitly curate the section) before rerunning the importer."
            )

        include_block = "\n".join(
            f"  <xi:include href=\"../content/{xml_id}.ptx\"/>" for xml_id in include_ids
        )

        start, end = match.start(2), match.end(2)
        new_text = text[:start] + "\n" + include_block + "\n\n" + text[end:]
        section_path.write_text(new_text)
        return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html",
        type=Path,
        required=True,
        help="Path to the practice.html file.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root containing the source/ tree.",
    )
    parser.add_argument(
        "--sections",
        default="A,B,C,D",
        help="Comma-separated section letters to import (default: A,B,C,D).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sections = [sect.strip().upper() for sect in args.sections.split(",") if sect.strip()]
    importer = PracticeImporter(args.html, args.project_root.resolve(), sections)
    try:
        importer.run()
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

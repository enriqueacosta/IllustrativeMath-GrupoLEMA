"""
Enrique Acosta, 2025. Created for the IllustrativeMath-GrupoLEMA project with github copoilot.

This script is intended for use in the IllustrativeMath-GrupoLEMA project to quickly find which activity center files
reference a given centro and what stages/etapas are listed for each. It searches all *-matCentros.ptx files in the 'source/' directory for a given centro name (e.g., 'centro-librosDeImagenes')
and prints the file prefix and the text that follows the <xref> tag in each match.

Usage:
    python searchCentroEnMatCentros.py centro-librosDeImagenes

Example output:
    act-centros-escoger2: etapa 1
    act-centros-escoger5: etapa 1 y etapa 2
    ...

Arguments:
    centro-name   The value of the 'ref' attribute to search for in <xref> tags (e.g., 'centro-librosDeImagenes')
"""
import sys
import glob
import os
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: python searchCentroEnMatCentros.py centro-name")
        sys.exit(1)


    centro = sys.argv[1]
    # # Pattern: find <xref ref="centro" .../> and capture the text after it up to </li>
    # pattern = re.compile(r'<xref\s+ref=["\']{}["\'][^>]*/>([^<]*)</li>'.format(re.escape(centro)))
    # # Fix: correct regex for whitespace and not double-escaping
    # pattern = re.compile(r'<xref\s+ref=["\']{}["\'][^>]*/>([^<]*)</li>'.format(re.escape(centro)))
    # # Actually, use a more robust regex for XML lines (allow for whitespace and attributes)
    # pattern = re.compile(r'<xref\s+ref=["\']{}["\'][^>]*/>([^<]*)</li>'.format(re.escape(centro)))
    # # But Python raw string, so:
    # pattern = re.compile(r'<xref\s+ref=["\']{}["\'][^>]*/>([^<]*)</li>'.format(re.escape(centro)))
    # # Actually, best to just match the line and parse after

    base_dir = "source"
    matches = []

    for filepath in glob.glob(f"{base_dir}/**/*-matCentros.ptx", recursive=True):
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                if f'<xref ref="{centro}"' in line:
                    # Extract the text after the self-closing tag
                    after = line.split('/>')[-1].split('</li>')[0].strip(" ,:")
                    prefix = os.path.basename(filepath).replace("-matCentros.ptx", "")
                    matches.append((prefix, after))

    for prefix, after in matches:
        print(f"{prefix}: {after}")

if __name__ == "__main__":
    main()

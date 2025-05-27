"""
Script to check if the filename of a .ptx file matches its top-level xml:id.

This script recursively searches for .ptx files in a given directory, skipping files ending with -mat, -matCentros, or PP#. If the filename does not match the xml:id, it prints a warning.

Usage:
    python check_xmlid_vs_filename.py <directory>
"""

import os
import re
import glob

def get_xml_id(filepath):
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            # Look for xml:id in the first tag after the XML declaration
            m = re.search(r'<\w+\s+[^>]*xml:id="([^"]+)"', line)
            if m:
                return m.group(1)
    return None

def check_filenames_vs_xmlid(directory):
    for filepath in glob.glob(os.path.join(directory, '**', '*.ptx'), recursive=True):
        filename = os.path.splitext(os.path.basename(filepath))[0]
        # Skip -mat, -matCentros, PP# files
        if re.search(r'(-mat(Centros)?|PP\d+)$', filename):
            continue
        xml_id = get_xml_id(filepath)
        if xml_id and filename != xml_id:
            print(f"WARNING: '{filename}' does not match xml:id '{xml_id}'")
        # Uncomment below to see all checked files
        # else:
        #     print(f"OK: {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        check_filenames_vs_xmlid(sys.argv[1])
    else:
        print("Usage: python check_xmlid_vs_filename.py <directory>")

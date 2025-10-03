#!/usr/bin/env python3

"""
This script generates lesson-related .ptx files from templates for a given unit.

Usage:
    python create_lesson_files.py <unit> <number> <lec-xml:id> [<warm-xml:id>] [<act-xml:id> ...] [<cool-xml:id>]

Arguments:
    <unit>           Unit identifier (e.g., gra0-uni2); files live directly in source/content
    <number>         The lesson number (used for replacement in template)
    <lec-xml:id>     The main lesson file ID (must start with lec-)
    <warm-xml:id>    (optional) ID for the warm-up file (must start with warm-)
    <act-xml:id>     (optional) Up to 3 activity file IDs (must start with act-)
    <cool-xml:id>    (optional) ID for the cool-down file (must start with cool-)

Behavior:
    • Copies templates from source/TEMPLATES/
    • Replaces placeholders in templates:
        - lec-VVVVVV         → <lec-xml:id>
        - warm-RRRRRR-SSSSSS → <warm-xml:id>
        - act-RRRRRR         → 1st <act-xml:id>
        - act-SSSSSS         → 2nd <act-xml:id>
        - act-TTTTTT         → 3rd <act-xml:id>
        - cool-RRRRRR        → <cool-xml:id>
        - [@##@]             → <number>
    • Patches the created <lec-xml:id>.ptx file:
        - Replaces warm-QQQQQQ and cool-UUUUUU if those references are present
        - Replaces activity references (act-RRRRRR, etc.)
        - Removes entire <... xml:id="<lec-xml:id>-act2"> or -act3 blocks if fewer than 2 or 3 activities are provided

Safety:
    • Performs full validation before writing any files
    • Does not overwrite existing files
    • Provides detailed status messages

Example:
    python create_lesson_files.py gra1-uni1 16 lec-myLesson warm-intro act-act1 act-act2 cool-wrapup

Author: Enrique Acosta, April 2025
"""



import os
import sys

def print_usage():
    print("Usage:")
    print("  python create_lesson_files.py <unit> <number> <lec-xml:id> [<warm-xml:id>] [<act-xml:id> ...] [<cool-xml:id>]")
    print("Notes:")
    print("  - <unit> is the unit identifier (e.g., gra0-uni2); files live in source/content")
    print("  - lec-xml:id is required and must start with 'lec-'")
    print("  - 0 or 1 warm-xml:id allowed and must start with 'warm-'")
    print("  - Up to 3 act-xml:id allowed and must start with 'act-'")
    print("  - 0 or 1 cool-xml:id allowed and must start with 'cool-' and must be last if present")

def validate_args(unit, number, lec_id, warm_id, act_ids, cool_id):
    errors = []
    paths_to_create = []

    if not lec_id.startswith("lec-"):
        errors.append(f"❌ ERROR: <lec-xml:id> must start with 'lec-'. Got '{lec_id}'")

    if warm_id and not warm_id.startswith("warm-"):
        errors.append(f"❌ ERROR: <warm-xml:id> must start with 'warm-'. Got '{warm_id}'")

    if any(not act.startswith("act-") for act in act_ids):
        errors.append(f"❌ ERROR: All activity IDs must start with 'act-'")

    if len(act_ids) > 3:
        errors.append(f"❌ ERROR: You can specify at most 3 activity IDs. Got {len(act_ids)}")

    if cool_id and not cool_id.startswith("cool-"):
        errors.append(f"❌ ERROR: <cool-xml:id> must start with 'cool-'. Got '{cool_id}'")

    base_dir = os.path.join("..", "source", "content")

    all_ids = [(lec_id, "lec-VVVVVV.ptx")] + \
              ([(warm_id, "warm-RRRRRR-SSSSSS.ptx")] if warm_id else []) + \
              [(aid, "act-RRRRRR-SSSSSS.ptx") for aid in act_ids] + \
              ([(cool_id, "cool-RRRRRR.ptx")] if cool_id else [])

    for xml_id, template in all_ids:
        target_path = os.path.join(base_dir, f"{xml_id}.ptx")
        template_path = os.path.join("..", "source", "TEMPLATES", template)
        if os.path.exists(target_path):
            errors.append(f"⚠️  WARNING: File already exists — {target_path}")
        if not os.path.exists(template_path):
            errors.append(f"❌ ERROR: Template not found — {template_path}")
        paths_to_create.append((template_path, target_path, xml_id))

    return errors, paths_to_create

def write_from_template(template_path, target_path, replacements):
    with open(template_path, "r", encoding="utf-8") as f:
        contents = f.read()
    for old, new in replacements.items():
        contents = contents.replace(old, new)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(contents)
    print(f"✅ Created file: {target_path}")

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 8:
        print("❌ ERROR: Incorrect number of arguments.\n")
        print_usage()
        sys.exit(1)

    unit = sys.argv[1]
    number = sys.argv[2]
    lec_id = sys.argv[3]
    warm_id = None
    act_ids = []
    cool_id = None

    for arg in sys.argv[4:]:
        if arg.startswith("warm-") and warm_id is None and not act_ids and not cool_id:
            warm_id = arg
        elif arg.startswith("act-") and cool_id is None:
            act_ids.append(arg)
        elif arg.startswith("cool-") and cool_id is None:
            cool_id = arg
        else:
            print(f"❌ ERROR: Invalid or misordered argument: {arg}")
            print_usage()
            sys.exit(1)

    errors, paths_to_create = validate_args(unit, number, lec_id, warm_id, act_ids, cool_id)

    if errors:
        print("\n".join(errors))
        print("\n🚫 No files were created due to the above issues.\n")
        sys.exit(1)

    # Create files from templates
    for template_path, target_path, xml_id in paths_to_create:
        if xml_id.startswith("lec-"):
            replacements = {"lec-VVVVVV": xml_id, "[@##@]": number}
        elif xml_id.startswith("warm-"):
            replacements = {"warm-RRRRRR-SSSSSS": xml_id}
        elif xml_id.startswith("act-"):
            replacements = {"act-RRRRRR-SSSSSS": xml_id}
        elif xml_id.startswith("cool-"):
            replacements = {"cool-RRRRRR": xml_id}
        else:
            continue
        write_from_template(template_path, target_path, replacements)

    # Post-processing: patch lesson file to insert warm/cool/act references and possibly remove unused sections
    lec_path = os.path.join("..", "source", "content", f"{lec_id}.ptx")
    try:
        with open(lec_path, "r", encoding="utf-8") as f:
            content = f.read()

        patched = False

        # Warm and cool replacements
        if warm_id and "warm-QQQQQQ" in content:
            content = content.replace("warm-QQQQQQ", warm_id)
            print(f"🔧 Patched lesson file to include warm-up reference: {warm_id}")
            patched = True

        if cool_id and "cool-UUUUUU" in content:
            content = content.replace("cool-UUUUUU", cool_id)
            print(f"🔧 Patched lesson file to include cool-down reference: {cool_id}")
            patched = True

        # Activity ID replacements
        act_placeholders = ["act-RRRRRR", "act-SSSSSS", "act-TTTTTT"]
        for i, act_id in enumerate(act_ids):
            if act_placeholders[i] in content:
                content = content.replace(act_placeholders[i], act_id)
                print(f"🔧 Patched lesson file to include activity {i+1}: {act_id}")
                patched = True

        import re

        # Remove act3 section if not provided
        if len(act_ids) < 3:
            pattern = rf"<(?P<tag>\w+)[^>]*xml:id=\"{lec_id}-act3\"[^>]*>(.*?)</(?P=tag)>"
            new_content, num_subs = re.subn(pattern, "", content, flags=re.DOTALL)
            if num_subs > 0:
                content = new_content
                print(f"🧹 Removed unused <act3> section with xml:id=\"{lec_id}-act3\"")
                patched = True

        # Remove act2 section if not provided
        if len(act_ids) < 2:
            pattern = rf"<(?P<tag>\w+)[^>]*xml:id=\"{lec_id}-act2\"[^>]*>(.*?)</(?P=tag)>"
            new_content, num_subs = re.subn(pattern, "", content, flags=re.DOTALL)
            if num_subs > 0:
                content = new_content
                print(f"🧹 Removed unused <act2> section with xml:id=\"{lec_id}-act2\"")
                patched = True

        if patched:
            with open(lec_path, "w", encoding="utf-8") as f:
                f.write(content)

    except Exception as e:
        print(f"❌ ERROR: Failed to patch lesson file {lec_path}: {e}")


if __name__ == "__main__":
    main()

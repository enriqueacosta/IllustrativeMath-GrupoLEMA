#!/usr/bin/env python3
"""
Script to update XML lesson files with content from an HTML file.

Usage:
    python ingest_simple_lesson_content.py <lesson_plan_file> <html_content_file>

Example:
    python ingest_simple_lesson_content.py source/gra0-uni1/lec-explicarConteo.ptx lesson_extracted_launch_activity_synthesis.html
"""

import sys
import os
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# -------------------------------
# HTML Extraction Functions
# -------------------------------
def extract_html_sections(html_file):
    """Extract sections and subsections from the HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    sections = []

    # Lesson-level section (for teacher and narrative items)
    lesson_section = {
        'title': 'Lesson',
        'subsections': []
    }
    for ref_name, ref_id in [
        ('Lesson Purpose', 'purpose-leccion-titulo'),
        ('Lesson Narrative', 'narrative-leccion-titulo'),
        ('Teacher Reflection Questions', 'reflection-quest-titulo')
    ]:
        for h3 in soup.find_all('h3'):
            if ref_name.lower() in h3.text.lower():
                next_element = h3.find_next(['p', 'ul'])
                if next_element and "NOT PRESENT" not in str(next_element):
                    lesson_section['subsections'].append({
                        'name': ref_name,
                        'ref': ref_id,
                        'content': str(next_element),
                        'type': next_element.name
                    })
                    break
    if lesson_section['subsections']:
        sections.append(lesson_section)

    # Regular activity sections
    current_section = None
    for element in soup.body.children:
        if element.name == 'h2':
            if current_section:
                sections.append(current_section)
            current_section = {
                'title': element.text,
                'subsections': []
            }
        elif element.name == 'h3' and current_section:
            # Extract ref info if present in the h3 text
            h3_text = element.text
            ref_match = re.search(r'\(for ref="([^"]+)"\)', h3_text)
            ref = ref_match.group(1) if ref_match else None
            subsection_name = re.sub(r'\s*\(for ref="[^"]+"\)', '', h3_text)

            next_element = element.find_next()
            if next_element:
                if next_element.name in ['ul', 'p']:
                    current_section['subsections'].append({
                        'name': subsection_name,
                        'ref': ref,
                        'content': str(next_element),
                        'type': next_element.name
                    })
            else:
                # Handle "NOT PRESENT" case if no proper element found
                sibling = element.next_sibling
                text_content = ""
                while sibling and (not getattr(sibling, 'name', None) or (sibling.name not in ['h3', 'h2'])):
                    if isinstance(sibling, str) and "NOT PRESENT" in sibling:
                        text_content = "NOT PRESENT"
                        break
                    sibling = sibling.next_sibling
                if text_content:
                    current_section['subsections'].append({
                        'name': subsection_name,
                        'ref': ref,
                        'content': text_content,
                        'type': 'text'
                    })
    if current_section:
        sections.append(current_section)
    return sections

def normalize_title(title):
    """Normalize a title by removing special characters and converting to lowercase."""
    normalized = re.sub(r'[^\w\s]', '', title).lower()
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

# -------------------------------
# Lesson Plan and XML Helper Functions
# -------------------------------
def extract_lesson_id(lesson_plan_file):
    """Extract the lesson ID from the lesson plan file."""
    filename = os.path.basename(lesson_plan_file)
    filename_without_ext = os.path.splitext(filename)[0]
    if filename_without_ext.startswith('lec-'):
        return filename_without_ext
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    id_match = re.search(r'<subsection xml:id="([^"]+)"', content)
    return id_match.group(1) if id_match else filename_without_ext

def find_included_files(lesson_plan_file):
    """Find all included XML files in the lesson plan and their types."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    base_dir = os.path.dirname(lesson_plan_file)
    lesson_id = extract_lesson_id(lesson_plan_file)
    file_info = []

    # Warm-up section
    warm_pattern = r'<subsubsection xml:id="' + re.escape(lesson_id) + r'-warm".*?<xi:include href="\./([^"]+)\.ptx"/>'
    warm_match = re.search(warm_pattern, content, re.DOTALL)
    if warm_match:
        warm_file = warm_match.group(1)
        file_info.append(("warm-up", os.path.join(base_dir, warm_file + '.ptx')))

    # Activity sections (activities 1-9)
    for act_num in range(1, 10):
        act_pattern = r'<subsubsection xml:id="' + re.escape(lesson_id) + r'-act' + str(act_num) + r'".*?<xi:include href="\./([^"]+)\.ptx"/>'
        act_matches = re.findall(act_pattern, content, re.DOTALL)
        for act_file in act_matches:
            file_info.append((f"activity-{act_num}", os.path.join(base_dir, act_file + '.ptx')))

    # Other included files not already captured
    other_pattern = r'<xi:include href="\./([^"]+)\.ptx"/>'
    all_includes = re.findall(other_pattern, content)
    for include in all_includes:
        file_path = os.path.join(base_dir, include + '.ptx')
        if not any(file_path == path for _, path in file_info):
            file_info.append(("other", file_path))
    print(f"Found {len(file_info)} files to process:")
    for title, path in file_info:
        print(f"  - {title}: {path}")
    return file_info

def get_xml_file_title(xml_file):
    """Extract the title from an XML file."""
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    title_match = re.search(r'<title>(.*?)</title>', content)
    return title_match.group(1).strip() if title_match else None

def indent_html_content(html_content):
    """Indent HTML content for ul/li structures while preserving child order.
    Any <q> element is output on its own indented line.
    Also converts any <fillin></fillin> to <fillin/>."""
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html_content, 'html.parser')
    ul = soup.find('ul')
    if not ul:
        return html_content

    # Define indentation levels:
    indent_ul = ""            # No indent for the <ul> tag line
    indent_li = "      "      # 6 spaces for each <li>
    indent_child = indent_li + "  "  # 8 spaces for child elements like <q>

    result_lines = [indent_ul + "<ul>"]

    # Process each top-level <li>
    for li in ul.find_all('li', recursive=False):
        processed_parts = []
        for child in li.contents:
            if getattr(child, "name", None) == "q":
                # For <q> tags, output on a new line with extra indentation.
                processed_parts.append("\n" + indent_child + str(child).strip())
            else:
                # For NavigableString or other tags, preserve as-is.
                if isinstance(child, NavigableString):
                    text = child.strip()
                    if text:
                        processed_parts.append(text)
                else:
                    processed_parts.append(str(child))
        li_content = "".join(processed_parts)
        # If there's a newline in the content, ensure the closing </li> appears on its own indented line.
        if "\n" in li_content:
            li_content = li_content.rstrip() + "\n" + indent_li
        result_lines.append(indent_li + "<li>" + li_content + "</li>")
    result_lines.append("    " + "</ul>")
    
    result = "\n".join(result_lines)
    # Post-process: convert any <fillin></fillin> to self-closing <fillin/>
    result = result.replace("<fillin></fillin>", "<fillin/>")
    return result



# -------------------------------
# XML Update Helper Functions
# -------------------------------
def create_replacement_xml(subsection):
    """Generate the replacement XML snippet for a given subsection."""
    ref = subsection['ref']
    content_type = subsection.get('type')
    if content_type == 'ul':
        inner = indent_html_content(subsection['content'])
    elif content_type == 'p':
        inner = subsection["content"]
    elif content_type == 'text' and subsection['content'] == 'NOT PRESENT':
        inner = '<p>[@@@@@@@@@]</p>'
    else:
        inner = '<p>[@@@@@@@@@]</p>'
    replacement = (
        f'<paragraphs>\n'
        f'    <title><custom ref="{ref}"/></title>\n'
        f'    {inner}\n'
        f'  </paragraphs>'
    )
    return replacement

def update_xml_content(content, subsection):
    """Apply XML update for the given subsection on the provided content."""
    # Build a regex pattern to find the paragraphs block based on the ref.
    pattern = r'<paragraphs>\s*<title><custom ref="' + re.escape(subsection['ref']) + r'"/></title>.*?</paragraphs>'
    replacement = create_replacement_xml(subsection)
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    return new_content, count

# -------------------------------
# File Update Functions
# -------------------------------
def update_file(xml_file, html_subsections, file_label):
    """Update a single XML file using matching HTML subsections."""
    if not os.path.exists(xml_file):
        print(f"Warning: File {xml_file} does not exist. Skipping.")
        return

    xml_title = get_xml_file_title(xml_file)
    if not xml_title:
        print(f"Warning: Could not extract title from {xml_file}. Skipping.")
        return

    # Select matching section based on file_label.
    matching_section = None
    if file_label == "warm-up":
        for section in html_subsections:
            if section['title'].startswith("Warm-up:"):
                matching_section = section
                print(f"  Found match as warm-up!")
                break
    elif file_label.startswith("activity-"):
        act_num = file_label.split("-")[1]
        for section in html_subsections:
            if section['title'].startswith(f"Activity {act_num}:"):
                matching_section = section
                print(f"  Found match as Activity {act_num}!")
                break
    else:
        normalized_xml_title = normalize_title(xml_title)
        print(f"Looking for match for '{xml_file}' with title '{xml_title}' (normalized: '{normalized_xml_title}')")
        for section in html_subsections:
            if normalized_xml_title in normalize_title(section['title']):
                matching_section = section
                print(f"  Found match by normalized title!")
                break

    if not matching_section:
        print(f"Warning: No matching HTML section found for {xml_file} with title '{xml_title}'. Skipping.")
        return

    print(f"Matched {xml_file} with HTML section '{matching_section['title']}'")
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for subsection in matching_section['subsections']:
        if not subsection['ref']:
            continue
        new_content, count = update_xml_content(content, subsection)
        if count > 0:
            print(f"  - Updated {count} instance(s) of '{subsection['ref']}' in {xml_file}")
            content = new_content
        else:
            print(f"  - No matches found for '{subsection['ref']}' in {xml_file}")

    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {xml_file} with content from '{matching_section['title']}'")

def update_lesson_file(lesson_plan_file, html_sections):
    """Update the main lesson file with lesson-level content from HTML."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    lesson_section = next((sec for sec in html_sections if sec['title'] == 'Lesson'), None)
    if not lesson_section:
        print("Warning: No lesson section found in HTML. Skipping lesson file updates.")
        return

    for subsection in lesson_section['subsections']:
        if not subsection['ref']:
            continue
        new_content, count = update_xml_content(content, subsection)
        if count > 0:
            print(f"  - Updated {count} instance(s) of '{subsection['ref']}' in main lesson file")
            content = new_content
        else:
            print(f"  - No matches found for '{subsection['ref']}' in main lesson file")

    with open(lesson_plan_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated main lesson file {lesson_plan_file}")

def update_time_values(lesson_plan_file, html_sections):
    """Update time values in the lesson plan file based on HTML section titles."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    lesson_id = extract_lesson_id(lesson_plan_file)
    for section in html_sections:
        time_match = re.search(r'\((\d+) minutes\)', section['title'])
        if time_match:
            time_value = time_match.group(1)
            section_name = section['title'].split(':')[0].strip()
            if "Warm-up" in section_name:
                pattern = (r'<subsubsection xml:id="' + re.escape(lesson_id) + 
                           r'-warm".*?<title component="profesor"><nbsp/>\(.*?mins\)</title>')
                replacement = (
                    f'<subsubsection xml:id="{lesson_id}-warm" component="no-libroTrabajo">\n'
                    f'  <shorttitle><custom ref="warm-up-leccion-titulo"/></shorttitle>\n'
                    f'  <title><custom ref="warm-up-leccion-titulo"/></title>\n'
                    f'  <!-- Tiempo en el título que solo ve el profesor -->\n'
                    f'  <title component="profesor"><nbsp/>({time_value} mins)</title>'
                )
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            elif "Activity" in section_name:
                activity_num = re.search(r'Activity (\d+)', section_name)
                if activity_num:
                    num = activity_num.group(1)
                    pattern = (r'<subsubsection xml:id="' + re.escape(lesson_id) +
                               r'-act' + num + r'".*?<title component="profesor"><nbsp/>\(.*?mins\)</title>')
                    replacement = (
                        f'<subsubsection xml:id="{lesson_id}-act{num}" component="no-libroTrabajo">\n'
                        f'  <shorttitle>Actividad {num}</shorttitle>\n'
                        f'  <title>Actividad {num}</title>\n'
                        f'  <!-- Tiempo en el título que solo ve el profesor -->\n'
                        f'  <title component="profesor"><nbsp/>({time_value} mins)</title>'
                    )
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(lesson_plan_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated time values in {lesson_plan_file}")

# -------------------------------
# Main Routine
# -------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python ingest_simple_lesson_content.py <lesson_plan_file> <html_content_file>")
        sys.exit(1)

    lesson_plan_file = sys.argv[1]
    html_file = sys.argv[2]

    lesson_id = extract_lesson_id(lesson_plan_file)
    print(f"Working with lesson ID: {lesson_id}")

    html_sections = extract_html_sections(html_file)
    print("Extracted HTML sections:")
    for section in html_sections:
        print(f"  - {section['title']}")
        for subsection in section['subsections']:
            print(f"    - {subsection['name']} (ref: {subsection['ref']})")

    update_lesson_file(lesson_plan_file, html_sections)
    update_time_values(lesson_plan_file, html_sections)

    included_files = find_included_files(lesson_plan_file)
    for file_label, xml_file in included_files:
        update_file(xml_file, html_sections, file_label)

    print("All files updated successfully!")

if __name__ == "__main__":
    main()

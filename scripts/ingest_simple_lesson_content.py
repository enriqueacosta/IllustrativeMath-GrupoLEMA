#!/usr/bin/env python3
"""
Script to update XML lesson files with content from a simple HTML file.
The HTML file is assumed to be the output of the extract_HTML_lesson_and_preparation
or extract_HTML_launch_synthesis_instructions script.

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
# Utility File I/O Functions
# -------------------------------
def read_file(filepath):
    """Read and return the contents of a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# -------------------------------
# HTML Extraction Functions
# -------------------------------
def extract_html_sections(html_file):
    """
    Parse the HTML file and extract its sections and subsections.
    Returns a list of sections where each section contains a title and a list of subsections.
    """
    html_content = read_file(html_file)
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = []

    # Extract lesson-level content (e.g., teacher reflections, lesson purpose, etc.)
    lesson_section = {'title': 'Lesson', 'subsections': []}
    lesson_refs = [
        ('Lesson Purpose', 'purpose-leccion-titulo'),
        ('Lesson Narrative', 'narrative-leccion-titulo'),
        ('Teacher Reflection Questions', 'reflection-quest-titulo')
    ]
    # Loop over each reference and find the corresponding h3 header in the HTML
    for ref_name, ref_id in lesson_refs:
        h3 = next((h for h in soup.find_all('h3') if ref_name.lower() in h.text.lower()), None)
        if h3:
            next_elem = h3.find_next(['p', 'ul'])
            # Only add subsections if valid content is found
            if next_elem and "NOT PRESENT" not in str(next_elem):
                lesson_section['subsections'].append({
                    'name': ref_name,
                    'ref': ref_id,
                    'content': str(next_elem),
                    'type': next_elem.name
                })
    if lesson_section['subsections']:
        sections.append(lesson_section)

    # Extract the Lesson Synthesis section from any <h2> that contains "lesson synthesis"
    for h2 in soup.find_all('h2'):
        if 'lesson synthesis' in h2.text.lower():
            content_elements = []
            current = h2.next_sibling
            # Collect all content elements until the next h2 is encountered
            while current and (not getattr(current, 'name', None) == 'h2'):
                if getattr(current, 'name', None) in ['p', 'ul']:
                    content_elements.append(str(current))
                current = current.next_sibling
            if content_elements:
                # Join the content elements if there are multiple
                content = content_elements[0] if len(content_elements) == 1 else "\n".join(content_elements)
                synthesis_section = {
                    'title': 'Lesson Synthesis',
                    'subsections': [{
                        'name': 'Lesson Synthesis',
                        'ref': 'synthesis-leccion-titulo',
                        'content': content,
                        'type': BeautifulSoup(content, 'html.parser').find().name if content else 'p'
                    }]
                }
                # Optionally extract time information from the h2 header text
                time_match = re.search(r'\((\d+) minutes\)', h2.text)
                if time_match:
                    synthesis_section['time'] = time_match.group(1)
                sections.append(synthesis_section)
                break  # Only process the first matching synthesis section

    # Extract regular activity sections based on h2/h3 structure in the HTML body
    current_section = None
    for element in soup.body.children:
        if element.name == 'h2':
            # When encountering an h2, finish the current section and start a new one.
            if current_section:
                sections.append(current_section)
            current_section = {'title': element.text, 'subsections': []}
        elif element.name == 'h3' and current_section:
            # Process h3 elements as subsection headers.
            h3_text = element.text
            # Look for a reference inside the h3 text using regex
            ref_match = re.search(r'\(for ref="([^"]+)"\)', h3_text)
            ref = ref_match.group(1) if ref_match else None
            # Remove the reference text from the title for clarity
            subsection_name = re.sub(r'\s*\(for ref="[^"]+"\)', '', h3_text)
            next_elem = element.find_next()
            if next_elem and next_elem.name in ['p', 'ul']:
                current_section['subsections'].append({
                    'name': subsection_name,
                    'ref': ref,
                    'content': str(next_elem),
                    'type': next_elem.name
                })
            else:
                # Handle cases where content is indicated as "NOT PRESENT"
                sibling = element.next_sibling
                text_content = ""
                while sibling and (not getattr(sibling, 'name', None) or sibling.name not in ['h2', 'h3']):
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
    return re.sub(r'\s+', ' ', normalized).strip()

# -------------------------------
# Lesson Plan and XML Helper Functions
# -------------------------------
def extract_lesson_id(lesson_plan_file):
    """
    Extract the lesson ID from the lesson plan file.
    It first attempts to use the filename if it starts with 'lec-',
    otherwise it looks for an xml:id attribute in the file.
    """
    filename = os.path.basename(lesson_plan_file)
    name_without_ext = os.path.splitext(filename)[0]
    if name_without_ext.startswith('lec-'):
        return name_without_ext
    content = read_file(lesson_plan_file)
    match = re.search(r'<subsection xml:id="([^"]+)"', content)
    return match.group(1) if match else name_without_ext

def find_included_files(lesson_plan_file):
    """
    Find all XML files that are included in the lesson plan file.
    This includes warm-up, activity, and other XML includes.
    """
    content = read_file(lesson_plan_file)
    base_dir = os.path.dirname(lesson_plan_file)
    lesson_id = extract_lesson_id(lesson_plan_file)
    files = []

    # Look for a warm-up file inclusion
    warm_pattern = r'<subsubsection xml:id="' + re.escape(lesson_id) + r'-warm".*?<xi:include href="\./([^"]+)\.ptx"/>'
    warm_match = re.search(warm_pattern, content, re.DOTALL)
    if warm_match:
        files.append(("warm-up", os.path.join(base_dir, warm_match.group(1) + '.ptx')))

    # Loop through possible activity sections (1-9) to capture their includes
    for i in range(1, 10):
        act_pattern = r'<subsubsection xml:id="' + re.escape(lesson_id) + r'-act' + str(i) + r'".*?<xi:include href="\./([^"]+)\.ptx"/>'
        for act_file in re.findall(act_pattern, content, re.DOTALL):
            files.append((f"activity-{i}", os.path.join(base_dir, act_file + '.ptx')))

    # Capture any other XML includes not already found
    other_pattern = r'<xi:include href="\./([^"]+)\.ptx"/>'
    for inc in re.findall(other_pattern, content):
        file_path = os.path.join(base_dir, inc + '.ptx')
        if not any(file_path == path for _, path in files):
            files.append(("other", file_path))
    print(f"Found {len(files)} files to process:")
    for label, path in files:
        print(f"  - {label}: {path}")
    return files

def get_xml_file_title(xml_file):
    """
    Extract the title from an XML file.
    It searches for the first occurrence of a <title> tag.
    """
    content = read_file(xml_file)
    match = re.search(r'<title>(.*?)</title>', content)
    return match.group(1).strip() if match else None

def indent_html_content(html_content):
    """
    Format and indent HTML content for <ul>/<li> structures.
    Also converts any <fillin></fillin> tags to self-closing <fillin/>.
    """
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(html_content, 'html.parser')
    ul = soup.find('ul')
    if not ul:
        return html_content

    # Define indentation levels
    indent_ul = ""            # No indent for the <ul> tag line
    indent_li = "      "      # 6 spaces for <li> items
    indent_child = indent_li + "  "  # 8 spaces for child elements inside <li>

    lines = [indent_ul + "<ul>"]
    for li in ul.find_all('li', recursive=False):
        parts = []
        for child in li.contents:
            # For <q> tags, output on a new line with extra indentation.
            if getattr(child, "name", None) == "q":
                parts.append("\n" + indent_child + str(child).strip())
            elif isinstance(child, NavigableString):
                text = child.strip()
                if text:
                    parts.append(text)
            else:
                parts.append(str(child))
        li_content = "".join(parts)
        # Ensure proper indentation if the content spans multiple lines.
        if "\n" in li_content:
            li_content = li_content.rstrip() + "\n" + indent_li
        lines.append(indent_li + "<li>" + li_content + "</li>")
    lines.append("    " + "</ul>")
    result = "\n".join(lines)
    # Convert any <fillin></fillin> tags to self-closing <fillin/>
    result = result.replace("<fillin></fillin>", "<fillin/>")
    return result

def create_replacement_xml(subsection):
    """
    Generate the replacement XML snippet for a given subsection.
    Uses the subsection type to determine how to format the inner content.
    """
    ref = subsection['ref']
    content_type = subsection.get('type')
    if content_type == 'ul':
        inner = indent_html_content(subsection['content'])
    elif content_type == 'p':
        inner = subsection['content']
    elif content_type == 'text' and subsection['content'] == 'NOT PRESENT':
        inner = '<p>[@@@@@@@@@]</p>'
    else:
        inner = '<p>[@@@@@@@@@]</p>'
    return (
        f'<paragraphs>\n'
        f'    <title><custom ref="{ref}"/></title>\n'
        f'    <p>[+++++++++++++++]</p>\n'
        f'    {inner}\n'
        f'  </paragraphs>'
    )

def update_xml_content(content, subsection):
    """
    Replace the XML block corresponding to the given subsection.
    Uses regex to locate the block and replaces it with the new content.
    """
    pattern = r'<paragraphs>\s*<title><custom ref="' + re.escape(subsection['ref']) + r'"/></title>.*?</paragraphs>'
    replacement = create_replacement_xml(subsection)
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    return new_content, count

# -------------------------------
# XML Update Functions
# -------------------------------
def update_recommended_time(xml_file, time_value):
    """
    Update the recommended time in an XML file.
    Searches for a specific time placeholder and replaces it with the new time.
    """
    if not os.path.exists(xml_file):
        return False
    content = read_file(xml_file)
    pattern = r'<paragraphs>\s*<title><custom ref="recommended-time-titulo"/></title>\s*<p>\[@{9,}\] minutos</p>\s*</paragraphs>'
    replacement = (
        f'<paragraphs>\n'
        f'    <title><custom ref="recommended-time-titulo"/></title>\n'
        f'    <p>{time_value} minutos</p>\n'
        f'  </paragraphs>'
    )
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count:
        write_file(xml_file, new_content)
        return True
    return False

def update_file(xml_file, html_sections, file_label):
    """
    Update a single XML file using matching HTML subsections.
    Determines the matching HTML section based on the file label and updates its content.
    """
    if not os.path.exists(xml_file):
        print(f"Warning: File {xml_file} does not exist. Skipping.")
        return

    xml_title = get_xml_file_title(xml_file)
    if not xml_title:
        print(f"Warning: Could not extract title from {xml_file}. Skipping.")
        return

    # Determine which HTML section matches based on the file label
    matching_section = None
    if file_label == "warm-up":
        matching_section = next((sec for sec in html_sections if sec['title'].startswith("Warm-up:")), None)
        if matching_section:
            print("  Found match as warm-up!")
    elif file_label.startswith("activity-"):
        act_num = file_label.split("-")[1]
        matching_section = next((sec for sec in html_sections if sec['title'].startswith(f"Activity {act_num}:")), None)
        if matching_section:
            print(f"  Found match as Activity {act_num}!")
    else:
        norm_xml_title = normalize_title(xml_title)
        print(f"Looking for match for '{xml_file}' with title '{xml_title}' (normalized: '{norm_xml_title}')")
        matching_section = next((sec for sec in html_sections if norm_xml_title in normalize_title(sec['title'])), None)
        if matching_section:
            print("  Found match by normalized title!")
    if not matching_section:
        print(f"Warning: No matching HTML section found for {xml_file} with title '{xml_title}'. Skipping.")
        return

    print(f"Matched {xml_file} with HTML section '{matching_section['title']}'")
    
    # Update the recommended time if present in the HTML section title
    time_match = re.search(r'\((\d+) minutes\)', matching_section['title'])
    if time_match:
        time_value = time_match.group(1)
        if update_recommended_time(xml_file, time_value):
            print(f"  - Updated recommended time to {time_value} minutes in {xml_file}")
    
    content = read_file(xml_file)
    # Process each subsection in the matched HTML section
    for subsection in matching_section['subsections']:
        if not subsection['ref']:
            continue
        content, count = update_xml_content(content, subsection)
        if count:
            print(f"  - Updated {count} instance(s) of '{subsection['ref']}' in {xml_file}")
        else:
            print(f"  - No matches found for '{subsection['ref']}' in {xml_file}")
    write_file(xml_file, content)
    print(f"Updated {xml_file} with content from '{matching_section['title']}'")

def update_lesson_file(lesson_plan_file, html_sections):
    """
    Update the main lesson plan file using the lesson-level HTML section.
    """
    content = read_file(lesson_plan_file)
    lesson_section = next((sec for sec in html_sections if sec['title'] == 'Lesson'), None)
    if not lesson_section:
        print("Warning: No lesson section found in HTML. Skipping lesson file updates.")
        return
    for subsection in lesson_section['subsections']:
        if not subsection['ref']:
            continue
        content, count = update_xml_content(content, subsection)
        if count:
            print(f"  - Updated {count} instance(s) of '{subsection['ref']}' in main lesson file")
        else:
            print(f"  - No matches found for '{subsection['ref']}' in main lesson file")
    write_file(lesson_plan_file, content)
    print(f"Updated main lesson file {lesson_plan_file}")

def update_time_values(lesson_plan_file, html_sections):
    """
    Update time values in the lesson plan file.
    Searches for time placeholders in the XML and replaces them with values from HTML sections.
    """
    content = read_file(lesson_plan_file)
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
                act_num = re.search(r'Activity (\d+)', section_name)
                if act_num:
                    num = act_num.group(1)
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
    write_file(lesson_plan_file, content)
    print(f"Updated time values in {lesson_plan_file}")

def update_synthesis_section(lesson_plan_file, html_sections):
    """
    Update the synthesis section of the lesson plan file.
    Replaces the synthesis block with the new content extracted from the HTML.
    """
    content = read_file(lesson_plan_file)
    lesson_id = extract_lesson_id(lesson_plan_file)
    synthesis_section = next((sec for sec in html_sections if sec['title'] == 'Lesson Synthesis'), None)
    if not synthesis_section or not synthesis_section['subsections']:
        print("Warning: No Lesson Synthesis section found in HTML. Skipping synthesis update.")
        return
    subsection = synthesis_section['subsections'][0]
    pattern = (r'<subsubsection xml:id="' + re.escape(lesson_id) +
               r'-sintesis".*?<p>\[@{9,}\]</p>\s*</subsubsection>')
    
    # Create replacement content
    synthesis_content = subsection['content']
    time_value = synthesis_section.get('time', '[@@@@@@@@@]')
    replacement = (
        f'<subsubsection xml:id="{lesson_id}-sintesis" component="profesor">\n'
        f'  <shorttitle><custom ref="synthesis-leccion-titulo"/></shorttitle>\n'
        f'  <title><custom ref="synthesis-leccion-titulo"/></title>\n'
        f'  <title component="profesor"><nbsp/>({time_value} mins)</title>\n\n'
        f'  <p>[+++++++++++++++]</p>\n'
        f'  {synthesis_content}\n\n'
        f'</subsubsection>'
    )
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count:
        write_file(lesson_plan_file, new_content)
        print(f"Updated Lesson Synthesis section in {lesson_plan_file}")
    else:
        print(f"Warning: Could not find Lesson Synthesis section in {lesson_plan_file}")

# -------------------------------
# Main Routine
# -------------------------------
def main():
    """
    Main function that orchestrates reading the HTML file, updating the main lesson file,
    updating time values, updating the synthesis section, and finally processing included XML files.
    """
    if len(sys.argv) != 3:
        print("Usage: python ingest_simple_lesson_content.py <lesson_plan_file> <html_content_file>")
        sys.exit(1)
    lesson_plan_file = sys.argv[1]
    html_file = sys.argv[2]

    # Extract the lesson ID for logging and processing purposes.
    lesson_id = extract_lesson_id(lesson_plan_file)
    print(f"Working with lesson ID: {lesson_id}")

    # Parse the HTML file to extract sections and subsections.
    html_sections = extract_html_sections(html_file)
    print("Extracted HTML sections:")
    for sec in html_sections:
        print(f"  - {sec['title']}")
        for sub in sec['subsections']:
            print(f"    - {sub['name']} (ref: {sub['ref']})")

    # Update the main lesson file and adjust time values and synthesis section.
    update_lesson_file(lesson_plan_file, html_sections)
    update_time_values(lesson_plan_file, html_sections)
    update_synthesis_section(lesson_plan_file, html_sections)

    # Process each included XML file based on the lesson plan file.
    included_files = find_included_files(lesson_plan_file)
    for file_label, xml_file in included_files:
        update_file(xml_file, html_sections, file_label)

    print("All files updated successfully!")

if __name__ == "__main__":
    main()

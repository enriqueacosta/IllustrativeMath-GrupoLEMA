#!/usr/bin/env python3
"""
Script to update XML lesson files with content from an HTML file.

Usage:
    python update_lesson_content.py <lesson_plan_file> <html_content_file>

Example:
    python update_lesson_content.py source/gra0-uni1/lec-explicarConteo.ptx lesson_extracted_launch_activity_synthesis.html
"""

import sys
import os
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom

def extract_html_sections(html_file):
    """Extract sections from the HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    sections = []
    current_section = None
    current_h2 = None
    
    # First, look for the lesson-level sections
    lesson_section = {
        'title': 'Lesson',
        'subsections': []
    }
    
    # Look for h3 elements with specific refs
    for ref_name, ref_id in [
        ('Lesson Purpose', 'purpose-leccion-titulo'),
        ('Lesson Narrative', 'narrative-leccion-titulo'),
        ('Teacher Reflection Questions', 'reflection-quest-titulo')
    ]:
        # Find h3 elements that might contain these sections
        for h3 in soup.find_all('h3'):
            if ref_name.lower() in h3.text.lower():
                # Find the next paragraph or text content
                next_element = h3.find_next(['p', 'ul'])
                if next_element:
                    lesson_section['subsections'].append({
                        'name': ref_name,
                        'ref': ref_id,
                        'content': str(next_element),
                        'type': next_element.name
                    })
                    break
    
    # Add the lesson section if it has any subsections
    if lesson_section['subsections']:
        sections.append(lesson_section)
    
    # Now extract the regular activity sections
    for element in soup.body.children:
        if element.name == 'h2':
            if current_section:
                sections.append(current_section)
            current_h2 = element.text
            current_section = {
                'title': current_h2,
                'subsections': []
            }
        elif element.name == 'h3' and current_section:
            # Extract the ref attribute from the h3 text
            h3_text = element.text
            ref_match = re.search(r'\(for ref="([^"]+)"\)', h3_text)
            ref = ref_match.group(1) if ref_match else None
            
            # Get the subsection name (without the ref part)
            subsection_name = re.sub(r'\s*\(for ref="[^"]+"\)', '', h3_text)
            
            # Find the next element after h3
            next_element = element.find_next()
            
            # Check if it's a ul or contains text like "NOT PRESENT"
            if next_element and next_element.name == 'ul':
                current_section['subsections'].append({
                    'name': subsection_name,
                    'ref': ref,
                    'content': str(next_element),
                    'type': 'ul'
                })
            else:
                # Look for text content that might indicate "NOT PRESENT"
                text_content = ""
                sibling = element.next_sibling
                while sibling and (not sibling.name or sibling.name != 'h3' and sibling.name != 'h2'):
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
    # Remove special characters and convert to lowercase
    normalized = re.sub(r'[^\w\s]', '', title).lower()
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

def find_included_files(lesson_plan_file):
    """Find all included files in the lesson plan and their titles."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract directory of the lesson plan file
    base_dir = os.path.dirname(lesson_plan_file)
    
    # Find all xi:include tags with their file paths
    include_pattern = r'<xi:include href="\./([^"]+)\.ptx"/>'
    all_includes = re.findall(include_pattern, content)
    
    # Create a list of file paths
    file_paths = [os.path.join(base_dir, f + '.ptx') for f in all_includes]
    
    # For each file, try to determine its title or activity number
    file_info = []
    
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        
        # Check if it's a warm-up file
        if "warm-" in file_name:
            file_info.append(("Warm-up", file_path))
        # Check if it's an activity file
        elif file_name.startswith("act-"):
            # Try to extract the activity number from the surrounding context
            act_pattern = r'<subsubsection xml:id="lec-explicarConteo-act(\d+)".*?<xi:include href="\./' + os.path.splitext(file_name)[0] + r'\.ptx"/>'
            act_match = re.search(act_pattern, content, re.DOTALL)
            
            if act_match:
                act_num = act_match.group(1)
                file_info.append((f"Activity {act_num}", file_path))
            else:
                # If we can't determine the activity number, just use the filename
                file_info.append((file_name, file_path))
    
    # Print all files that will be processed
    print(f"Found {len(file_info)} files to process:")
    for title, path in file_info:
        print(f"  - {title}: {path}")
    
    return file_info

def get_xml_file_title(xml_file):
    """Extract the title from an XML file."""
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_pattern = r'<title>(.*?)</title>'
    title_match = re.search(title_pattern, content)
    
    if title_match:
        return title_match.group(1).strip()
    
    return None

def update_xml_file(xml_file, html_sections):
    """Update an XML file with content from HTML sections."""
    if not os.path.exists(xml_file):
        print(f"Warning: File {xml_file} does not exist. Skipping.")
        return
    
    # Get the title of the XML file
    xml_title = get_xml_file_title(xml_file)
    if not xml_title:
        print(f"Warning: Could not extract title from {xml_file}. Skipping.")
        return
    
    # Get the filename without path
    file_basename = os.path.basename(xml_file)
    
    # Special case for the problematic file
    if "tableroConteoLlevarCuenta" in file_basename:
        print(f"Special handling for {file_basename}")
        # Find the Activity 2 section
        for section in html_sections:
            if "Activity 2:" in section['title']:
                matching_section = section
                print(f"Found direct match for {file_basename} with '{matching_section['title']}'")
                break
        else:
            print(f"Warning: Could not find Activity 2 section for {file_basename}. Skipping.")
            return
    else:
        # Normalize the XML title
        normalized_xml_title = normalize_title(xml_title)
        print(f"Looking for match for '{xml_title}' (normalized: '{normalized_xml_title}')")
        
        # Find the matching HTML section based on the title or filename
        matching_section = None
        
        # First try to match by normalized title
        for section in html_sections:
            section_title = section['title']
            normalized_section_title = normalize_title(section_title)
            
            # Print normalized titles for debugging
            print(f"  Comparing with '{section_title}' (normalized: '{normalized_section_title}')")
            
            # Check if the normalized XML title is in the normalized HTML section title
            # or if significant parts of the title match
            if normalized_xml_title in normalized_section_title or any(
                part in normalized_section_title 
                for part in normalized_xml_title.split() 
                if len(part) > 5
            ):
                matching_section = section
                print(f"  Found match by normalized title!")
                break
        
        # If no match by title, try to match by activity number or warm-up
        if not matching_section:
            if "warm-" in file_basename:
                # Find the warm-up section
                for section in html_sections:
                    if "warm-up" in normalize_title(section['title']):
                        matching_section = section
                        print(f"  Found match as warm-up!")
                        break
            else:
                # Try to extract activity number from filename
                act_match = re.search(r'act-.*?(\d+)', file_basename)
                if act_match:
                    act_num = act_match.group(1)
                    # Find the corresponding activity section
                    for section in html_sections:
                        if f"activity {act_num}" in normalize_title(section['title']):
                            matching_section = section
                            print(f"  Found match as Activity {act_num}!")
                            break
        
        # Last resort: try to match by keywords in the filename and section title
        if not matching_section:
            # Extract keywords from the filename
            keywords = re.findall(r'[a-zA-Z]+', file_basename)
            for section in html_sections:
                section_title = section['title']
                # Check if any keyword from the filename is in the section title
                for keyword in keywords:
                    if len(keyword) > 3 and keyword.lower() in normalize_title(section_title):
                        matching_section = section
                        print(f"  Found match by keyword '{keyword}'!")
                        break
                if matching_section:
                    break
    
    if not matching_section:
        print(f"Warning: No matching HTML section found for {xml_file} with title '{xml_title}'. Skipping.")
        return
    
    print(f"Matched {xml_file} with HTML section '{matching_section['title']}'")
    
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For each subsection in the matching HTML section
    for subsection in matching_section['subsections']:
        if not subsection['ref']:
            continue
        
        # Create the pattern to find the corresponding section in the XML
        pattern = r'<paragraphs>\s*<title><custom ref="' + subsection['ref'] + r'"/></title>.*?</paragraphs>'
        
        # Create the replacement XML based on the content type
        if subsection.get('type') == 'ul':
            # Apply indentation to the HTML content
            indented_content = indent_html_content(subsection['content'])
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    {indented_content}\n  </paragraphs>'
        elif subsection.get('type') == 'text' and subsection['content'] == 'NOT PRESENT':
            # For "NOT PRESENT" sections, keep the original placeholder
            if subsection['ref'] == 'support-actividad-titulo':
                replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    <p>[@@@@@@@@@]</p>\n  </paragraphs>'
            else:
                # For other sections, use empty content
                replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    <p></p>\n  </paragraphs>'
        elif subsection.get('type') == 'p':
            # For paragraph content
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    {subsection["content"]}\n  </paragraphs>'
        else:
            # Default case
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    <p>[@@@@@@@@@]</p>\n  </paragraphs>'
        
        # Replace in the content
        match_count = 0
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=0)
        
        # Check if any replacements were made
        if new_content != content:
            match_count += 1
            content = new_content
        
        if match_count > 0:
            print(f"  - Updated {match_count} instances of '{subsection['ref']}' in {xml_file}")
        else:
            print(f"  - No matches found for '{subsection['ref']}' in {xml_file}")
    
    # Write the updated content back to the file
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {xml_file} with content from '{matching_section['title']}'")

def indent_html_content(html_content):
    """Apply proper indentation to HTML content without adding too many line breaks."""
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get the ul element
    ul = soup.find('ul')
    if not ul:
        return html_content
    
    # Start with the opening ul tag
    result = "<ul>\n"
    
    # Process each li element
    for li in ul.find_all('li', recursive=False):
        result += "      <li>"
        
        # Check if the li contains a q tag
        q_tags = li.find_all('q')
        if q_tags:
            for q in q_tags:
                # Replace the q tag with properly indented version
                q_content = str(q.string) if q.string else ""
                result += f"\n        <q>{q_content}</q>"
                # Remove the q tag from the li content
                q.extract()
            
            # Add any remaining content in the li
            if li.contents:
                for content in li.contents:
                    if content.strip():
                        result += f" {content.strip()}"
            
            # Add a line break before closing the li tag
            result += "\n      </li>\n"
        else:
            # No q tags, just add the li content and close the tag on the same line
            result += f"{li.get_text().strip()}</li>\n"
    
    # Close the ul tag
    result += "    </ul>"
    
    return result

def update_lesson_file(lesson_plan_file, html_sections):
    """Update the main lesson file with content from HTML sections."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the lesson section
    lesson_section = None
    for section in html_sections:
        if section['title'] == 'Lesson':
            lesson_section = section
            break
    
    if not lesson_section:
        print("Warning: No lesson section found in HTML. Skipping lesson file updates.")
        return
    
    # Update each subsection in the lesson file
    for subsection in lesson_section['subsections']:
        if not subsection['ref']:
            continue
        
        # Create the pattern to find the corresponding section in the XML
        pattern = r'<paragraphs>\s*<title><custom ref="' + subsection['ref'] + r'"/></title>.*?</paragraphs>'
        
        # Create the replacement XML based on the content type
        if subsection['type'] == 'ul':
            # Apply indentation to the HTML content
            indented_content = indent_html_content(subsection['content'])
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    {indented_content}\n  </paragraphs>'
        elif subsection['type'] == 'p':
            # For paragraph content
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    {subsection["content"]}\n  </paragraphs>'
        else:
            # Default case
            replacement = f'<paragraphs>\n    <title><custom ref="{subsection["ref"]}"/></title>\n    <p>[@@@@@@@@@]</p>\n  </paragraphs>'
        
        # Replace in the content
        match_count = 0
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=0)
        
        # Check if any replacements were made
        if new_content != content:
            match_count += 1
            content = new_content
        
        if match_count > 0:
            print(f"  - Updated {match_count} instances of '{subsection['ref']}' in main lesson file")
        else:
            print(f"  - No matches found for '{subsection['ref']}' in main lesson file")
    
    # Write the updated content back to the file
    with open(lesson_plan_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated main lesson file {lesson_plan_file}")

def update_time_values(lesson_plan_file, html_sections):
    """Update time values in the lesson plan file."""
    with open(lesson_plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For each section in the HTML
    for section in html_sections:
        # Extract time from the title
        time_match = re.search(r'\((\d+) minutes\)', section['title'])
        if time_match:
            time_value = time_match.group(1)
            
            # Create pattern to find the corresponding section in the XML
            section_name = section['title'].split(':')[0].strip()
            if "Warm-up" in section_name:
                pattern = r'<subsubsection xml:id="lec-explicarConteo-warm".*?<title component="profesor"><nbsp/>\(.*?mins\)</title>'
                replacement = f'<subsubsection xml:id="lec-explicarConteo-warm" component="no-libroTrabajo">\n  <shorttitle><custom ref="warm-up-leccion-titulo"/></shorttitle>\n  <title><custom ref="warm-up-leccion-titulo"/></title>\n  <!-- Tiempo en el título que solo ve el profesor -->\n  <title component="profesor"><nbsp/>({time_value} mins)</title>'
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            elif "Activity" in section_name:
                # Extract activity number
                activity_num = re.search(r'Activity (\d+)', section_name)
                if activity_num:
                    num = activity_num.group(1)
                    pattern = r'<subsubsection xml:id="lec-explicarConteo-act' + num + r'".*?<title component="profesor"><nbsp/>\(.*?mins\)</title>'
                    replacement = f'<subsubsection xml:id="lec-explicarConteo-act{num}" component="no-libroTrabajo">\n  <shorttitle>Actividad {num}</shorttitle>\n  <title>Actividad {num}</title>\n  <!-- Tiempo en el título que solo ve el profesor -->\n  <title component="profesor"><nbsp/>({time_value} mins)</title>'
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(lesson_plan_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated time values in {lesson_plan_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_lesson_content.py <lesson_plan_file> <html_content_file>")
        sys.exit(1)
    
    lesson_plan_file = sys.argv[1]
    html_file = sys.argv[2]
    
    # Extract sections from the HTML file
    html_sections = extract_html_sections(html_file)
    
    # Print all extracted sections for debugging
    print("Extracted HTML sections:")
    for section in html_sections:
        print(f"  - {section['title']}")
        for subsection in section['subsections']:
            print(f"    - {subsection['name']} (ref: {subsection['ref']})")
    
    # Update the main lesson file with lesson-level content
    update_lesson_file(lesson_plan_file, html_sections)
    
    # Update time values in the lesson plan file
    update_time_values(lesson_plan_file, html_sections)
    
    # Find all included files and their titles
    included_files = find_included_files(lesson_plan_file)
    
    # Update each included file
    for title, xml_file in included_files:
        update_xml_file(xml_file, html_sections)
    
    print("All files updated successfully!")

if __name__ == "__main__":
    main() 
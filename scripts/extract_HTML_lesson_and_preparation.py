"""
extract_HTML_lesson_and_preparation.py

This script extracts specific sections from two different lesson HTML files inside a given folder:
- From preparation.html: "Lesson Purpose", "Lesson Narrative", "Teacher Reflection Questions"
- From lesson.html: "Launch", "Activity", "Activity Synthesis", "Advancing Student Thinking"
- Also extracts "Lesson Synthesis" section from lesson.html

The extracted sections from preparation.html appear first under an <h2> titled "Lesson Fields",
followed by the "Lesson Synthesis" section, then the sections from lesson.html under their respective headings.

Processing:
- Removes unnecessary tags.
- Replaces straight quotes with <q> tags.
- Converts sequences of three or more underscores (_____) into <fillin/>.
- Ensures <fillin/> is displayed as "_____" using CSS.
- Places math in <m> tags: change <span class="math math-repaired">\(CONTENT\)</span> to <m>CONTENT</m>
- Drops <span> tags but keeps the content inside them
- Drops <div class="imgrid"> tags and their contents except for <img> tags
- Drops <figure> tags and their contents except for <img> tags
- Drops <div class="c-annotation c-annotation--ell"> tags and their contents
- Drops <div class="c-annotation c-annotation--swd"> tags and their contents
- Drops <div class="c-annotations"> tags and their contents
- Wraps text inside <li> tags with <p> tags when there is a nested <ul>
- Formats raw HTML properly inside <pre><code> blocks.
- Allows stripping of duplicate <q> tags after // if specified.
- Saves extracted content into a single output file.

Usage:
    python extract_HTML_lesson_and_preparation.py path/to/folder [--no-raw-html] [--strip-qtags]

Arguments:
    - path/to/folder : Path to the folder containing preparation.html and lesson.html.
    - --no-raw-html  : Disable raw HTML inside <pre><code> blocks.
    - --strip-qtags  : Remove second <q>...</q> after //, keeping parentheses.

Output:
    - lesson_extracted_combined.html saved in the same folder.
"""

import argparse
import os
import sys
import re
from bs4 import BeautifulSoup, NavigableString, Tag

def clean_q_tags(text):
    """Removes duplicate <q>...</q> pairs after // while keeping text inside parentheses."""
    pattern = re.compile(r'(<q>.*?</q>)\s*//\s*<q>.*?</q>(\s*\(.*?\))?', re.DOTALL)
    return re.sub(pattern, r'\1\2', text)

def replace_underscores_with_fillin(text):
    """Replaces three or more underscores (_____) with <fillin/>."""
    return re.sub(r'_{3,}', '<fillin/>', text)

def format_raw_html(html):
    """Formats HTML with 2-space indentation while keeping inline elements intact."""
    soup = BeautifulSoup(html, "html.parser")
    formatted_html = soup.prettify(formatter=None).replace("    ", "  ")
    formatted_html = re.sub(r"<fillin>\s*</fillin>", "<fillin/>", formatted_html)
    formatted_html = re.sub(r">\s*\n\s*([^<>\s].*?)\s*\n\s*<", r"> \1 <", formatted_html)
    return formatted_html.strip()

def extract_preparation_sections(soup, include_raw_html=True, strip_qtags=False):
    """Extracts sections from preparation.html."""
    sections_to_extract = {
        "Lesson Purpose": "<p>=== NOT PRESENT ===</p>",
        "Lesson Narrative": "<p>=== NOT PRESENT ===</p>",
        "Teacher Reflection Questions": "<p>=== NOT PRESENT ===</p>"
    }

    for heading in soup.find_all("h3", class_="im-c-heading--xsb"):
        heading_text = heading.get_text(strip=True)
        if heading_text in sections_to_extract:
            content_div = heading.find_next("div", class_="im-c-content")
            if content_div:
                extracted_content = process_content(content_div, include_raw_html, strip_qtags)
                sections_to_extract[heading_text] = extracted_content

    return sections_to_extract

def extract_lesson_sections(soup, include_raw_html=True, strip_qtags=False):
    """Extracts sections from lesson.html."""
    grouped_sections = {}
    titles = soup.find_all("h2", class_="im-c-hero__heading")

    for title in titles:
        title_text = title.get_text(strip=True)
        # if "Cool-down" in title_text:
            # continue

        section = title.find_next("div", class_="im-c-container--content")
        if section:
            grouped_sections[title_text] = {
                "Narrative": [],
                "Launch": [],
                "Activity": [],
                "Activity Synthesis": [],
                "Advancing Student Thinking": "<p>=== NOT PRESENT ===</p>",
                "Student Response": []
            }

            section_rows = section.find_all("div", class_="im-c-row")

            for row in section_rows:
                heading = row.find("h3")
                if heading:
                    content = row.find("div", class_="im-c-content")
                    if content:
                        extracted_content = process_content(content, include_raw_html, strip_qtags)
                        if "Narrative" in heading.text:
                            grouped_sections[title_text]["Narrative"].append(extracted_content)
                        elif "Launch" in heading.text:
                            grouped_sections[title_text]["Launch"].append(extracted_content)
                        elif "Activity Synthesis" in heading.text:
                            grouped_sections[title_text]["Activity Synthesis"].append(extracted_content)
                        elif "Activity" in heading.text:
                            grouped_sections[title_text]["Activity"].append(extracted_content)
                        elif "Advancing Student Thinking" in heading.text:
                            grouped_sections[title_text]["Advancing Student Thinking"] = extracted_content
                        elif "Student Response" in heading.text:
                            grouped_sections[title_text]["Student Response"].append(extracted_content)

    return grouped_sections

def extract_lesson_synthesis(soup, include_raw_html=True, strip_qtags=False):
    """Extracts the Lesson Synthesis section from lesson.html."""
    synthesis_title = soup.find("h2", class_="im-c-hero__heading", string=lambda text: "Lesson Synthesis" in text)
    
    if not synthesis_title:
        return "<p>=== NOT PRESENT ===</p>"
    
    section = synthesis_title.find_next("div", class_="im-c-container--content")
    if not section:
        return "<p>=== NOT PRESENT ===</p>"
    
    content_div = section.find("div", class_="im-c-content")
    if not content_div:
        return "<p>=== NOT PRESENT ===</p>"
    
    extracted_content = process_content(content_div, include_raw_html, strip_qtags)
    return extracted_content

def process_content(content, include_raw_html, strip_qtags):
    """Processes and cleans up extracted content."""
    
    for em_tag in content.find_all("em", class_="spanish-translation translation"):
        next_sibling = em_tag.find_next_sibling()
        if next_sibling and next_sibling.name == "em" and not next_sibling.text.strip():
            next_sibling.extract()
        em_tag.unwrap()

    # grab only the <img> tags inside <div class="imgrid">
    imgrid_divs = content.find_all("div", class_="imgrid")
    for div in imgrid_divs:
        # Find all descendant <img> tags
        img_tags = div.find_all("img")

        # Insert each img tag before the current div (preserving order)
        for img in img_tags:
            warning_html = BeautifulSoup("\n<p>[@@@@@@@@] WARNING: Fix Image.</p>\n", "html.parser")
            div.insert_before(warning_html)
            div.insert_before(img)
        # Remove the entire div
        div.decompose()
    
    # grab only the <img> tags inside <figure>
    figure_tags = content.find_all("figure")
    for figure in figure_tags:
        # Find all descendant <img> tags
        img_tags = figure.find_all("img")
        # Insert each img tag before the current figure (preserving order)
        for img in img_tags:
            warning_html = BeautifulSoup("\n<p>[@@@@@@@@] WARNING: Fix Image.</p>\n", "html.parser")
            figure.insert_before(warning_html)
            figure.insert_before(img)
        # Remove the entire figure
        figure.decompose()

    # print(content)

    # Convert extracted content to string and remove the outer <div> tag
    extracted_content = "".join(str(tag) for tag in content.contents)

    # remove tabs
    extracted_content = extracted_content.replace("\t", "")

    # If a <li> has <ul> tags inside, make sure to add <p> tags to any parts that don't have tags but don't absorb the \n if the text that gets wrapped
    # extracted_content = re.sub(r'(<li[^>]*>)([^<]+)(\s*<ul>)', r'\1<p>\2</p>\n\3', extracted_content)
    extracted_content = re.sub(r'(<li[^>]*>)([^<]+)\n(\s*<ul>)', r'\1<p>\2</p>\n\3', extracted_content)

    # Ensure content is wrapped in <p> if it's missing block-level tags
    if not any(tag in extracted_content for tag in ["<p", "<ul", "<ol", "<table", "<div"]):
        extracted_content = f"<p>{extracted_content.strip()}</p>"

    # Replace non-breaking spaces by normal spaces
    extracted_content = extracted_content.replace("\xa0", " ")

    # remove zero width space
    extracted_content = re.sub(r'\u200b', '', extracted_content)

    # Convert curly quotes into <q> tags
    extracted_content = extracted_content.replace("“", "<q>").replace("”", "</q>")

    # Apply <q> tag cleanup if --strip-qtags is enabled
    if strip_qtags:
        extracted_content = clean_q_tags(extracted_content)

    # Apply <fillin/> replacement
    extracted_content = replace_underscores_with_fillin(extracted_content)

    # Drop ELL supports <div class="c-annotation c-annotation--ell"> tags and their contents
    extracted_content = re.sub(r'<div class="c-annotation c-annotation--ell">.*?</div>', '', extracted_content, flags=re.DOTALL)

    # Drop accessinility <div class="c-annotation c-annotation--swd"> tags and their contents
    extracted_content = re.sub(r'<div class="c-annotation c-annotation--swd">.*?</div>', '', extracted_content, flags=re.DOTALL)

    # Drop <div class="c-annotations"> tags and their contents
    extracted_content = re.sub(r'<div class="c-annotations">.*?</div>', '', extracted_content, flags=re.DOTALL)

    # Drop empty <p> tags
    extracted_content = re.sub(r'<p>\s*</p>', '', extracted_content)

    # Drop <br/> tags
    extracted_content = re.sub(r'<br\s*/?>\s*', ' ', extracted_content)

    # place math in <m> tags: change <span class="math math-repaired">\(CONTENT\)</span> to <m>CONTENT</m>
    extracted_content = re.sub(r'<span class="math math-repaired">\\\((.*?)\\\)</span>', r'<m>\1</m>', extracted_content)

    # Drop <span> tags but keep the content inside them
    extracted_content = re.sub(r'<span>(.*?)</span>', r'\1', extracted_content)

    # If a <li> has a "<p>[@@@@@@@@] WARNING: " fig warning, make sure to add <p> tags to any parts that don't have tags but don't absorb the \n if the text that gets wrapped
    extracted_content = re.sub(r'(<li[^>]*>)([^<]+)(\s*<p>\[@@@@@@@@\] WARNING:)', r'\1<p>\2</p>\3', extracted_content)


    formatted_raw_html = format_raw_html(extracted_content) if include_raw_html else ""
    raw_html = f"<pre><code>{formatted_raw_html.replace('<', '&lt;').replace('>', '&gt;')}</code></pre>" if include_raw_html else ""

    return extracted_content + raw_html

def save_combined_sections(prep_sections, lesson_sections, lesson_synthesis, output_filename):
    """Saves combined extracted sections to an HTML file."""
    output_content = (
        "<html>\n"
        "<head>\n"
        "  <title>Extracted Lesson and Preparation Sections</title>\n"
        "  <style> fillin::before { content: \"_____\"; font-family: monospace; } </style>\n"
        "  <style> m::before { content: \"<m>\"; } </style>\n"
        "  <style> m::after { content: \"</m>\"; } </style>\n"
        "</head>\n"
        "<body>\n"
    )

    output_content += "\n<h2>Lesson Fields</h2>\n"

    output_content += "\n<h3>Lesson Purpose (for ref=\"purpose-leccion-titulo\")</h3>\n" + prep_sections["Lesson Purpose"]
    output_content += "\n<h3>Lesson Narrative (for ref=\"narrative-leccion-titulo\")</h3>\n" + prep_sections["Lesson Narrative"]
    output_content += "\n<h3>Teacher Reflection Questions (for ref=\"reflection-quest-titulo\")</h3>\n" + prep_sections["Teacher Reflection Questions"]
    
    # Add Lesson Synthesis after Lesson Fields and before other h2 sections
    output_content += "\n<h2>Lesson Synthesis </h2>\n" + lesson_synthesis

    for title, sections in lesson_sections.items():
        output_content += f"\n<h2>{title}</h2>\n"
        output_content += "\n<h3>Narrative (for ref=\"narrative-actividad-titulo\")</h3>\n" + "".join(sections["Narrative"])
        output_content += "\n<h3>Launch (for ref=\"launch-titulo\")</h3>\n" + "".join(sections["Launch"])
        output_content += "\n<h3>Activity (for ref=\"instructions-teacher-actividad-titulo\")</h3>\n" + "".join(sections["Activity"])
        output_content += "\n<h3>Activity Synthesis (for ref=\"synthesis-actividad-titulo\")</h3>\n" + "".join(sections["Activity Synthesis"])
        output_content += "\n<h3>Advancing Student Thinking (for ref=\"support-actividad-titulo\")</h3>\n" + sections["Advancing Student Thinking"]
        output_content += "\n<h3>Student Response (for solution)</h3>\n" + "".join(sections["Student Response"])

    output_content += "\n</body>\n</html>"

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(output_content)

    print(f"✅ Extraction completed! Output saved to: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract lesson and preparation sections from HTML files in a folder.")
    parser.add_argument("folder_path", help="Path to the folder containing preparation.html and lesson.html")
    parser.add_argument("--no-raw-html", action="store_true", help="Disable raw HTML inside <pre><code> blocks")
    parser.add_argument("--strip-qtags", action="store_true", help="Remove duplicate <q>...</q> tags.")

    args = parser.parse_args()

    prep_file = os.path.join(args.folder_path, "preparation.html")
    lesson_file = os.path.join(args.folder_path, "lesson.html")

    if not os.path.exists(prep_file) or not os.path.exists(lesson_file):
        print("\n❌ Error: Both 'preparation.html' and 'lesson.html' must be in the specified folder.\n")
        sys.exit(1)

    with open(prep_file, "r", encoding="utf-8") as file:
        prep_soup = BeautifulSoup(file, "html.parser")

    with open(lesson_file, "r", encoding="utf-8") as file:
        lesson_soup = BeautifulSoup(file, "html.parser")

    prep_sections = extract_preparation_sections(prep_soup, not args.no_raw_html, args.strip_qtags)
    lesson_sections = extract_lesson_sections(lesson_soup, not args.no_raw_html, args.strip_qtags)
    lesson_synthesis = extract_lesson_synthesis(lesson_soup, not args.no_raw_html, args.strip_qtags)

    save_combined_sections(prep_sections, lesson_sections, lesson_synthesis, os.path.join(args.folder_path, "lesson_extracted_combined.html"))
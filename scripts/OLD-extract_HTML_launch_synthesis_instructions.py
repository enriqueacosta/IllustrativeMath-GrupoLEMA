"""
extract_HTML_launch_synthesis_instructions.py

This script extracts specific sections (Launch, Activity, Activity Synthesis, and Advancing Student Thinking)
from a lesson HTML file. It processes the content, removes unnecessary tags, replaces straight quotes with <q> tags,
and includes raw HTML inside <pre><code>...</code></pre> blocks by default.

Additionally:
- Sequences of five or more underscores (_____) are replaced with <fillin/>.
- The raw HTML output is **properly indented (2 spaces)** inside <pre><code>.
- <fillin/> is displayed as "_____" in the rendered HTML using CSS.

Usage:
    python extract_HTML_launch_synthesis_instructions.py path/to/lesson.html [--no-raw-html] [--strip-qtags]

Arguments:
    - `path/to/lesson.html` : Path to the input HTML file.
    - `--no-raw-html`       : Disable raw HTML inside <pre><code> blocks.
    - `--strip-qtags`       : Remove second <q>...</q> after `//`, keeping parentheses.

Output:
    - Extracted content is saved as `lesson_extracted_launch_activity_synthesis.html`
      in the same directory as the input file.

Examples:
    python extract_HTML_launch_synthesis_instructions.py lesson.html --no-raw-html --strip-qtags
"""

import argparse
import os
import sys
import re
from bs4 import BeautifulSoup

def clean_q_tags(text):
    """
    Processes <q> tags to remove duplicate paired <q>...</q> after "//",
    while keeping any text in parentheses that follows.
    """
    pattern = re.compile(r'(<q>.*?</q>)\s*//\s*<q>.*?</q>(\s*\(.*?\))?', re.DOTALL)
    cleaned_text = re.sub(pattern, r'\1\2', text)
    return cleaned_text

def replace_underscores_with_fillin(text):
    """
    Replaces instances of five or more underscores (_____) with <fillin/>.
    """
    return re.sub(r'_{4,}', '<fillin/>', text)

def format_raw_html(html):
    """Formats HTML with 2-space indentation while preserving inline elements and keeping the original structure intact."""
        
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Convert to properly indented HTML with 2 spaces instead of 4
    formatted_html = soup.prettify(formatter=None).replace("    ", "  ")

    # Ensure <fillin/> stays self-closing and does not add extra line breaks
    formatted_html = re.sub(r"<fillin>\s*</fillin>", "<fillin/>", formatted_html)

    # Preserve spaces around <fillin/> only if they existed in the original input
    formatted_html = re.sub(r"\s*<fillin/>\s*", lambda m: f" {m.group().strip()} " if " " in m.group() else "<fillin/>", formatted_html)

    # Remove unwanted newlines between inline elements while keeping necessary line breaks
    formatted_html = re.sub(r">\s*\n\s*([^<>\s].*?)\s*\n\s*<", r"> \1 <", formatted_html)

    return formatted_html.strip()


def extract_sections(html_file, include_raw_html=True, strip_qtags=False):
    """Extracts lesson sections from the given HTML file and saves the cleaned output."""
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except FileNotFoundError:
        print(f"❌ Error: The file '{html_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: Unable to read the file '{html_file}'.\n{str(e)}")
        sys.exit(1)

    grouped_sections = {}

    # Find all h2 elements which represent the titles
    titles = soup.find_all("h2", class_="im-c-hero__heading")

    # Iterate through all titles and extract relevant sections while avoiding "Cool-down"
    for title in titles:
        title_text = title.get_text(strip=True)
        
        if "Cool-down" in title_text:
            continue  # Skip "Cool-down" sections

        section = title.find_next("div", class_="im-c-container--content")

        if section:
            grouped_sections[title_text] = {
                "Launch": [],
                "Activity": [],
                "Activity Synthesis": [],
                "Advancing Student Thinking": "--- NOT PRESENT ---"
            }

            section_rows = section.find_all("div", class_="im-c-row")

            for row in section_rows:
                heading = row.find("h3")
                if heading:
                    content = row.find("div", class_="im-c-content")
                    if content:
                        # Remove <em class="spanish-translation translation"> and any empty <em> following it
                        for em_tag in content.find_all("em", class_="spanish-translation translation"):
                            next_sibling = em_tag.find_next_sibling()
                            if next_sibling and next_sibling.name == "em" and not next_sibling.text.strip():
                                next_sibling.extract()  # Remove empty <em> following it
                            em_tag.unwrap()  # Remove the translation <em>

                        # Replace straight quotes with <q> tags
                        for text_node in content.find_all(string=True):
                            if "“" in text_node or "”" in text_node:
                                new_text = text_node.replace("“", "<q>").replace("”", "</q>")
                                text_node.replace_with(BeautifulSoup(new_text, "html.parser"))

                        # Remove the <div class="im-c-content"> but keep its inner content
                        extracted_content = "".join(str(tag) for tag in content.contents)

                        # replace non-breaking spaces with normal spaces
                        extracted_content = extracted_content.replace("\xa0", " ")

                        # Apply <q> tag cleanup if enabled
                        if strip_qtags:
                            extracted_content = clean_q_tags(extracted_content)

                        # Apply <fillin/> replacement to both formatted and raw content
                        extracted_content = replace_underscores_with_fillin(extracted_content)

                        # Format raw HTML properly with 2-space indentation
                        formatted_raw_html = format_raw_html(extracted_content) if include_raw_html else ""
                        raw_html = f"<pre><code>{formatted_raw_html.replace('<', '&lt;').replace('>', '&gt;')}</code></pre>" if include_raw_html else ""

                        # Append formatted content first, followed by the processed raw HTML
                        combined_content = extracted_content + raw_html

                        # Classify the section correctly
                        if "Launch" in heading.text:
                            grouped_sections[title_text]["Launch"].append(combined_content)
                        elif "Activity Synthesis" in heading.text:
                            grouped_sections[title_text]["Activity Synthesis"].append(combined_content)
                        elif "Activity" in heading.text:
                            grouped_sections[title_text]["Activity"].append(combined_content)
                        elif "Advancing Student Thinking" in heading.text:
                            grouped_sections[title_text]["Advancing Student Thinking"] = combined_content

    # Generate updated grouped HTML output
    corrected_html_output = """<html><head>
    <style> fillin::before { content: "_____"; font-family: monospace; } </style>
    </head><body>"""
    
    for title, sections in grouped_sections.items():
        corrected_html_output += f"<h2>{title}</h2>\n"
        corrected_html_output += "<h3>Launch (for ref=\"launch-titulo\")</h3>\n" + "".join(sections["Launch"])
        corrected_html_output += "<h3>Activity (for ref=\"instructions-teacher-actividad-titulo\")</h3>\n" + "".join(sections["Activity"])
        corrected_html_output += "<h3>Activity Synthesis (for ref=\"synthesis-actividad-titulo\")</h3>\n" + "".join(sections["Activity Synthesis"])
        corrected_html_output += "<h3>Advancing Student Thinking (for ref=\"support-actividad-titulo\")</h3>\n" + (
            sections["Advancing Student Thinking"] if isinstance(sections["Advancing Student Thinking"], str) 
            else "--- NOT PRESENT ---"
        )

    corrected_html_output += "</body></html>"

    output_file = os.path.join(os.path.dirname(html_file), "lesson_extracted_launch_activity_synthesis.html")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(corrected_html_output)

    print(f"✅ Extraction completed! Output saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract Launch, Activity, Activity Synthesis, and Advancing Student Thinking sections from a lesson HTML file."
    )
    parser.add_argument("html_file", nargs="?", help="Path to the lesson.html file")
    parser.add_argument("--no-raw-html", action="store_true", help="Disable raw HTML inside <pre><code> blocks")
    parser.add_argument("--strip-qtags", action="store_true", help="Remove second <q>...</q> after '//' but keep text in parentheses.")

    args = parser.parse_args()

    if not args.html_file:
        print("\n❌ Error: No input file provided.\n")
        print("Usage:")
        print("  python extract_HTML_launch_synthesis_instructions.py path/to/lesson.html [--no-raw-html] [--strip-qtags]")
        sys.exit(1)

    extract_sections(args.html_file, not args.no_raw_html, args.strip_qtags)

#!/usr/bin/env python3

"""
Lista todos los xml:ids de una unidad (lec, warm, act, cool) ordenados por número de lección.

Usage: python list_unit_xmlids.py <unit-folder (full path)>

Creado con la ayuda de Claude 3.5 Sonnet
Enrique Acosta, Abril 2025
"""

import os
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Activity:
    file_name: str
    xml_id: str
    title: Optional[str] = None
    activity_type: str = "activity"  # Can be "warmup", "activity", or "cooldown"
    activity_number: Optional[int] = None

@dataclass
class Lesson:
    file_name: str
    xml_id: str
    lesson_number: int
    title: str
    warmup: Optional[Activity] = None
    activities: List[Activity] = None
    cooldown: Optional[Activity] = None

def extract_xml_id(file_path: str) -> str:
    """Extract xml:id from a PTX file."""
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "xml")
            # Find first element with xml:id attribute
            element = soup.find(attrs={"xml:id": True})
            if element:
                return element["xml:id"]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return ""

def extract_title(file_path: str) -> str:
    """Extract title from a PTX file."""
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "xml")
            
            # For lesson files, get the third title tag in the root subsection
            if "lec-" in file_path:
                subsection = soup.find("subsection")
                if subsection:
                    # Get only direct children title tags
                    titles = [t for t in subsection.find_all("title", recursive=False)]
                    # The real title is the third one (index 2)
                    if len(titles) > 2:
                        return titles[2].text.strip()
            
            # For other files, get first title
            title = soup.find("title")
            if title:
                return title.text.strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return ""

def extract_lesson_number(file_path: str) -> int:
    """Extract lesson number from a PTX file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "xml")
            shorttitle = soup.find("shorttitle")
            if shorttitle:
                text = shorttitle.text.strip()
                # Extract number from "Lección X"
                match = re.search(r'Lección\s+(\d+)', text)
                if match:
                    return int(match.group(1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return 0

def find_included_files(lesson_file: str) -> tuple[Optional[str], List[str], Optional[str]]:
    """Find warmup, activities and cooldown files included in a lesson file."""
    try:
        with open(lesson_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        warmup = None
        activities = []
        cooldown = None
        
        # Parse XML with BeautifulSoup
        soup = BeautifulSoup(content, "xml")
        
        # Find warmup section and its included file
        warm_section = soup.find("subsubsection", attrs={"component": "warms"})
        if warm_section:
            include = warm_section.find("xi:include")
            if include and "href" in include.attrs:
                warmup_file = include["href"].replace("./", "")
                if not warmup_file.endswith(".ptx"):
                    warmup_file += ".ptx"
                warmup_path = os.path.join(os.path.dirname(lesson_file), warmup_file)
                if os.path.exists(warmup_path):
                    warmup = warmup_file
        
        # Find activity sections and their included files
        act_sections = soup.find_all("subsubsection", attrs={"component": lambda x: x and x.startswith("acts-")})
        for act_section in act_sections:
            include = act_section.find("xi:include")
            if include and "href" in include.attrs:
                act_file = include["href"].replace("./", "")
                if not act_file.endswith(".ptx"):
                    act_file += ".ptx"
                act_path = os.path.join(os.path.dirname(lesson_file), act_file)
                if os.path.exists(act_path):
                    activities.append(act_file)
        
        # Find cooldown section and its included file
        cool_section = soup.find("reading-questions", attrs={"component": "cools"})
        if cool_section:
            include = cool_section.find("xi:include")
            if include and "href" in include.attrs:
                cool_file = include["href"].replace("./", "")
                if not cool_file.endswith(".ptx"):
                    cool_file += ".ptx"
                cool_path = os.path.join(os.path.dirname(lesson_file), cool_file)
                if os.path.exists(cool_path):
                    cooldown = cool_file
                    
        return warmup, activities, cooldown
        
    except Exception as e:
        print(f"Error processing {lesson_file}: {e}")
        return None, [], None

def process_unit_folder(unit_folder: str) -> List[Lesson]:
    """Process all lessons in a unit folder and return structured data."""
    lessons = []
    
    # Get absolute path
    unit_path = os.path.abspath(unit_folder)
    
    # Find all lesson files
    lesson_files = []
    for f in os.listdir(unit_path):
        if f.startswith("lec-") and f.endswith(".ptx"):
            lesson_files.append(os.path.join(unit_path, f))
    
    # Process each lesson file
    for lesson_file in sorted(lesson_files):
        # Extract lesson info
        lesson_xml_id = extract_xml_id(lesson_file)
        lesson_number = extract_lesson_number(lesson_file)
        lesson_title = extract_title(lesson_file)
        
        # Find included files
        warmup_file, activity_files, cooldown_file = find_included_files(lesson_file)
        
        # Create lesson activities
        activities = []
        if warmup_file:
            warmup_path = os.path.join(unit_path, warmup_file)
            if os.path.exists(warmup_path):
                warmup = Activity(
                    file_name=warmup_file,
                    xml_id=extract_xml_id(warmup_path),
                    title=extract_title(warmup_path),
                    activity_type="warmup"
                )
            else:
                warmup = None
        else:
            warmup = None
            
        for i, act_file in enumerate(activity_files, 1):
            act_path = os.path.join(unit_path, act_file)
            if os.path.exists(act_path):
                activity = Activity(
                    file_name=act_file,
                    xml_id=extract_xml_id(act_path),
                    title=extract_title(act_path),
                    activity_type="activity",
                    activity_number=i
                )
                activities.append(activity)
            
        if cooldown_file:
            cooldown_path = os.path.join(unit_path, cooldown_file)
            if os.path.exists(cooldown_path):
                cooldown = Activity(
                    file_name=cooldown_file,
                    xml_id=extract_xml_id(cooldown_path),
                    title=extract_title(cooldown_path),
                    activity_type="cooldown"
                )
            else:
                cooldown = None
        else:
            cooldown = None
            
        # Create lesson object
        lesson = Lesson(
            file_name=os.path.basename(lesson_file),
            xml_id=lesson_xml_id,
            lesson_number=lesson_number,
            title=lesson_title,
            warmup=warmup,
            activities=activities,
            cooldown=cooldown
        )
        
        lessons.append(lesson)
    
    # Sort lessons by number
    lessons.sort(key=lambda x: x.lesson_number)
    return lessons

def print_lesson_structure(lessons: List[Lesson]):
    """Print the lesson structure in a readable format."""
    for lesson in lessons:
        print(f"\nLección {lesson.lesson_number}:")
        print(f"* file: {lesson.file_name}")
        print(f"* xml:id: {lesson.xml_id}")
        print(f"* title: {lesson.title}")
        
        if lesson.warmup:
            print("* warmup:")
            print(f"  - file: {lesson.warmup.file_name}")
            print(f"  - xml:id: {lesson.warmup.xml_id}")
            if lesson.warmup.title:
                print(f"  - title: {lesson.warmup.title}")
            
        for activity in lesson.activities:
            print(f"* activity {activity.activity_number}:")
            print(f"  - file: {activity.file_name}")
            print(f"  - xml:id: {activity.xml_id}")
            if activity.title:
                print(f"  - title: {activity.title}")
            
        if lesson.cooldown:
            print("* cooldown:")
            print(f"  - file: {lesson.cooldown.file_name}")
            print(f"  - xml:id: {lesson.cooldown.xml_id}")
            if lesson.cooldown.title:
                print(f"  - title: {lesson.cooldown.title}")

def print_tab_separated(lessons: List[Lesson]):
    """Print the lesson structure in tab separated format."""
    for lesson in lessons:
        # print(f"\nLección {lesson.lesson_number}:")
        
        parts = [str(lesson.lesson_number), lesson.xml_id]
        
        # Warm-up
        if lesson.warmup:
            parts.append(lesson.warmup.xml_id)
        else:
            parts.append('')  # empty for missing warmup

        # Activities
        activities = lesson.activities
        for i in range(3):  # Expecting 3 main activities (some may not exist, but loop needs to go over all of them to create the empty cols)
            if i < len(activities):
                parts.append(activities[i].xml_id)
            else:
                parts.append('')  # empty if not enough activities

        # Cooldown
        if lesson.cooldown:
            parts.append(lesson.cooldown.xml_id)
        else:
            parts.append('')  # empty for missing cooldown

        # Now join with tabs
        lesson_tab_info = '\t'.join(parts)
        print(lesson_tab_info)


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python list_unit_xmlids.py <unit-folder>")
        sys.exit(1)
        
    unit_folder = sys.argv[1]
    lessons = process_unit_folder(unit_folder)
    print("*************************************************************")
    print(" Tab separated lessons")
    print("*************************************************************")
    print_tab_separated(lessons)

    print("*************************************************************")
    print(" Details per lesson")
    print("*************************************************************")
    print_lesson_structure(lessons)

if __name__ == "__main__":
    main()
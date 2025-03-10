import csv
from pathlib import Path
from tools.course_csv_loaders.course_csv_loader_utils import get_csv_file_path
from langchain_core.tools import tool

csv_file = get_csv_file_path()
COURSE_MAPPING = {}

# Open the CSV file and read its contents
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        COURSE_MAPPING[row["Course"]] = row["Title"]

@tool
def course_to_title(course_number: str):
    """
    A LangChain tool that retrieves the course title or name for a given course number.

    This tool allows users to query the course catalog by providing a course number
    and receive the corresponding course title. It is useful for students, advisors,
    and administrators who need quick access to course details.

    Example Usage:
    - Input: "35150"
    - Output: "Advanced Investments"

    - Input: "33942"
    - Output: "Applied Macroeconomics: Micro Data for Macro Models"

    If the course number is not found, the tool returns a relevant message.

    Args:
        course_number (str): The course number to look up.

    Returns:
        str: The corresponding course title, or an error message if the course number is not found.
    """
    if course_number in COURSE_MAPPING:
        return COURSE_MAPPING[course_number]
    else:
        return f"Course number {course_number} not found."

# Example usage:
if __name__ == "__main__":



    # Example queries
    print(course_to_title("35150"))  # Output: "Advanced Investments"
    print(course_to_title("33942"))  # Output: "Applied Macroeconomics: Micro Data for Macro Models"
    print(course_to_title("99999"))  # Output: "Course number 99999 not found."

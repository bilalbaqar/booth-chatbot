from pathlib import Path

def get_csv_file_path():
    # Initialize file paths at module level
    current_file = Path(__file__)
    BASE_DIR = current_file.parents[3]
    csv_file = BASE_DIR / "data" / "all-course-list.csv"
    return csv_file





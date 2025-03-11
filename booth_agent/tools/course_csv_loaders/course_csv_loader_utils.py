from pathlib import Path

def get_csv_file_path() -> Path:
    """
    Get the path to the course list CSV file.
    
    Returns:
        Path: Path object pointing to the all-course-list.csv file
        
    Note:
        The file is expected to be in the data directory at the root of the project.
        The path is constructed relative to this utility file's location.
    """
    current_file = Path(__file__)
    base_dir = current_file.parents[3]  # Go up 3 levels to reach project root
    csv_file = base_dir / "data" / "all-course-list.csv"
    return csv_file





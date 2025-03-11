import pandas as pd
from langchain_core.tools import tool
from pathlib import Path




# Initialize file paths
current_file = Path(__file__)
BASE_DIR = current_file.parents[3]
FILE_PATH = BASE_DIR / "data" / "bidding-history.csv"

# Initialize bidding data at module level
try:
    bidding_data = pd.read_csv(FILE_PATH)
    print(f"Successfully loaded bidding data from {FILE_PATH}")
    print(f"Total records: {len(bidding_data)}")
except FileNotFoundError:
    print(f"Warning: Bidding history file not found at {FILE_PATH}")
    print("Please run the bidding_history_loader.py script first")
    bidding_data = None
except Exception as e:
    print(f"Error loading bidding data: {str(e)}")
    bidding_data = None


def bid_history_by_course_number(course_number: str):
    """
    Retrieve bid point history for a given Booth course.
    
    :param course_number: The course number (e.g., "30000-81")
    :return: Dictionary containing bid history details.
    """
    if bidding_data is None:
        return {
            "error": "Bidding data not initialized. Please ensure the bidding history CSV file exists and is properly formatted."
        }
    filtered_data = bidding_data[bidding_data["Course_Number"].astype(str) == course_number]

    if filtered_data.empty:
        return {
            "error": f"No bid history found for course {course_number}"
        }

    return filtered_data.to_dict(orient="records")



if __name__ == "__main__":
    print(bid_history_by_course_number("30000"))
    print(bid_history_by_course_number("40000"))

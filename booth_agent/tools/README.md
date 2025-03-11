# Tools Documentation

This directory contains various tools and utilities used by the Booth Course Assistant Chatbot. Each tool serves a specific purpose in processing and analyzing course-related data.

## Tool Structure

### Bidding Tools (`bidding_loader/`)

#### `bidding_tool.py`
- **Purpose**: Handles course bidding history analysis and queries
- **Key Functions**:
  - `bid_history_by_course_number()`: Retrieves bidding history for a specific course
  - `get_all_sections()`: Gets all available sections for a course
  - `analyze_bid_trends()`: Analyzes historical bidding patterns
- **Usage**: Used by the chatbot to provide bidding recommendations and historical price analysis

### Course Information Tools (`course_loader/`)

#### `course_tool.py`
- **Purpose**: Manages course information retrieval and processing
- **Key Functions**:
  - `get_course_info()`: Retrieves detailed course information
  - `search_courses()`: Searches for courses based on various criteria
  - `get_prerequisites()`: Retrieves course prerequisites
- **Usage**: Provides course-specific information to users

### Syllabus Tools (`syllabus_loader/`)

#### `syllabus_tool.py`
- **Purpose**: Handles syllabus document processing and information extraction
- **Key Functions**:
  - `get_syllabus()`: Retrieves syllabus for a specific course
  - `extract_syllabus_info()`: Extracts key information from syllabus PDFs
- **Usage**: Processes and provides syllabus-related information

### Data Processing Tools (`data_loader/`)

#### `bidding_history_loader.py`
- **Purpose**: Processes raw bidding history data
- **Key Functions**:
  - `process_bidding_data()`: Cleans and processes bidding history
  - `update_bidding_history()`: Updates the bidding history database
- **Usage**: Maintains and updates the bidding history dataset

## Integration

These tools are integrated into the main chatbot system through:
1. Direct function calls from the agent
2. API endpoints in the Flask server
3. LangChain tool configurations

## Testing

Each tool can be run directly with some predefined tests:

```bash
# First, go to the project root directory
cd booth-chatbot
python path\to\script.py
```
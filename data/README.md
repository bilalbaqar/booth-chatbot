# Data Files Documentation

This directory contains the data files used by the Booth Course Assistant Chatbot. Below is a description of each file and its purpose.

## File Structure

### `bidding-history.csv`
- **Purpose**: Contains historical bidding data for Booth courses
- **Format**: CSV (Comma Separated Values)
- **Columns**:
  - `Course_Original`: Original course identifier (e.g., "30000-81")
  - `Course_Number`: Base course number (e.g., "30000")
  - `Section`: Section identifier (e.g., "81")
  - `Title`: Course title
  - `Quarter`: Academic quarter (Autumn, Winter, Spring, Summer)
  - `Year`: Academic year
  - `Day and Time`: Course schedule
  - `Instructor`: Course instructor
  - `Phase 1 Price`: Clearing price in Phase 1 bidding
  - `Phase 2 Price`: Clearing price in Phase 2 bidding
  - `Phase 3 Price`: Clearing price in Phase 3 bidding
  - Additional enrollment and pricing details for different phases

### `course-info.csv`
- **Purpose**: Contains detailed information about Booth courses
- **Format**: CSV
- **Columns**:
  - Course number and section
  - Course title
  - Course description
  - Prerequisites
  - Credit hours
  - Professor information
  - Other course-specific details

### `syllabus\*_syllabus.pdf`
- **Purpose**: Contains syllabus of Booth courses
- **Format**: pdf

## Data Updates

- Bidding history data is updated quarterly after each bidding cycle
- Course information is updated each academic year
- Degree requirements are updated as per Booth School policy changes

## Data Usage

These files are used by various components of the chatbot:
1. Bidding analysis tools use `bidding-history.csv` for price predictions and trends
2. Course information queries utilize `course-info.csv` for detailed responses

## Data Privacy

- All data is anonymized and contains no personal student information
- Bidding data is aggregated by course and section
- Course information is publicly available through Booth's course catalog

## Contributing

When updating data files:
1. Maintain the existing file format and column structure
2. Update the corresponding timestamp or version information
3. Verify data integrity before committing changes
4. Document any structural changes in this README

## Note

Please ensure all data files are properly formatted and validated before use in the production environment. 
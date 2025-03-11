# Data Files Documentation

This directory contains the data files used by the Booth Course Assistant Chatbot. Below is a description of each file and its purpose.

## File Structure

### `bidding-history.csv`
- **Purpose**: Contains historical bidding data for Booth courses
- **Format**: CSV
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

### `all-course-list.csv`
- **Purpose**: Contains detailed information about Booth courses
- **Format**: CSV
- **Columns**:
  - `Quarter`: Academic quarter
  - `Title`: Course title
  - `Course`: Course number
  - `Section`: Section identifier
  - `Program`: Program type
  - `Faculty`: Course instructor
  - `Schedule`: Class timing
  - `Capacity`: Maximum enrollment
  - `Building`: Building name
  - `Location`: Room location

### `syllabus\*_syllabus.pdf`
- **Purpose**: Contains syllabus of Booth courses
- **Format**: PDF

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

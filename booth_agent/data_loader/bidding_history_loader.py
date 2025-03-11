import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Load bidding history from Excel file')
    parser.add_argument('input_file_path', help='Path to the Excel file containing bidding history')
    parser.add_argument('output_file_path', help='Path to the CSV file that will be created')
    return parser.parse_args()

def process_bidding_data(df):
    """Process the bidding data to split course numbers and sections."""
    # Split Course column into Course_Number and Section
    df[['Course_Number', 'Section']] = df['Course'].str.split('-', n=1, expand=True)
    
    # Fill NaN values in Section with empty string
    df['Section'] = df['Section'].fillna('')
    
    # Keep original Course column
    df = df.rename(columns={'Course': 'Course_Original'})
    
    # Reorder columns to put new columns after Course_Original
    cols = df.columns.tolist()
    cols.insert(cols.index('Course_Original') + 1, cols.pop(cols.index('Course_Number')))
    cols.insert(cols.index('Course_Number') + 1, cols.pop(cols.index('Section')))
    df = df[cols]
    
    return df

if __name__ == "__main__":
    args = parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path

    # Load the Excel file
    print(f"Loading Excel file from {input_file_path}...")
    xls = pd.ExcelFile(input_file_path)

    # Read all sheets and merge them
    df_list = [xls.parse(sheet) for sheet in xls.sheet_names]
    merged_df = pd.concat(df_list, ignore_index=True)

    # Process the data to split course numbers and sections
    print("Processing course numbers and sections...")
    processed_df = process_bidding_data(merged_df)

    # Save to a CSV file
    processed_df.to_csv(output_file_path, index=False)

    # Display summary of the merged data
    print("\nData Summary:")
    print(f"Total rows: {len(processed_df)}")
    print(f"Columns: {', '.join(processed_df.columns)}")
    print("\nSample of processed data:")
    print(processed_df[['Course_Original', 'Course_Number', 'Section']].head())
    print(f"\nProcessed data saved as {output_file_path}")


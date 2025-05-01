import pandas as pd
import numpy as np
import time
import os
import json
from datetime import datetime

PATH = '../../data/logs/'
OUTPUT_FILE = '../../data/logs/dataset.json'
CHECK_INTERVAL = 10  # seconds between checks for file changes

# Store last modification times
last_modified = {
    'ssl': 0,
    'conn': 0,
    'http': 0
}


def format_csv(input_file):
    """Parse Zeek log files and convert to DataFrame."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        separator = "\t"
        columns = []
        data_rows = []
        current_line = ""
        for line in lines:
            if line.startswith("#separator"):
                continue
            elif line.startswith("#fields"):
                columns = line.split(separator)[1:]
                data_rows.append(columns)
                continue
            elif line.startswith("#"):
                continue
            elif line.endswith("\\"):
                current_line += line[:-1]
            else:
                current_line += line
                data_rows.append(current_line.split(separator))
                current_line = ""

        df = pd.DataFrame(data_rows, columns=columns)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return pd.DataFrame()


def merge_logs():
    """Merge the log files and save to JSON."""
    print(f"[{datetime.now()}] Processing log files...")

    df_ssl = format_csv(PATH + 'ssl.log')
    df_conn = format_csv(PATH + 'conn.log')
    df_http = format_csv(PATH + 'http.log')
    df_x509 = format_csv(PATH + 'x509.log')

    # Skip if essential dataframes are empty
    if df_ssl.empty or df_conn.empty or df_http.empty:
        print(
            "One or more essential log files are empty or couldn't be read. Skipping merge.")
        return False

    # Note if x509 is empty but continue processing
    if df_x509.empty:
        print(
            "Warning: x509.log is empty or couldn't be read. Continuing without x509 data.")

    # Merge DataFrames
    merged_df = pd.merge(df_conn, df_ssl, on=["ts"], how="outer")
    merged_df = pd.merge(merged_df, df_http, on=["ts"], how="outer")

    # Only merge x509 if it has data
    if not df_x509.empty:
        merged_df = pd.merge(merged_df, df_x509, on=["ts"], how="outer")

    # Clean data
    merged_df = merged_df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Handle merged info
    merged_df = merged_df[1:-1]  # Skip header/footer rows

    # Handle duplicate columns from merges more thoroughly
    # First drop _y columns from the merge
    columns_to_drop = [col for col in merged_df.columns if col.endswith('_y')]
    merged_df = merged_df.drop(columns=columns_to_drop)

    # Rename _x columns
    merged_df = merged_df.rename(columns=lambda x: x.rstrip('_x'))

    # Check for any remaining duplicate columns and make them unique
    if merged_df.columns.duplicated().any():
        print(f"Warning: Found duplicate column names. Making them unique...")
        # Get duplicate columns
        duplicates = merged_df.columns[merged_df.columns.duplicated()].tolist()
        print(f"Duplicate columns: {duplicates}")

        # Create a mapping to make columns unique
        column_mapping = {}
        seen_columns = set()

        for i, col in enumerate(merged_df.columns):
            if col in seen_columns:
                new_col = f"{col}_{i}"
                column_mapping[col] = new_col
                print(f"Renaming duplicate column '{col}' to '{new_col}'")
            else:
                seen_columns.add(col)

        # Apply the mapping to rename duplicates
        merged_df = merged_df.rename(columns=column_mapping)

    # Filter columns based on the specified list
    filter_columns = [
        'ts', 'missed_bytes', 'version', 'cipher', 'curve', 'resumed',
        'last_alert', 'established', 'sni_matches_cert', 'username', 'password',
        'certificate.not_valid_before', 'certificate.not_valid_after',
        'certificate.sig_alg', 'certificate.key_length', 'certificate.key'
    ]

    # Print info about filtered columns and available columns
    print(f"Available columns in merged data: {
          sorted(merged_df.columns.tolist())}")

    # Keep only columns that exist in the DataFrame
    existing_columns = [
        col for col in filter_columns if col in merged_df.columns]

    # Print info about filtered columns
    print(f"Filtering to keep {len(existing_columns)} columns out of {
          len(merged_df.columns)} total columns")
    print(f"Columns being kept: {existing_columns}")
    missing_columns = [
        col for col in filter_columns if col not in merged_df.columns]
    if missing_columns:
        print(f"Note: The following requested columns were not found in the data: {
              missing_columns}")

    # Apply the filter
    filtered_df = merged_df[existing_columns]

    # Ensure all requested columns exist in the output, adding empty ones if needed
    for col in filter_columns:
        if col not in filtered_df.columns:
            print(f"Adding empty column: {col}")
            filtered_df[col] = ""

    # Convert to JSON Lines format (one JSON object per line)
    try:
        # Print column names to help debug
        print(f"Columns in final DataFrame: {filtered_df.columns.tolist()}")
        print(f"Any duplicate column names: {
              filtered_df.columns.duplicated().any()}")

        # Handle duplicate columns if present (shouldn't happen after filtering, but just in case)
        if filtered_df.columns.duplicated().any():
            print("WARNING: Handling duplicate columns...")
            # Get original column names before making them unique
            original_columns = filtered_df.columns.tolist()

            # Create unique column names temporarily
            unique_columns = []
            seen = set()
            for col in original_columns:
                if col in seen:
                    count = 1
                    while f"{col}_{count}" in seen:
                        count += 1
                    unique_columns.append(f"{col}_{count}")
                    seen.add(f"{col}_{count}")
                else:
                    unique_columns.append(col)
                    seen.add(col)

            # Assign unique column names
            filtered_df.columns = unique_columns

        # Replace NaN values with empty strings (instead of null)
        filtered_df = filtered_df.replace({np.nan: ""})

        # Convert to records with proper column names
        records = filtered_df.to_dict('records')

        # Write each record as a separate JSON object on its own line (JSONL format)
        with open(OUTPUT_FILE, 'w') as f:
            for record in records:
                f.write(json.dumps(record) + '\n')

        print(f"[{datetime.now()}] Successfully saved filtered data to {
              OUTPUT_FILE} in JSON Lines format")
        print(f"Number of records: {len(records)}")
        return True

        print(f"[{datetime.now()}] Successfully saved merged data to {OUTPUT_FILE}")

        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False


def files_modified():
    """Check if any input files have been modified."""
    file_paths = {
        'ssl': PATH + 'ssl.log',
        'conn': PATH + 'conn.log',
        'http': PATH + 'http.log',
        'x509': PATH + 'x509.log'
    }

    modified = False

    for key, filepath in file_paths.items():
        try:
            current_mtime = os.path.getmtime(filepath)
            if current_mtime > last_modified[key]:
                last_modified[key] = current_mtime
                modified = True
                print(f"[{datetime.now()}] Detected changes in {filepath}")
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")

    return modified


def main():
    """Main function to continuously monitor and process log files."""
    print(f"[{datetime.now()}] Starting continuous log merger...")
    print(f"Monitoring directory: {PATH}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")

    # Initialize last modified times
    global last_modified
    last_modified = {
        'ssl': 0,
        'conn': 0,
        'http': 0,
        'x509': 0
    }

    for key in last_modified:
        file_path = PATH + f'{key}.log'
        try:
            last_modified[key] = os.path.getmtime(file_path)
        except FileNotFoundError:
            print(f"Warning: {file_path} not found during initialization")

    # Initial merge
    merge_logs()

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            if files_modified():
                merge_logs()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Program terminated by user")


if __name__ == "__main__":
    main()

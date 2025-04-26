#!/usr/bin/env python3
"""
Continuous Zeek JSON Log Merger - Monitors and merges multiple Zeek JSON log files as they grow.
Handles common Zeek log files like http.log, conn.log, ssl.log, etc. in JSON format.
"""

import os
import sys
import json
import gzip
import time
import argparse
import hashlib
from collections import defaultdict
from datetime import datetime


class ContinuousZeekJsonLogMerger:
    def __init__(self, input_files, output_file, output_format="jsonl", interval=5):
        self.input_files = input_files
        self.output_file = output_file
        self.output_format = output_format
        self.interval = interval  # Polling interval in seconds
        self.source_field = "source_log"  # Field to indicate source log file
        
        # Tracking variables
        self.file_sizes = {}      # Track file sizes to detect changes
        self.processed_entries = set()  # Use hash of entries to avoid duplicates
        self.logs = []            # Collection of all log entries
    
    def get_file_size(self, file_path):
        """Get the size of a file in bytes."""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    def process_file(self, file_path, from_beginning=False):
        """
        Process a single JSON-formatted Zeek log file.
        
        Args:
            file_path: Path to the log file
            from_beginning: If True, process the entire file; otherwise, only new content
        """
        log_type = os.path.basename(file_path).split('.')[0]
        
        # Get current and previous file sizes
        current_size = self.get_file_size(file_path)
        previous_size = self.file_sizes.get(file_path, 0)
        
        # If file is new or we're forced to read from beginning
        if from_beginning or file_path not in self.file_sizes:
            previous_size = 0
        
        # If file hasn't grown, or has shrunk (rotated), no need to process
        if current_size <= previous_size and not from_beginning:
            return 0
        
        # Handle both plain text and gzipped files
        is_gzip = file_path.endswith('.gz')
        open_func = gzip.open if is_gzip else open
        open_mode = 'rt' if is_gzip else 'r'
        
        try:
            with open_func(file_path, open_mode) as f:
                # If we're not starting from the beginning, seek to the previous position
                if previous_size > 0:
                    f.seek(previous_size)
                
                # Process each line as a separate JSON object
                new_entries = 0
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):  # Skip empty lines and comments
                        continue
                    
                    try:
                        record = json.loads(line)
                        
                        # Generate a unique identifier for this record to avoid duplicates
                        # This should work for most Zeek logs that have uid or similar identifiers
                        id_fields = ['uid', 'id', 'ts', 'id.orig_h', 'id.resp_h']
                        id_parts = []
                        
                        for field in id_fields:
                            if field in record:
                                id_parts.append(str(record[field]))
                        
                        if not id_parts:
                            # If no unique fields found, use the whole record
                            record_id = hashlib.md5(line.encode()).hexdigest()
                        else:
                            record_id = hashlib.md5('|'.join(id_parts).encode()).hexdigest()
                        
                        # Only add if we haven't seen this record before
                        if record_id not in self.processed_entries:
                            record[self.source_field] = log_type  # Add source log info
                            self.logs.append(record)
                            self.processed_entries.add(record_id)
                            new_entries += 1
                    
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON in {file_path}: {e}")
                        continue
                
                # Update file size for next read
                self.file_sizes[file_path] = current_size
                
                if new_entries > 0:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Added {new_entries} new entries from {file_path}")
                
                return new_entries
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return 0
    
    def sort_logs(self):
        """Sort all log entries by timestamp."""
        timestamp_fields = ["ts", "timestamp"]
        
        if self.logs:
            # Check which timestamp field exists
            sample_records = self.logs[:min(10, len(self.logs))]
            for field in timestamp_fields:
                if any(field in record for record in sample_records):
                    self.logs.sort(key=lambda x: float(x.get(field, 0)))
                    return True
        
        return False

    def write_merged_log(self):
        """Write the merged log to the output file."""
        try:
            with open(self.output_file, 'w') as out:
                if self.output_format == "jsonl":
                    # Write as JSON Lines (one JSON object per line)
                    for record in self.logs:
                        out.write(json.dumps(record) + "\n")
                elif self.output_format == "json_array":
                    # Write as a single JSON array
                    json.dump(self.logs, out)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Updated merged log: {self.output_file} ({len(self.logs)} total entries)")
            return True
        
        except Exception as e:
            print(f"Error writing to output file: {e}")
            return False

    def scan_for_changes(self):
        """Scan input files for changes and process any new data."""
        changes_detected = False
        
        for file_path in self.input_files:
            if not os.path.exists(file_path):
                continue
            
            current_size = self.get_file_size(file_path)
            if current_size > self.file_sizes.get(file_path, 0):
                # File has grown, process it
                if self.process_file(file_path) > 0:
                    changes_detected = True
            elif current_size < self.file_sizes.get(file_path, 0):
                # File has shrunk (potentially rotated), process from beginning
                print(f"File size decreased for {file_path}, reprocessing from beginning...")
                if self.process_file(file_path, from_beginning=True) > 0:
                    changes_detected = True
        
        return changes_detected

    def run(self):
        """Main monitoring loop."""
        print(f"Starting continuous monitoring of {len(self.input_files)} Zeek log files...")
        print(f"Merged output will be written to: {self.output_file}")
        print(f"Monitoring interval: {self.interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            # Initial processing of all files
            for file_path in self.input_files:
                if os.path.exists(file_path):
                    print(f"Initial processing of {file_path}...")
                    self.process_file(file_path, from_beginning=True)
                else:
                    print(f"Warning: File not found - {file_path}")
            
            # Initial sort and write
            if self.logs:
                self.sort_logs()
                self.write_merged_log()
            
            # Continuous monitoring loop
            while True:
                time.sleep(self.interval)
                
                if self.scan_for_changes():
                    # If changes were detected and processed
                    self.sort_logs()
                    self.write_merged_log()
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        
        finally:
            # Write final output
            if self.logs:
                print("Writing final merged log...")
                self.sort_logs()
                self.write_merged_log()
            
            # Show summary
            log_counts = defaultdict(int)
            for record in self.logs:
                log_counts[record.get(self.source_field, "unknown")] += 1
            
            print("\nFinal summary of merged logs:")
            for log_type, count in sorted(log_counts.items()):
                print(f"  {log_type}: {count} entries")


def main():
    parser = argparse.ArgumentParser(description="Continuously merge multiple JSON-formatted Zeek log files as they grow.")
    parser.add_argument("input_files", nargs="+", help="Input JSON Zeek log files (http.log, conn.log, etc.)")
    parser.add_argument("-o", "--output", default="merged.log", help="Output file name (default: merged.log)")
    parser.add_argument("-f", "--format", choices=["jsonl", "json_array"], default="jsonl",
                        help="Output format: jsonl (JSON Lines, default) or json_array (single JSON array)")
    parser.add_argument("-i", "--interval", type=int, default=5,
                        help="Monitoring interval in seconds (default: 5)")
    
    args = parser.parse_args()
    
    merger = ContinuousZeekJsonLogMerger(
        args.input_files,
        args.output,
        args.format,
        args.interval
    )
    merger.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Add MMS IDs to Seeklight records by matching titles with Alma records
"""

import csv
from difflib import SequenceMatcher
from pathlib import Path

def read_csv_with_comments(filepath):
    """Read CSV file, skipping comment lines starting with #"""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line for line in f if not line.strip().startswith('#')]
    
    reader = csv.DictReader(lines)
    for row in reader:
        rows.append(row)
    
    return rows

def get_header_comments(filepath):
    """Extract comment lines from the beginning of the file"""
    comments = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('#'):
                comments.append(line.rstrip())
            else:
                break
    return comments

def similarity_ratio(a, b):
    """Calculate similarity ratio between two strings"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(seeklight_title, alma_records, min_threshold=0.5):
    """Find the best matching Alma record for a Seeklight title"""
    best_match = None
    best_ratio = min_threshold
    
    for alma_rec in alma_records:
        alma_title = alma_rec.get('dc:title', '')
        ratio = similarity_ratio(seeklight_title, alma_title)
        
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = alma_rec
    
    return best_match, best_ratio

def add_mms_ids(seeklight_records, alma_records):
    """Add MMS IDs to Seeklight records based on title matching"""
    matches = []
    
    for seek_rec in seeklight_records:
        seek_title = seek_rec.get('dc:title', '')
        best_match, ratio = find_best_match(seek_title, alma_records)
        
        if best_match:
            mms_id = best_match.get('mms_id', '')
            seek_rec['mms_id'] = mms_id
            matches.append({
                'seeklight_title': seek_title,
                'alma_title': best_match.get('dc:title', ''),
                'mms_id': mms_id,
                'similarity': ratio
            })
            print(f"  Matched ({int(ratio*100)}%): {seek_title[:60]}... → {mms_id}")
        else:
            print(f"  No match: {seek_title[:60]}...")
    
    return seeklight_records, matches

def write_csv_with_comments(records, comments, fieldnames, output_file):
    """Write CSV with header comments"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Write comments
        for comment in comments:
            f.write(comment + '\n')
        
        # Write CSV data
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def main():
    # File paths
    alma_file = Path(__file__).parent / 'alma_export_20260506_131357.csv'
    seeklight_input = Path(__file__).parent / 'seeklight_export_to_DCAP01-FROM-SCRIPT.csv'
    seeklight_output = Path(__file__).parent / 'seeklight_export_to_DCAP01-FROM-SCRIPT.csv'
    
    print("Reading Alma export...")
    alma_records = read_csv_with_comments(alma_file)
    print(f"  Found {len(alma_records)} Alma records")
    
    print("\nReading Seeklight export...")
    seeklight_records = read_csv_with_comments(seeklight_input)
    print(f"  Found {len(seeklight_records)} Seeklight records")
    
    print("\nMatching titles and adding MMS IDs...")
    updated_records, matches = add_mms_ids(seeklight_records, alma_records)
    
    # Get header comments and field names
    comments = get_header_comments(seeklight_input)
    fieldnames = list(updated_records[0].keys())
    
    print(f"\nWriting updated file to: {seeklight_output}")
    write_csv_with_comments(updated_records, comments, fieldnames, seeklight_output)
    
    print(f"\n✓ Complete! Added MMS IDs to {len(matches)} of {len(seeklight_records)} records")
    print("\nMatch summary:")
    for match in matches:
        print(f"  {match['mms_id']}: {int(match['similarity']*100)}% match")

if __name__ == '__main__':
    main()

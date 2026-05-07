#!/usr/bin/env python3
"""
Manually add the two missing MMS IDs that couldn't be matched by title similarity
"""

import csv
from pathlib import Path

def read_csv_with_comments(filepath):
    """Read CSV file, skipping comment lines"""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line for line in f if not line.strip().startswith('#')]
    
    reader = csv.DictReader(lines)
    for row in reader:
        rows.append(row)
    
    return rows

def get_header_comments(filepath):
    """Extract comment lines"""
    comments = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('#'):
                comments.append(line.rstrip())
            else:
                break
    return comments

def write_csv_with_comments(records, comments, fieldnames, output_file):
    """Write CSV with header comments"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + '\n')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

# Manual mapping based on content knowledge
manual_mappings = {
    '42356816': '991011591313304641',  # Dorothy Lannom Interview
    '42356812': '991011582745504641',  # Lucille Ley letter
}

seeklight_file = Path(__file__).parent / 'seeklight_export_to_DCAP01-FROM-SCRIPT.csv'

print("Reading Seeklight export...")
records = read_csv_with_comments(seeklight_file)
comments = get_header_comments(seeklight_file)
fieldnames = list(records[0].keys())

print("Adding manual MMS ID mappings...")
for record in records:
    ssid = record.get('originating_system_id', '')
    if ssid in manual_mappings and not record.get('mms_id'):
        record['mms_id'] = manual_mappings[ssid]
        title = record.get('dc:title', '')[:60]
        print(f"  {ssid} → {manual_mappings[ssid]}: {title}...")

print(f"\nWriting updated file...")
write_csv_with_comments(records, comments, fieldnames, seeklight_file)

# Verify
records_with_mms = sum(1 for r in records if r.get('mms_id'))
print(f"\n✓ Complete! {records_with_mms} of {len(records)} records now have MMS IDs")

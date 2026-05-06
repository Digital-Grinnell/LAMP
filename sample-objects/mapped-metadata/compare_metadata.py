#!/usr/bin/env python3
"""
Compare two DCAP01 CSV metadata files and generate a Markdown comparison table.
Uses MMS ID as the record key for matching.
"""

import csv
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

def index_by_mms_id(records):
    """Create a dictionary indexed by mms_id"""
    indexed = {}
    no_mms = []
    
    for record in records:
        mms_id = record.get('mms_id', '').strip()
        if mms_id:
            indexed[mms_id] = record
        else:
            no_mms.append(record)
    
    return indexed, no_mms

def match_records(alma_records, seeklight_records):
    """Match records between the two sources based on MMS ID"""
    alma_indexed, alma_no_mms = index_by_mms_id(alma_records)
    seek_indexed, seek_no_mms = index_by_mms_id(seeklight_records)
    
    # Find all MMS IDs
    all_mms_ids = set(alma_indexed.keys()) | set(seek_indexed.keys())
    
    # Create matched pairs
    matched_pairs = []
    for mms_id in sorted(all_mms_ids):
        alma_rec = alma_indexed.get(mms_id)
        seek_rec = seek_indexed.get(mms_id)
        matched_pairs.append((mms_id, alma_rec, seek_rec))
    
    return matched_pairs, alma_no_mms, seek_no_mms

def get_status_and_notes(alma_val, seek_val, field_name):
    """Determine status and notes for a field comparison"""
    alma_empty = not alma_val or alma_val.strip() == ''
    seek_empty = not seek_val or seek_val.strip() == ''
    
    if alma_empty and seek_empty:
        return "Both empty", ""
    elif alma_empty and not seek_empty:
        return "Added in Seeklight AI", ""
    elif not alma_empty and seek_empty:
        return "Missing in Seeklight AI", ""
    elif alma_val == seek_val:
        return "Match", ""
    else:
        # Analyze differences
        if alma_val.lower() == seek_val.lower():
            return "Different", "Case difference"
        elif alma_val.replace(' ', '') == seek_val.replace(' ', ''):
            return "Different", "Spacing difference"
        elif alma_val in seek_val or seek_val in alma_val:
            return "Different", "One contains the other"
        else:
            return "Different", "Content differs"

def escape_markdown(text):
    """Escape markdown special characters and truncate long text"""
    if not text:
        return ""
    
    text = str(text).replace('|', '\\|').replace('\n', ' ')
    
    # Truncate very long values
    if len(text) > 100:
        text = text[:97] + "..."
    
    return text

def generate_comparison_markdown(matched_pairs, alma_no_mms, seek_no_mms, output_file):
    """Generate Markdown comparison table"""
    
    # Get all field names from both sources
    all_fields = set()
    for _, alma_rec, seek_rec in matched_pairs:
        if alma_rec:
            all_fields.update(alma_rec.keys())
        if seek_rec:
            all_fields.update(seek_rec.keys())
    
    # Sort fields, putting key fields first
    priority_fields = ['mms_id', 'originating_system_id', 'dc:title', 'dc:identifier', 
                      'dc:creator', 'dc:date', 'dcterms:created', 'dc:subject']
    sorted_fields = [f for f in priority_fields if f in all_fields]
    sorted_fields.extend(sorted(f for f in all_fields if f not in priority_fields))
    
    # Generate markdown
    lines = []
    lines.append("# Metadata Comparison: Alma vs Seeklight Export\n")
    lines.append(f"**Date Generated:** May 6, 2026\n")
    lines.append("**Source: Alma:** alma_export_20260506_131357.csv")
    lines.append("**Source: Seeklight AI:** seeklight_export_to_DCAP01.csv\n")
    lines.append("---\n")
    
    # Summary section
    lines.append("## Summary\n")
    lines.append(f"- **Matched records (by MMS ID):** {len(matched_pairs)}")
    lines.append(f"- **Records without MMS ID in Alma:** {len(alma_no_mms)}")
    lines.append(f"- **Records without MMS ID in Seeklight AI:** {len(seek_no_mms)}\n")
    lines.append("---\n")
    
    # Process matched pairs
    for mms_id, alma_rec, seek_rec in matched_pairs:
        lines.append(f"\n## Record: {mms_id}\n")
        
        # Get titles
        title_alma = alma_rec.get('dc:title', '') if alma_rec else ''
        title_seek = seek_rec.get('dc:title', '') if seek_rec else ''
        
        if alma_rec and seek_rec:
            lines.append(f"**Title (Alma):** {title_alma}")
            lines.append(f"**Title (Seeklight AI):** {title_seek}\n")
        elif alma_rec:
            lines.append(f"**Status:** Only in Alma")
            lines.append(f"**Title:** {title_alma}\n")
        else:
            lines.append(f"**Status:** Only in Seeklight AI")
            lines.append(f"**Title:** {title_seek}\n")
        
        # Create comparison table
        lines.append("| Field | Source: Alma | Source: Seeklight AI | Status | Notes |")
        lines.append("|-------|--------------|----------------------|--------|-------|")
        
        # Track differences
        diff_count = 0
        match_count = 0
        
        for field in sorted_fields:
            alma_val = alma_rec.get(field, '') if alma_rec else ''
            seek_val = seek_rec.get(field, '') if seek_rec else ''
            
            # Skip if both empty
            if not alma_val and not seek_val:
                continue
            
            status, notes = get_status_and_notes(alma_val, seek_val, field)
            
            if status == "Match":
                match_count += 1
            elif status != "Both empty":
                diff_count += 1
            
            alma_display = escape_markdown(alma_val)
            seek_display = escape_markdown(seek_val)
            
            lines.append(f"| {field} | {alma_display} | {seek_display} | {status} | {notes} |")
        
        lines.append(f"\n**Summary:** {match_count} matches, {diff_count} differences\n")
        lines.append("---\n")
    
    # Report records without MMS ID
    if seek_no_mms:
        lines.append("\n## Records Without MMS ID (Seeklight AI only)\n")
        lines.append("*These records cannot be matched to Alma records and are listed for reference only.*\n")
        
        for idx, rec in enumerate(seek_no_mms, 1):
            orig_id = rec.get('originating_system_id', 'Unknown')
            title = rec.get('dc:title', 'Untitled')
            lines.append(f"\n### {idx}. {title}")
            lines.append(f"**Originating System ID:** {orig_id}\n")
            
            # List key metadata
            key_fields = ['dc:creator', 'dc:date', 'dcterms:created', 'dc:type', 'dc:subject']
            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            for field in key_fields:
                val = rec.get(field, '')
                if val:
                    lines.append(f"| {field} | {escape_markdown(val)} |")
            lines.append("")
    
    if alma_no_mms:
        lines.append("\n## Records Without MMS ID (Alma only)\n")
        lines.append("*These records cannot be matched to Seeklight AI records and are listed for reference only.*\n")
        
        for idx, rec in enumerate(alma_no_mms, 1):
            orig_id = rec.get('originating_system_id', 'Unknown')
            title = rec.get('dc:title', 'Untitled')
            lines.append(f"\n### {idx}. {title}")
            lines.append(f"**Originating System ID:** {orig_id}\n")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Comparison written to: {output_file}")
    return len(matched_pairs)

def main():
    # File paths
    alma_file = Path(__file__).parent / 'alma_export_20260506_131357.csv'
    seeklight_file = Path(__file__).parent / 'seeklight_export_to_DCAP01.csv'
    output_file = Path(__file__).parent / 'metadata_comparison.md'
    
    print("Reading Alma export...")
    alma_records = read_csv_with_comments(alma_file)
    print(f"Found {len(alma_records)} Alma records")
    
    print("Reading Seeklight export...")
    seeklight_records = read_csv_with_comments(seeklight_file)
    print(f"Found {len(seeklight_records)} Seeklight records")
    
    print("\nMatching records by MMS ID...")
    matched_pairs, alma_no_mms, seek_no_mms = match_records(alma_records, seeklight_records)
    print(f"Matched {len(matched_pairs)} record pairs by MMS ID")
    print(f"Found {len(alma_no_mms)} Alma records without MMS ID")
    print(f"Found {len(seek_no_mms)} Seeklight records without MMS ID")
    
    print("\nGenerating comparison markdown...")
    count = generate_comparison_markdown(matched_pairs, alma_no_mms, seek_no_mms, output_file)
    
    print(f"\n✓ Comparison complete! Analyzed {count} matched records.")
    print(f"  Output: {output_file}")

if __name__ == '__main__':
    main()

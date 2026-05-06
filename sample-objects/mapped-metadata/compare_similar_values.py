#!/usr/bin/env python3
"""
Compare metadata values across different fields to identify similar content
that may be stored in different columns between Alma and Seeklight.
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
        if alma_rec and seek_rec:  # Only include records present in both
            matched_pairs.append((mms_id, alma_rec, seek_rec))
    
    return matched_pairs

def similarity_ratio(a, b):
    """Calculate similarity ratio between two strings"""
    if not a or not b:
        return 0.0
    
    # Normalize strings
    a_norm = str(a).strip().lower()
    b_norm = str(b).strip().lower()
    
    if not a_norm or not b_norm:
        return 0.0
    
    # Calculate similarity
    ratio = SequenceMatcher(None, a_norm, b_norm).ratio()
    return ratio

def find_similar_values(alma_rec, seek_rec, min_threshold=0.0, max_threshold=1.0):
    """Find similar values across ALL fields between two records within a threshold range"""
    similar_values = []
    seen_pairs = set()
    
    # Get all non-empty field values from both records
    alma_fields = {k: v for k, v in alma_rec.items() if v and v.strip()}
    seek_fields = {k: v for k, v in seek_rec.items() if v and v.strip()}
    
    # Only skip truly empty structural fields
    skip_fields = {'group_id', 'collection_id'}
    
    # Compare each Alma field value against each Seeklight field value
    for alma_field, alma_value in alma_fields.items():
        if alma_field in skip_fields:
            continue
        
        alma_str = str(alma_value).strip()
        
        # Skip very short values (less than 10 chars) to avoid noise
        if len(alma_str) < 10:
            continue
        
        for seek_field, seek_value in seek_fields.items():
            if seek_field in skip_fields:
                continue
            
            seek_str = str(seek_value).strip()
            
            if len(seek_str) < 10:
                continue
            
            # Skip if already compared this pair
            pair_key = (alma_field, seek_field)
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            
            # Calculate similarity
            ratio = similarity_ratio(alma_value, seek_value)
            
            # Only proceed if within threshold range
            if ratio < min_threshold or ratio >= max_threshold:
                continue
            
            # Determine match type
            is_same_field = (alma_field == seek_field)
            
            # Check for substring relationship
            alma_lower = alma_str.lower()
            seek_lower = seek_str.lower()
            
            is_substring = False
            if len(alma_lower) > 15 and alma_lower in seek_lower:
                is_substring = True
            elif len(seek_lower) > 15 and seek_lower in alma_lower:
                is_substring = True
            
            similar_values.append({
                'alma_field': alma_field,
                'alma_value': alma_value,
                'seek_field': seek_field,
                'seek_value': seek_value,
                'similarity': ratio,
                'is_substring': is_substring,
                'is_same_field': is_same_field
            })
    
    # Sort by: same_field first (obvious), then by similarity (highest first)
    similar_values.sort(key=lambda x: (not x['is_same_field'], -x['similarity']))
    
    return similar_values

def escape_markdown(text):
    """Escape markdown special characters and truncate long text"""
    if not text:
        return ""
    
    text = str(text).replace('|', '\\|').replace('\n', ' ')
    
    # Truncate very long values
    if len(text) > 150:
        text = text[:147] + "..."
    
    return text

def generate_similar_values_markdown(matched_pairs, output_file, min_threshold=0.0, max_threshold=1.0):
    """Generate Markdown report of similar values across different fields"""
    
    lines = []
    lines.append("# Similar Metadata Values Across Different Fields\n")
    lines.append(f"**Date Generated:** May 6, 2026")
    lines.append(f"**Similarity Range:** {int(min_threshold * 100)}%-{int(max_threshold * 100)}%\n")
    lines.append("**Source: Alma:** alma_export_20260506_131357.csv")
    lines.append("**Source: Seeklight AI:** seeklight_export_to_DCAP01.csv\n")
    lines.append("This report identifies similar metadata values that appear across ALL fields ")
    lines.append("between the Alma and Seeklight AI sources. This includes both:\n")
    lines.append("- **Same Field** matches - Values in identically named fields (obvious matches)")
    lines.append("- **Cross Field** matches - Values appearing in differently named fields (potential mapping issues)\n")
    lines.append("This can help identify:")
    lines.append("- Exact matches and differences in corresponding fields")
    lines.append("- Content that has been moved to different fields")
    lines.append("- Values that have been reformatted or rephrased")
    lines.append("- Potential field mapping issues")
    lines.append("- Duplicated information across different fields\n")
    lines.append("---\n")
    
    # Summary
    total_similarities = 0
    same_field_matches = 0
    cross_field_matches = 0
    records_with_similarities = 0
    
    for mms_id, alma_rec, seek_rec in matched_pairs:
        similar_values = find_similar_values(alma_rec, seek_rec, min_threshold, max_threshold)
        if similar_values:
            records_with_similarities += 1
            total_similarities += len(similar_values)
            for item in similar_values:
                if item.get('is_same_field', False):
                    same_field_matches += 1
                else:
                    cross_field_matches += 1
    
    lines.append("## Summary\n")
    lines.append(f"- **Records analyzed:** {len(matched_pairs)}")
    lines.append(f"- **Records with similar values:** {records_with_similarities}")
    lines.append(f"- **Total similar value pairs found:** {total_similarities}")
    lines.append(f"  - Same field matches: {same_field_matches}")
    lines.append(f"  - Cross field matches: {cross_field_matches}\n")
    lines.append("---\n")
    
    # Process each matched pair
    for mms_id, alma_rec, seek_rec in matched_pairs:
        title = alma_rec.get('dc:title', 'Untitled')
        similar_values = find_similar_values(alma_rec, seek_rec, min_threshold, max_threshold)
        
        if not similar_values:
            continue
        
        lines.append(f"\n## Record: {mms_id}\n")
        lines.append(f"**Title:** {title}")
        lines.append(f"**Similar value pairs found:** {len(similar_values)}\n")
        
        lines.append("| Alma Field | Alma Value | Seeklight AI Field | Seeklight AI Value | Similarity | Match Category |")
        lines.append("|------------|------------|-------------------|-------------------|------------|----------------|")
        
        for item in similar_values:
            alma_field = item['alma_field']
            alma_value = escape_markdown(item['alma_value'])
            seek_field = item['seek_field']
            seek_value = escape_markdown(item['seek_value'])
            similarity = f"{int(item['similarity'] * 100)}%"
            
            # Determine match category
            if item.get('is_same_field', False):
                category = "Same Field"
            elif item.get('is_substring', False):
                category = "Cross Field (Substring)"
            else:
                category = "Cross Field"
            
            lines.append(f"| {alma_field} | {alma_value} | {seek_field} | {seek_value} | {similarity} | {category} |")
        
        lines.append("")
        lines.append("---\n")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Similar values report written to: {output_file}")
    print(f"Found {total_similarities} similar value pairs across {records_with_similarities} records")

def main():
    # File paths
    alma_file = Path(__file__).parent / 'alma_export_20260506_131357.csv'
    seeklight_file = Path(__file__).parent / 'seeklight_export_to_DCAP01.csv'
    
    print("Reading Alma export...")
    alma_records = read_csv_with_comments(alma_file)
    print(f"Found {len(alma_records)} Alma records")
    
    print("Reading Seeklight export...")
    seeklight_records = read_csv_with_comments(seeklight_file)
    print(f"Found {len(seeklight_records)} Seeklight records")
    
    print("\nMatching records by MMS ID...")
    matched_pairs = match_records(alma_records, seeklight_records)
    print(f"Matched {len(matched_pairs)} record pairs by MMS ID")
    
    # Generate reports for each threshold band
    threshold_bands = [
        (0.90, 1.01, '90-100'),  # 90-100%
        (0.80, 0.90, '80-89'),   # 80-89%
        (0.70, 0.80, '70-79'),   # 70-79%
        (0.60, 0.70, '60-69'),   # 60-69%
        (0.50, 0.60, '50-59'),   # 50-59%
    ]
    
    print("\nGenerating similarity reports by threshold bands...")
    for min_thresh, max_thresh, label in threshold_bands:
        output_file = Path(__file__).parent / f'metadata_similar_values_{label}.md'
        print(f"\n  Analyzing {label}% similarity range...")
        generate_similar_values_markdown(matched_pairs, output_file, min_thresh, max_thresh)
    
    print(f"\n✓ Analysis complete! Generated 5 threshold band reports.")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Map Seeklight metadata from New_LAMP_628302.csv to DCAP01 format
"""

import csv
from pathlib import Path

def read_seeklight_csv(file_path):
    """Read the Seeklight CSV file"""
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def get_field_value(record, field_base_name):
    """
    Get field value by base name, ignoring bracketed numbers.
    
    Seeklight fields have bracketed numbers (e.g., 'Title[3076089]') that
    are specific to JSTOR Forum's system and can change between exports.
    This function finds fields by their base name regardless of the number.
    
    Args:
        record: Dictionary containing the CSV row data
        field_base_name: Base name of field (e.g., 'Title', 'Creator')
    
    Returns:
        Field value or empty string if not found
    """
    # First try exact match (for fields without brackets like SSID)
    if field_base_name in record:
        return record[field_base_name]
    
    # Then look for fields starting with the base name followed by '['
    for key in record.keys():
        if key.startswith(f"{field_base_name}["):
            return record[key]
    
    return ''

def combine_fields(*fields):
    """Combine multiple field values with pipe separator"""
    values = [str(f).strip() for f in fields if f and str(f).strip()]
    return ' | '.join(values) if values else ''

def map_to_dcap01(seeklight_record):
    """Map a single Seeklight record to DCAP01 format"""
    
    # Build combined medium/format/material description
    medium_parts = []
    medium = get_field_value(seeklight_record, 'Medium')
    technique = get_field_value(seeklight_record, 'Technique')
    material = get_field_value(seeklight_record, 'Material')
    
    if medium:
        medium_parts.append(medium)
    if technique:
        medium_parts.append(technique)
    if material:
        medium_parts.append(material)
    
    # Extract style/culture/period/location from Coverage field
    coverage = get_field_value(seeklight_record, 'Coverage')
    
    # Get the date field
    date = get_field_value(seeklight_record, 'Date')
    
    # Get description
    description = get_field_value(seeklight_record, 'Description')
    
    # Combine Subject and Keywords
    subject_combined = combine_fields(
        get_field_value(seeklight_record, 'Subject'),
        get_field_value(seeklight_record, 'Keywords')
    )
    
    # Get SSID (no brackets in this field name)
    ssid = get_field_value(seeklight_record, 'SSID')
    
    dcap01_record = {
        'group_id': '',
        'collection_id': '',
        'mms_id': '',  # Will need to be added manually if known
        'originating_system_id': ssid,
        'compoundrelationship': '',
        'dc:title': get_field_value(seeklight_record, 'Title'),
        'dcterms:alternative': '',
        'oldalttitle': '',
        'dc:identifier': ssid,
        'dcterms:identifier.dcterms:URI': get_field_value(seeklight_record, 'Media URL'),
        'dcterms:tableOfContents': '',
        'dc:creator': get_field_value(seeklight_record, 'Creator'),
        'dc:contributor': get_field_value(seeklight_record, 'Named Entities'),
        'dc:subject': subject_combined,
        'dcterms:subject.dcterms:LCSH': '',
        'dc:description': description,
        'dcterms:provenance': '',
        'dcterms:bibliographicCitation': '',
        'dcterms:abstract': description,
        'dcterms:publisher': get_field_value(seeklight_record, 'Publisher'),
        'dc:date': date,
        'dcterms:created': date,
        'dcterms:issued': date,
        'dcterms:dateSubmitted': '',
        'dcterms:dateAccepted': '',
        'dc:type': get_field_value(seeklight_record, 'Type'),
        'dc:format': ', '.join(medium_parts) if medium_parts else '',
        'dcterms:extent': get_field_value(seeklight_record, 'Measurements'),
        'dcterms:medium': combine_fields(medium, technique, material),
        'dcterms:format.dcterms:IMT': '',
        'dcterms:type.dcterms:DCMIType': get_field_value(seeklight_record, 'Resource Type'),
        'dc:language': get_field_value(seeklight_record, 'Language'),
        'dc:relation': '',
        'dcterms:isPartOf': '',
        'dc:coverage': coverage,
        'dcterms:spatial': get_field_value(seeklight_record, 'Location'),
        'dcterms:spatial.dcterms:Point': get_field_value(seeklight_record, 'Location'),
        'dcterms:temporal': get_field_value(seeklight_record, 'Period'),
        'dc:rights': '',
        'dc:source': '',
        'bib custom field': '',
        'rep_label': '',
        'rep_public_note': '',
        'rep_access_rights': '',
        'rep_usage_type': '',
        'rep_library': '',
        'rep_note': '',
        'rep_custom field': '',
        'file_name_1': '',
        'file_label_1': '',
        'file_name_2': '',
        'file_label_2': '',
        'googlesheetsource': '',
        'dginfo': 'Generated from Seeklight export New_LAMP_628302.csv'
    }
    
    return dcap01_record

def write_dcap01_csv(records, output_file):
    """Write records to DCAP01 CSV format with header comments"""
    
    # Define the field order
    fieldnames = [
        'group_id', 'collection_id', 'mms_id', 'originating_system_id', 'compoundrelationship',
        'dc:title', 'dcterms:alternative', 'oldalttitle', 'dc:identifier', 'dcterms:identifier.dcterms:URI',
        'dcterms:tableOfContents', 'dc:creator', 'dc:contributor', 'dc:subject', 'dcterms:subject.dcterms:LCSH',
        'dc:description', 'dcterms:provenance', 'dcterms:bibliographicCitation', 'dcterms:abstract',
        'dcterms:publisher', 'dc:date', 'dcterms:created', 'dcterms:issued', 'dcterms:dateSubmitted',
        'dcterms:dateAccepted', 'dc:type', 'dc:format', 'dcterms:extent', 'dcterms:medium',
        'dcterms:format.dcterms:IMT', 'dcterms:type.dcterms:DCMIType', 'dc:language', 'dc:relation',
        'dcterms:isPartOf', 'dc:coverage', 'dcterms:spatial', 'dcterms:spatial.dcterms:Point',
        'dcterms:temporal', 'dc:rights', 'dc:source', 'bib custom field', 'rep_label',
        'rep_public_note', 'rep_access_rights', 'rep_usage_type', 'rep_library', 'rep_note',
        'rep_custom field', 'file_name_1', 'file_label_1', 'file_name_2', 'file_label_2',
        'googlesheetsource', 'dginfo'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Write header comments
        f.write('# This is a CSV mapping of Seeklight AI generated metadata mapped to the Dublin Core Application Profile (DCAP01).\n')
        f.write('# Source: New_LAMP_628302.csv from seeklight-metadata-Rev-1 folder\n')
        f.write('# Each row represents a unique digital object with its associated metadata fields.\n')
        f.write('# The metadata is structured to facilitate discovery, access, and management of digital resources.\n')
        f.write('#\n')
        
        # Write CSV data
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✓ Wrote {len(records)} records to {output_file}")

def main():
    # File paths
    input_file = Path(__file__).parent.parent / 'seeklight-metadata-Rev-1' / 'New_LAMP_628302.csv'
    output_file = Path(__file__).parent / 'seeklight_export_to_DCAP01-FROM-SCRIPT.csv'
    
    print(f"Reading Seeklight metadata from: {input_file}")
    seeklight_records = read_seeklight_csv(input_file)
    print(f"  Found {len(seeklight_records)} records")
    
    print("\nMapping to DCAP01 format...")
    dcap01_records = []
    for record in seeklight_records:
        dcap01_record = map_to_dcap01(record)
        dcap01_records.append(dcap01_record)
    
    print(f"\nWriting to: {output_file}")
    write_dcap01_csv(dcap01_records, output_file)
    
    print("\n✓ Mapping complete!")
    print(f"  Input: {len(seeklight_records)} Seeklight records")
    print(f"  Output: {len(dcap01_records)} DCAP01 records")

if __name__ == '__main__':
    main()

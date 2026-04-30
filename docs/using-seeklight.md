# Using JSTOR Seeklight for Metadata Generation

This guide explains how to access and use JSTOR Seeklight to generate AI-assisted metadata for digital objects.

## What is JSTOR Seeklight?

JSTOR Seeklight is an AI-powered tool designed for librarians and archivists to accelerate collections processing. It's part of JSTOR Digital Stewardship Services (Tier 3) and helps generate:

- **Descriptive metadata** — Standards-aligned metadata at the item level
- **Transcripts** — Full-text transcriptions for handwritten, typed, and mixed-media items
- **Collection summaries** — Structured overviews to support finding aids and reports

Seeklight is built with "AI drafts, people decide" workflows—all AI-generated content is surfaced for human review, editing, and approval.

## Prerequisites

To use JSTOR Seeklight, your institution must:

1. **Subscribe to JSTOR Digital Stewardship Services Tier 3**
   - Contact JSTOR to inquire about institutional subscription: [https://about.jstor.org/products/digital-stewardship/](https://about.jstor.org/products/digital-stewardship/)
   - Consider joining the [charter program](https://about.jstor.org/products/digital-stewardship/charter-program/) to help shape the tool's development

2. **Have access to the JSTOR Stewardship platform**
   - Web-based interface (no software installation required)
   - Credentials provided by your institution's JSTOR administrator

## How to Access Seeklight

1. **Log in to JSTOR Stewardship**
   - **Grinnell College login**: [https://stewardship.jstor.org/#/login?redirect=/dashboard](https://stewardship.jstor.org/#/login?redirect=/dashboard)
   - Use your institutional credentials to sign in

2. **Access Seeklight features**
   - Seeklight capabilities are integrated throughout the Stewardship platform
   - Look for options like "Generate Metadata," "Create Transcript," or "Generate Summary"

## Using Seeklight to Generate Metadata for a Single Object

### Step 1: Upload Your Digital Object

1. In the JSTOR Stewardship platform, navigate to your collection or project
2. Upload your digital object file(s):
   - Images (JPEG, TIFF, PNG)
   - PDFs
   - Audio files (MP3, WAV)
   - Video files
   - Text documents

### Step 2: Generate Metadata

1. Select the uploaded object
2. Click the **"Generate Metadata"** button
3. Seeklight will analyze the object and create:
   - Title
   - Description/Abstract
   - Subject terms
   - Date information (if visible in the object)
   - Format and type information
   - Other relevant descriptive metadata fields

### Step 3: Review and Edit

1. **Review the generated metadata**
   - AI-generated fields are tagged/labeled for easy identification
   - Each field includes a confidence score (when applicable)

2. **Edit as needed**
   - Correct any inaccuracies
   - Add context that the AI couldn't infer
   - Enhance descriptions with institutional knowledge
   - Verify dates, names, and proper nouns

3. **Approve or regenerate**
   - Accept the metadata to add it to your record
   - Or regenerate if the results aren't suitable

### Step 4: Export Metadata

1. Once approved, metadata becomes part of the object's record
2. Export options:
   - Download as JSON (for Seeklight-format metadata)
   - Export according to your metadata schema (DC, MODS, etc.)
   - Share to JSTOR for public access
   - Export via OAI-PMH to other systems

## Additional Seeklight Features

### Generate Transcripts

For text-based materials (letters, manuscripts, typed documents):

1. Select your object
2. Click **"Create Transcript"**
3. Review and edit the generated transcript
4. Transcripts support full-text search and accessibility

### Create Collection Summaries

For groups of related objects:

1. Select a collection or batch of items
2. Click **"Generate Summary"**
3. Seeklight identifies themes, patterns, and key information
4. Export summaries to enrich finding aids and reports

## Best Practices

- **Always review AI-generated content** — Seeklight is designed to assist, not replace, human expertise
- **Start with a pilot batch** — Test Seeklight on 10-20 objects before processing larger collections
- **Document your workflow** — Note which fields typically need manual correction
- **Track processing time** — Monitor efficiency gains and areas for improvement
- **Contribute feedback** — Share insights with JSTOR to help improve the tool

## Saving Seeklight Output for LAMP

When using Seeklight for objects in this repository:

1. Generate and review metadata using the steps above
2. Export the metadata in JSON format
3. Save the file in [`../sample-objects/seeklight-metadata/`](../sample-objects/seeklight-metadata/) using the object's Title as the filename (e.g., `Stewart Public Library, Grinnell, Iowa.json`)
4. Compare with existing DC metadata in [`../sample-objects/existing-dc-metadata/`](../sample-objects/existing-dc-metadata/)
5. Update [`field-mapping.md`](field-mapping.md) with any new field mappings you identify

## Resources

- **Seeklight Product Page**: [https://about.jstor.org/products/digital-stewardship/seeklight/](https://about.jstor.org/products/digital-stewardship/seeklight/)
- **JSTOR Stewardship Support**: [https://support.jstor.org/](https://support.jstor.org/)
- **Case Studies**: Read how other institutions use Seeklight at [https://about.jstor.org/case-study/](https://about.jstor.org/case-study/)
- **Seeklight Blog Posts**: [https://about.jstor.org/blog/](https://about.jstor.org/blog/) (search for "Seeklight")

## Grinnell College Specific Information

> **Note**: Contact Grinnell College's Digital Collections team or library administration for information about:
> - Institutional access credentials
> - Current subscription tier
> - Recommended workflows
> - Local training and support resources

---

*Last updated: April 30, 2026*

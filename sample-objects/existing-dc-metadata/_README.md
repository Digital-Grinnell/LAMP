# Existing DC Metadata

This directory contains existing Dublin Core (DC) and DCTerms metadata for each sample digital object.

## File Naming Convention

Files should be named to match their corresponding digital object's Title, e.g.:

- `Lucille Ley to Jimmy Ley - June 21, 1943.md` — Markdown file with DC metadata for the object with this title
- `Stewart Public Library, Grinnell, Iowa.md` — Markdown file with DC metadata for the object with this title

## Dublin Core Elements Reference

The following DC elements are used in our metadata records:

| Element         | DC Term URI                                           | Description                                      |
|-----------------|-------------------------------------------------------|--------------------------------------------------|
| Title           | `dc:title`                                            | A name given to the resource                     |
| Creator         | `dc:creator`                                          | An entity primarily responsible for the content |
| Subject         | `dc:subject`                                          | The topic of the resource                        |
| Description     | `dc:description`                                      | An account of the resource                       |
| Publisher       | `dc:publisher`                                        | An entity responsible for making the resource available |
| Contributor     | `dc:contributor`                                      | An entity responsible for contributions          |
| Date            | `dc:date`                                             | A point or period of time                        |
| Type            | `dc:type`                                             | The nature or genre of the resource              |
| Format          | `dc:format`                                           | The file format or physical medium               |
| Identifier      | `dc:identifier`                                       | An unambiguous reference to the resource         |
| Source          | `dc:source`                                           | A related resource from which this is derived    |
| Language        | `dc:language`                                         | A language of the resource                       |
| Relation        | `dc:relation`                                         | A related resource                               |
| Coverage        | `dc:coverage`                                         | The spatial or temporal topic of the resource    |
| Rights          | `dc:rights`                                           | Information about rights held in the resource    |

## DCTerms Extensions

Extended DCTerms elements in use may include `dcterms:alternative`, `dcterms:tableOfContents`, `dcterms:abstract`, `dcterms:created`, `dcterms:issued`, `dcterms:modified`, `dcterms:spatial`, `dcterms:temporal`, and others as appropriate.

### 12
We need some testing of Seeklight's prompt and its impact on generated metadata, if any.  Results of two "prompted" analysis are held in the "mapped-metadata-Rev-2" directory.  

#### Developmental Dilemmas
New metadata generation around "Developmental Dilemmas: The Role of Power and Agency" was run using this prompt:  

```
This is a digitized PDF copy of a print book with supplemental appendices (in the digital edition only).  The book by Grinnell College faculty member William D. Ferguson is titled "Developmental Dilemmas: The Role of Power and Agency".  It is part of the Digital Grinnell Faculty Scholarship collection. 
```

The result is /Users/mcfatem/GitHub/LAMP/sample-objects/seeklight-metadata-Rev-2/New_LAMP_628632.csv, and the corresponding .xlsx file.  

Copilot comparison of the old versus new metadata points out these differences:  


Let me read both files to compare them:   

Read [seeklight-metadata-Rev-2/New_LAMP_628632.csv](sample-objects/seeklight-metadata-Rev-2/New_LAMP_628632.csv)

Read [seeklight-metadata-Rev-1/New_LAMP_628302.csv](sample-objects/seeklight-metadata-Rev-1/New_LAMP_628302.csv#1-1), lines 1 to 1

Read [seeklight-metadata-Rev-1/New_LAMP_628302.csv](sample-objects/seeklight-metadata-Rev-1/New_LAMP_628302.csv#4-4), lines 4 to 4

Here's a detailed comparison of the **"Developmental Dilemmas"** record between Rev-2 and Rev-1 (row 4):

## Key Differences

| Field | Rev-2 (New_LAMP_628632.csv) | Rev-1 (New_LAMP_628302.csv - Row 4) |
|-------|----------------------------|--------------------------------------|
| **SSID** | 42358758 | 42356814 |
| **Description** | "examining why developmental policies often fail, focusing on the roles of power, agency, and collective-action problems..." | "analyzing why developmental policies often fail, focusing on the interplay of power, agency, and institutional evolution..." |
| **Subject** | Development economics \| Economic development \| Power resources \| Institution building \| Collective behavior \| Leadership \| Corruption | Development economics \| Corruption \| Power resources \| Leadership \| Institutional economics \| Collective behavior \| Political corruption |
| **Type** | Book | Monograph |
| **Coverage (culture)** | American | Global |
| **Format (medium)** | paper | Digital text |
| **Format (technique)** | printed | typed |
| **Format (material)** | paper | PDF file |
| **Publisher** | Cambridge University Press | Cambridge University Press \| UNU-WIDER |
| **Named Entities** | ...University of Cambridge... (added) | (not present) |
| **Keywords** | ...social identity \| ...developmental policy... | ...social identities \| ...inclusive development... |
| **Media URL** | .../42358758/... | .../42356814/... |

## Summary

The two records describe the same book but with notable differences:

1. **Different SSIDs** - Suggesting these are separate Seeklight processing runs
2. **Physical vs Digital** - Rev-2 describes it as a physical paper book, Rev-1 as a digital PDF
3. **Type terminology** - "Book" vs "Monograph" 
4. **Culture scope** - "American" vs "Global"
5. **Description variations** - Slight rewording with similar content
6. **Subject terms** - Different controlled vocabulary choices ("Economic development" vs "Institutional economics", "Corruption" vs "Political corruption")
7. **Publisher** - Rev-2 omits "UNU-WIDER" co-publisher
8. **Named Entities** - Rev-2 adds "University of Cambridge"

These differences suggest Rev-2 may be a revised/reprocessed metadata export with updated or corrected field values.


#### Stewart Public Library
New metadata generation around the "Stewart Public Library" postcard was run using this prompt:  

```
This is a postcard from the Digital Grinnell Ivan Sheets Postcard Collection and is related to the Poweshiek History Preservation Project, and Drake Community Library (Grinnell, Iowa) Archives.  The verso side of the card appears to be an invitation to an anniversary event in the library in May 1977.    
```

The result is /Users/mcfatem/GitHub/LAMP/sample-objects/seeklight-metadata-Rev-2/New_LAMP_628665.csv, and the corresponding .xlsx file.  

Copilot comparison of the old versus new metadata points out these differences: 


Read [seeklight-metadata-Rev-2/New_LAMP_628665.csv](sample-objects/seeklight-metadata-Rev-2/New_LAMP_628665.csv)

Read [seeklight-metadata-Rev-1/New_LAMP_628302.csv](sample-objects/seeklight-metadata-Rev-1/New_LAMP_628302.csv#5-5), lines 5 to 5

Here's a detailed comparison of the **"Stewart Library 75th Anniversary Invitation"** record between Rev-2 and Rev-1 (row 5):

## Key Differences

| Field | Rev-2 (New_LAMP_628665.csv) | Rev-1 (New_LAMP_628302.csv - Row 5) |
|-------|----------------------------|--------------------------------------|
| **SSID** | 42358859 | 42356813 |
| **Title** | Seventy-Fifth Anniversary Invitation for Stewart Library | Seventy-Fifth Anniversary Invitation for Stewart Library, Grinnell, Iowa |
| **Description** | "Invitation postcard from Stewart Library in Grinnell, Iowa, announcing its seventy-fifth anniversary...The event was scheduled for May 15, 1977." | "Invitation to the seventy-fifth anniversary ceremonies...The document includes a black and white halftone image of the Stewart Public Library building, with a caption noting its dedication on May 9, 1902." |
| **Subject** | Anniversaries \| Library sites \| Illustrators \| Special events \| Piano trios \| Community life \| Open admission | Anniversaries \| Library buildings \| Art exhibition audiences \| Illustrators \| Piano trios \| Exhibitions |
| **Type** | Postcard | Invitation |
| **Coverage (style)** | invitation | commemorative print |
| **Coverage (location)** | Grinnell, Iowa | Grinnell, Iowa, United States |
| **Format (medium)** | paper | printed paper |
| **Format (technique)** | printed | halftone printing and letterpress |
| **Format (material)** | cardstock | ink on paper |
| **Format (measurements)** | N/A | Unknown |
| **Named Entities** | Stewart Library \| Grinnell, Iowa \| Lloyd Herfindahl \| Mirecourt Trio | Stewart Library \| Grinnell \| Iowa \| Lloyd Herfindahl \| Mirecourt Trio |
| **Keywords** | library anniversary \| Stewart Library \| Grinnell Iowa \| ... \| community events \| open house | Stewart Library \| Grinnell \| Iowa \| anniversary \| open house \| art exhibition \| ... |
| **Media URL** | .../42358859/... | .../42356813/... |

## Summary

Both records describe the same physical item (the Stewart Library 75th anniversary invitation) but with significant differences:

1. **Different SSIDs** - Different Seeklight processing runs
2. **Title** - Rev-2 omits "Grinnell, Iowa" from title
3. **Type classification** - "Postcard" vs "Invitation"
4. **Style** - "invitation" vs "commemorative print"
5. **Description focus** - Rev-2 describes it as a postcard announcing the event; Rev-1 mentions the halftone image and 1902 dedication date
6. **Subject terms** - Different controlled vocabulary:
   - Rev-2: "Library sites", "Special events", "Community life", "Open admission"
   - Rev-1: "Library buildings", "Art exhibition audiences", "Exhibitions"
7. **Format specificity** - Rev-1 more detailed ("halftone printing and letterpress") vs Rev-2 generic ("printed")
8. **Material** - "cardstock" vs "ink on paper"
9. **Location format** - Rev-2 uses comma format "Grinnell, Iowa"; Rev-1 separates with pipes and adds "United States"

Rev-2 appears to characterize this more as a postcard-style invitation with community focus, while Rev-1 emphasizes the commemorative/exhibition nature with more technical printing details.

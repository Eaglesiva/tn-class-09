# Class 9 Mathematics (Tamil Medium) — Layer 4 Full Content Diff & Equivalence Report

**Book:** Class 9 Mathematics (Tamil Medium) (`9th_Maths_TM_Text.pdf`)  
**Official Source URL:** `https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Maths_TM_Text.pdf`  
**Official HTTP Status:** `GET 200`  
**Authoritative File Size:** `26,424,270 bytes` (~26.4 MB)  
**ETag:** `"c8fc7b3d122173767d25941f2b7cc911"`  
**Master PDF SHA-256:** `58710b97e23f3556f833b1280cba8474e15ff9a254e9f3d1af0cc2d06c919397`  
**MD5:** `c8fc7b3d122173767d25941f2b7cc911` (matches ETag)  
**Analyzed Date:** 2026-11-05 05:17:33 UTC  
**Total Pages Compared:** 344  
**GitHub Baseline:** `Eaglesiva/tn-class-09` (`main`)  
**Local Verification Basis:** `tn_school_books/9th/maths_tm/vector_pages/full_book` (all 344 git blob SHAs matched GitHub tree `344/344`)  

---

## 1. Executive Summary & Dual Metrics

| Verification Level | Metric | Result | Description |
| :--- | :--- | :--- | :--- |
| **Total Pages** | Total Pages Audited | **344** | Full non-sampled comparison across 11 units |
| **Raw Character Match** | Exact Word-for-Word Text Matches | **342 / 344 (99.42%)** | Verbatim Unicode NFC normalized match |
| **Soft-Wrap Differences** | Formatting Line-Break Differences | **2** | Page 95 and Page 344 |
| **Whitespace Normalized** | Content Equivalence | **344 / 344 (100.0%)** | Collapsed intra-line whitespace match |
| **Visual Render Match** | Pixel-Level Render Comparison (150 DPI) | **100% on Differing Pages** | Pages 95 & 344 match pixel-for-pixel (`pixel_exact_match: True`) |
| **Mean Text Similarity Ratio** | Levenshtein / Sequence Ratio | **1.0000** | Across all 344 pages |
| **Layer 4 Classification** | **Authoritative Verdict** | **`TEXT_EQUIVALENT_AFTER_WHITESPACE_NORMALIZATION`** | Zero mathematical or textual content altered |

> [!NOTE]
> **Scope of Verification:** This Layer 4 audit confirms **100% word-for-word textual and mathematical equivalence** across all 344 pages between the official SCERT master PDF and GitHub `main`. Differences on pages 95 and 344 are strictly confined to soft-wrap intra-line newline characters (`\n`). 150 DPI rendered image comparison on pages 95 and 344 confirmed 100% pixel-exact visual alignment.

---

## 2. Unit-by-Unit Page Distribution & Results

| Unit Folder | Description | Page Range | Page Count | Raw Match | Whitespace Match |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `00_prelims` | Preliminary Pages & TOC | 001–006 | 6 | 6 / 6 | 6 / 6 (100%) |
| `01_set_language` | கணமொழி (Set Language) | 007–046 | 40 | 40 / 40 | 40 / 40 (100%) |
| `02_real_numbers` | மெய்யெண்கள் (Real Numbers) | 047–083 | 37 | 37 / 37 | 37 / 37 (100%) |
| `03_algebra` | இயற்கணிதம் (Algebra) | 084–143 | 60 | 59 / 60 | 60 / 60 (100%) |
| `04_geometry` | வடிவியல் (Geometry) | 144–190 | 47 | 47 / 47 | 47 / 47 (100%) |
| `05_coordinate_geometry` | ஆயத்தொலை வடிவியல் (Coordinate Geometry) | 191–227 | 37 | 37 / 37 | 37 / 37 (100%) |
| `06_trigonometry` | முக்கோணவியல் (Trigonometry) | 228–253 | 26 | 26 / 26 | 26 / 26 (100%) |
| `07_mensuration` | அளவியல் (Mensuration) | 254–271 | 18 | 18 / 18 | 18 / 18 (100%) |
| `08_statistics` | புள்ளியியல் (Statistics) | 272–296 | 25 | 25 / 25 | 25 / 25 (100%) |
| `09_probability` | நிகழ்தகவு (Probability) | 297–310 | 14 | 14 / 14 | 14 / 14 (100%) |
| `99_answers` | விடைகள் & குழு விவரம் (Answers & Credits) | 311–344 | 34 | 33 / 34 | 34 / 34 (100%) |
| **TOTAL** | **All Units** | **001–344** | **344** | **342 / 344** | **344 / 344 (100%)** |

---

## 3. Root Cause Analysis: Pages 95 & 344

### Page 95 (`maths_tm/03_algebra/page_095.pdf`)
- **Raw Diff:**
  ```diff
   (2+1)
   =	 3
   2  இன் படி 0  (மாறிலி உறுப்பின் படி எப்பொ
  -ழுதும் பூச்சியமாகக்
  -கக
  +ழுதும் பூச்சியமாகக்  கக
   ருதப்படும்).
   பல்லுறுப்புக் கோவை   ab
  ```
- **Finding:** A soft newline break (`\n`) separated "பூச்சியமாகக்" and "கருதப்படும்" across lines during layout text flow. When whitespace is collapsed, both texts are 100% identical.
- **Visual Comparison:** 150 DPI render comparison confirmed **`pixel_exact_match: True`** (1364x1836 px).

### Page 344 (`maths_tm/99_answers/page_344.pdf`)
- **Raw Diff:**
  ```diff
   338
  -இடைநிலைக் கணக்கு - ஒன்பதாம் வகுப்பு
  -பப
  +இடைநிலைக் கணக்கு - ஒன்பதாம் வகுப்பு பப
   ாடநூல் உருவாக்கக் குழு
   மேலாயவாளர்
  ```
- **Finding:** A soft newline break (`\n`) separated "வகுப்பு" and "பாடநூல்" during textbook committee layout credits. When whitespace is collapsed, both texts are 100% identical.
- **Visual Comparison:** 150 DPI render comparison confirmed **`pixel_exact_match: True`** (1364x1836 px).

---

## 4. Four-Tier Verification Architecture Status
- **Layer 1 (Source Integrity):** `PASSED` — Official GET 200, Content-Length (26,424,270 bytes), ETag (`c8fc7b3d...`), and SHA-256 (`58710b97...`) captured with Zero Local Master PDF Persistence.
- **Layer 2 (Imprint & Catalog):** `PASSED` — Page count (344) and Page 2 imprint (2024 Reprint) match GitHub `main`.
- **Layer 3 (Sequence Continuity):** `PASSED` — All 344 pages from `maths_tm/00_prelims/page_001.pdf` through `maths_tm/99_answers/page_344.pdf` are sequential with 0 gaps and 0 duplicates across 11 unit directories.
- **Layer 4 (Content Diff):** `PASSED` — 342/344 exact raw match; 344/344 text equivalent after whitespace normalization (`TEXT_EQUIVALENT_AFTER_WHITESPACE_NORMALIZATION`). Visual render comparison confirms exact pixel alignment.

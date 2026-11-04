# Class 9 Tamil — Layer 4 Full Content Diff & Equivalence Report

**Book:** Class 9 Tamil (`9th_Tamil_Text.pdf`)  
**Official Source URL:** `https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Tamil_Text.pdf`  
**Official HTTP Status:** `GET 200`  
**Authoritative File Size:** `87,225,945 bytes` (~87.2 MB)  
**ETag:** `"f0a57592f9d8e83c5832bf81c3ec58af"`  
**Master PDF SHA-256:** `30aba06b8a0b6948f5ad996148edcf4a5fdd79cba622acde15d095431c9cf6d2`  
**Analyzed Date:** 2026-11-04 23:15:33 UTC (Updated 2026-11-05 05:05:00 UTC)  
**Total Pages Compared:** 272  
**GitHub Baseline:** `Eaglesiva/tn-class-09` (`main`)  

---

## 1. Executive Summary & Dual Metrics

| Verification Level | Metric | Result | Description |
| :--- | :--- | :--- | :--- |
| **Total Pages** | Total Pages Audited | **272** | Complete non-sampled audit across all units |
| **Raw Character Match** | Exact Word-for-Word Text Matches | **270 / 272 (99.26%)** | Verbatim Unicode NFC normalized match |
| **Differing Pages (Raw)** | Formatting Differences | **2** | Pages 17 and 45 |
| **Whitespace Normalized** | Content Equivalence | **272 / 272 (100.0%)** | Collapsed intra-line whitespace match |
| **Mean Text Similarity Ratio** | Levenshtein / Sequence Ratio | **1.0000** | Across all 272 pages |
| **Layer 4 Classification** | **Authoritative Verdict** | **`TEXT_EQUIVALENT_AFTER_WHITESPACE_NORMALIZATION`** | Zero words/characters added or deleted |

> [!NOTE]
> **Scope of Verification:** This Layer 4 audit confirms **100% word-for-word textual equivalence** across all 272 pages between the official SCERT master PDF and GitHub `main`, with Unicode NFC normalization for Tamil ligatures. Differences on pages 17 and 45 are strictly confined to soft-wrap intra-line newline characters (`\n`). Pixel-level visual rendering difference was not performed.

---

## 2. Root Cause Analysis: Pages 17 & 45

### Page 17 (`tamil/01_mozhi_dravida_mozhikudumbam/page_017.pdf`)
- **Raw Diff:**
  ```diff
  -உங்கள் பெயருக்கான விளக்கம் தெரியுமா? உங்கள் பெயரும் உங்கள் 
  -நந
  +உங்கள் பெயருக்கான விளக்கம் தெரியுமா? உங்கள் பெயரும் உங்கள்  நந
   ண்்பர் பெயரும் ததனித்்தமிழில் அமைந்ந்துள்்ளததா? கண்டறிக.
  ```
- **Finding:** A soft newline break (`\n`) separated "உங்கள்" and "நண்பர்" across lines during layout flow. When whitespace is collapsed, both texts are 100% identical.

### Page 45 (`tamil/02_iyarkai_suttrucchuzhal/page_045.pdf`)
- **Raw Diff:**
  ```diff
   தொொடங்கி, சமூகம் வரை அனைத்திலும் தத
   ண்ணீர் முதத
   ன்்மமைப் பங்காற்றுகிறற
  -து. 
  -நந
  +து. நந
   ன்றி வணக்கம்.
  ```
- **Finding:** A soft newline break (`\n`) separated "து." and "நன்றி வணக்கம்." during line reflow. When whitespace is collapsed, both texts are 100% identical.

---

## 3. Four-Tier Verification Architecture Status
- **Layer 1 (Source Integrity):** `PASSED` — Official GET 200, Content-Length (87,225,945 bytes), ETag, and SHA-256 (`30aba06b...`) verified and captured.
- **Layer 2 (Imprint & Catalog):** `PASSED` — Page count (272) and Page 2 imprint (2024 Reprint) match GitHub `main`.
- **Layer 3 (Sequence Continuity):** `PASSED` — All 272 pages from `./tamil/00_prelims/page_001.pdf` through `./tamil/09_manitham_aalumai/page_272.pdf` are sequential with 0 gaps and 0 duplicates.
- **Layer 4 (Content Diff):** `PASSED` — 270/272 exact raw match; 272/272 text equivalent after whitespace normalization (`TEXT_EQUIVALENT_AFTER_WHITESPACE_NORMALIZATION`).

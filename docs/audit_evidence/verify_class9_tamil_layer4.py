#!/usr/bin/env python3
"""
Portable Layer 4 Content Diff Verification Script for Class 9 Tamil
Compares official SCERT Master PDF against GitHub main split pages with Unicode NFC normalization.
Includes both Raw NFC Match and Whitespace-Normalized Equivalence checks.
Zero Local Master PDF persistence: Master PDF is streamed into memory and discarded.
"""
import io, os, sys, glob, json, difflib, requests, unicodedata
import fitz  # PyMuPDF

def run_layer4_verification(pages_dir, official_url="https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Tamil_Text.pdf"):
    print(f"Loading local split pages from: {pages_dir}")
    local_pages = sorted(glob.glob(os.path.join(pages_dir, "**/page_*.pdf"), recursive=True))
    if len(local_pages) != 272:
        raise ValueError(f"Expected 272 split pages, found {len(local_pages)}")

    print(f"Streaming official master PDF from: {official_url}")
    r = requests.get(official_url, timeout=90)
    r.raise_for_status()
    pdf_bytes = r.content
    print(f"Downloaded {len(pdf_bytes)} bytes.")

    doc_master = fitz.open(stream=pdf_bytes, filetype="pdf")
    if len(doc_master) != 272:
        raise ValueError(f"Master PDF has {len(doc_master)} pages, expected 272")

    results = []
    raw_exact_matches = 0
    ws_normalized_matches = 0

    for i in range(272):
        p_num = i + 1
        m_text = doc_master[i].get_text()
        with open(local_pages[i], 'rb') as fp:
            doc_l = fitz.open(stream=fp.read(), filetype="pdf")
            l_text = doc_l[0].get_text() if len(doc_l) > 0 else ""
            doc_l.close()

        m_clean = unicodedata.normalize('NFC', "\n".join(l.strip() for l in m_text.splitlines() if l.strip()))
        l_clean = unicodedata.normalize('NFC', "\n".join(l.strip() for l in l_text.splitlines() if l.strip()))

        is_raw_exact = (m_clean == l_clean)
        ratio = difflib.SequenceMatcher(None, m_clean, l_clean).ratio()
        if is_raw_exact:
            raw_exact_matches += 1

        # Whitespace-collapsed check
        m_ws = " ".join(m_clean.split())
        l_ws = " ".join(l_clean.split())
        is_ws_match = (m_ws == l_ws)
        if is_ws_match:
            ws_normalized_matches += 1

        results.append({
            "page_number": p_num,
            "is_raw_exact_match": is_raw_exact,
            "is_whitespace_normalized_match": is_ws_match,
            "similarity_ratio": round(ratio, 4),
            "master_char_count": len(m_clean),
            "local_char_count": len(l_clean)
        })

    doc_master.close()
    del doc_master
    del pdf_bytes

    print(f"Verification complete:")
    print(f"  - Raw Exact Matches: {raw_exact_matches}/272 ({raw_exact_matches/272*100:.2f}%)")
    print(f"  - Whitespace-Normalized Matches: {ws_normalized_matches}/272 ({ws_normalized_matches/272*100:.2f}%)")
    print(f"  - Verdict: {'TEXT_EQUIVALENT_AFTER_WHITESPACE_NORMALIZATION' if ws_normalized_matches == 272 else 'CONTENT_DIFFERENCES_DETECTED'}")
    return results

if __name__ == "__main__":
    split_dir = sys.argv[1] if len(sys.argv) > 1 else "tn_school_books/9th/tamil/vector_pages/full_book"
    run_layer4_verification(split_dir)

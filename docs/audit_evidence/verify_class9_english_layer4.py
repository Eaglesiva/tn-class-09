#!/usr/bin/env python3
"""
Portable Layer 4 Content Diff Verification Script for Class 9 English
Compares official SCERT Master PDF against GitHub main split pages.
Zero Local Master PDF persistence: Master PDF is streamed into memory and discarded.
"""
import io, os, sys, glob, json, difflib, requests
import fitz  # PyMuPDF
import datetime

def run_layer4_verification(pages_dir, official_url="https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th%20English_Text.pdf"):
    print(f"Loading local split pages from: {pages_dir}")
    local_pages = sorted(glob.glob(os.path.join(pages_dir, "**/page_*.pdf"), recursive=True))
    if len(local_pages) != 224:
        raise ValueError(f"Expected 224 split pages, found {len(local_pages)}")

    print(f"Streaming official master PDF from: {official_url}")
    r = requests.get(official_url, timeout=60)
    r.raise_for_status()
    pdf_bytes = r.content
    print(f"Downloaded {len(pdf_bytes)} bytes.")

    doc_master = fitz.open(stream=pdf_bytes, filetype="pdf")
    if len(doc_master) != 224:
        raise ValueError(f"Master PDF has {len(doc_master)} pages, expected 224")

    results = []
    perfect_matches = 0
    for i in range(224):
        p_num = i + 1
        m_text = doc_master[i].get_text()
        with open(local_pages[i], 'rb') as fp:
            doc_l = fitz.open(stream=fp.read(), filetype="pdf")
            l_text = doc_l[0].get_text() if len(doc_l) > 0 else ""
            doc_l.close()

        m_clean = "\n".join(l.strip() for l in m_text.splitlines() if l.strip())
        l_clean = "\n".join(l.strip() for l in l_text.splitlines() if l.strip())

        is_exact = (m_clean == l_clean)
        ratio = difflib.SequenceMatcher(None, m_clean, l_clean).ratio()
        if is_exact:
            perfect_matches += 1

        results.append({
            "page_number": p_num,
            "is_exact_match": is_exact,
            "similarity_ratio": round(ratio, 4),
            "master_char_count": len(m_clean),
            "local_char_count": len(l_clean)
        })

    doc_master.close()
    del doc_master
    del pdf_bytes

    print(f"Verification complete: {perfect_matches}/224 exact matches.")
    return results

if __name__ == "__main__":
    split_dir = sys.argv[1] if len(sys.argv) > 1 else "tn_school_books/9th/english/vector_pages/full_book"
    run_layer4_verification(split_dir)

import os, sys, json, time, requests, fitz, hashlib, subprocess, glob

print("=================================================================")
print("SCERT 2026-27 - OFFICIAL PDF DIRECT REFRESH: CLASS 9 (5 BOOKS)")
print("=================================================================")

TARGET_BOOKS = [
    {
        "key": "maths_em",
        "class": "9",
        "subject": "Mathematics",
        "medium": "English",
        "expected_pages": 328,
        "folder": "maths_em",
        "url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Maths_EM_Text.pdf",
        "official_filename": "9th_Maths_EM_Text.pdf"
    },
    {
        "key": "science_tm",
        "class": "9",
        "subject": "Science",
        "medium": "Tamil",
        "expected_pages": 336,
        "folder": "science_tm",
        "url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Science_TM_Text.pdf",
        "official_filename": "9th_Science_TM_Text.pdf"
    },
    {
        "key": "science_em",
        "class": "9",
        "subject": "Science",
        "medium": "English",
        "expected_pages": 328,
        "folder": "science_em",
        "url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Science_EM_Text.pdf",
        "official_filename": "9th_Science_EM_Text.pdf"
    },
    {
        "key": "social_science_tm",
        "class": "9",
        "subject": "Social Science",
        "medium": "Tamil",
        "expected_pages": 344,
        "folder": "social_science_tm",
        "url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Social%20Science_TM_Text.pdf",
        "official_filename": "9th_Social Science_TM_Text.pdf"
    },
    {
        "key": "social_science_em",
        "class": "9",
        "subject": "Social Science",
        "medium": "English",
        "expected_pages": 328,
        "folder": "social_science_em",
        "url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Social%20Science_EM_Text.pdf",
        "official_filename": "9th_Social Science_EM_Text.pdf"
    }
]

os.makedirs("docs/refresh_evidence", exist_ok=True)
all_evidence = []

# Git author config
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])

for idx, b in enumerate(TARGET_BOOKS, 1):
    print(f"\n=======================================================")
    print(f"[{idx:02d}/05] PROCESSING: {b['subject']} ({b['medium']}) - {b['expected_pages']}p")
    print(f"URL: {b['url']}")
    print(f"Folder: {b['folder']}")
    print(f"=======================================================")
    
    # 1. Identify existing page PDF paths
    all_existing_pages = sorted(glob.glob(os.path.join(b['folder'], "**", "page_*.pdf"), recursive=True))
    print(f"Existing page PDF count: {len(all_existing_pages)} (Expected: {b['expected_pages']})")
    
    if len(all_existing_pages) != b['expected_pages']:
        print(f"ERROR: Page count mismatch in repository! Found {len(all_existing_pages)} != {b['expected_pages']}. Skipping book.")
        continue
        
    # 2. Download Official Master PDF to /tmp
    temp_pdf_path = f"/tmp/master_c9_{b['key']}.pdf"
    print(f"Downloading master PDF to {temp_pdf_path}...")
    t0 = time.time()
    
    try:
        resp = requests.get(b['url'], headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=120)
        resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: Download failed: {e}. Skipping book.")
        continue
        
    content_length = int(resp.headers.get('Content-Length', 0))
    etag = resp.headers.get('ETag', '').strip('"')
    last_modified = resp.headers.get('Last-Modified', '')
    
    sha256 = hashlib.sha256()
    with open(temp_pdf_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
                sha256.update(chunk)
                
    master_sha256 = sha256.hexdigest()
    master_size = os.path.getsize(temp_pdf_path)
    print(f"Downloaded {master_size} bytes in {time.time() - t0:.2f}s | SHA-256: {master_sha256}")
    
    # Magic bytes check
    with open(temp_pdf_path, 'rb') as f:
        magic = f.read(5)
    if not magic.startswith(b'%PDF'):
        print(f"ERROR: Invalid PDF magic bytes: {magic}. Skipping book.")
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        continue
        
    # 3. Open PyMuPDF and Validate Page Count
    doc = fitz.open(temp_pdf_path)
    master_page_count = len(doc)
    print(f"Master PDF Page Count: {master_page_count}")
    
    if master_page_count != b['expected_pages']:
        print(f"ERROR: Master page count {master_page_count} != Expected {b['expected_pages']}. Skipping book.")
        doc.close()
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        continue
        
    # 4. In-Place Single-Page PDF Splitting & Overwrite
    print(f"Splitting master PDF and overwriting {master_page_count} pages in {b['folder']}...")
    split_success_count = 0
    for p_idx in range(master_page_count):
        dest_page_path = all_existing_pages[p_idx]
        single_doc = fitz.open()
        single_doc.insert_pdf(doc, from_page=p_idx, to_page=p_idx)
        single_doc.save(dest_page_path)
        single_doc.close()
        
        # Validation
        check_doc = fitz.open(dest_page_path)
        if len(check_doc) != 1 or os.path.getsize(dest_page_path) == 0:
            print(f"FAILED validation on {dest_page_path}!")
            check_doc.close()
            doc.close()
            sys.exit(1)
        check_doc.close()
        split_success_count += 1
        
    print(f"Successfully split and validated {split_success_count} / {master_page_count} pages.")
    
    # 5. Delete temporary master PDF immediately
    doc.close()
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)
        print("Zero Local Master PDF Persistence: /tmp master PDF removed.")
        
    # 6. Verify Git Safety & Restore any untouched non-PDF files
    p_status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    for line in p_status.stdout.splitlines():
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            fpath = parts[1]
            if not fpath.endswith('.pdf') and not fpath.startswith('.github/') and not fpath.startswith('docs/refresh_evidence/'):
                subprocess.run(['git', 'checkout', '--', fpath])
                print(f"Restored untouched non-pdf file: {fpath}")
                
    # 7. Write Evidence Record
    evidence = {
        "book_id": f"class_09_{b['key']}",
        "class": "9",
        "subject": b['subject'],
        "medium": b['medium'],
        "official_filename": b['official_filename'],
        "official_url": b['url'],
        "http_status": "GET_200",
        "content_length": master_size,
        "etag": etag,
        "last_modified": last_modified,
        "sha256": master_sha256,
        "expected_page_count": b['expected_pages'],
        "actual_page_count": master_page_count,
        "pages_replaced_count": split_success_count,
        "all_pages_validated": True,
        "refresh_status": "OFFICIAL_SOURCE_REFRESHED",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "zero_master_pdf_persistence_verified": True
    }
    
    ev_path = f"docs/refresh_evidence/class_09_{b['key']}_refresh_evidence.json"
    with open(ev_path, "w", encoding="utf-8") as f_ev:
        json.dump(evidence, f_ev, indent=2)
    all_evidence.append(evidence)
    
    # 8. Git Commit for This Book
    print(f"Committing changes for {b['subject']} ({b['medium']})...")
    subprocess.run(['git', 'add', b['folder'] + '/', ev_path])
    commit_msg = f"feat(scert): refresh official PDF pages for {b['subject']} ({b['medium']}) [{split_success_count} pages]"
    subprocess.run(['git', 'commit', '-m', commit_msg])

# Final summary evidence
with open("docs/refresh_evidence/class_09_all_refreshed_evidence.json", "w", encoding="utf-8") as f_all:
    json.dump(all_evidence, f_all, indent=2)

print("\n=======================================================")
print(f"Class 9 Refresh Completed: {len(all_evidence)} / 5 books successfully refreshed and committed!")
print("=======================================================")

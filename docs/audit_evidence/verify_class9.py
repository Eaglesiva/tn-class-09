import os, subprocess, requests, json, fitz, tempfile

def get_token():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(input='protocol=https\nhost=github.com\n\n')
    for line in out.splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1]
    return None

token = get_token()
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
repo = 'Eaglesiva/tn-class-09'

# Artifact & render directory
artifact_dir = r"C:\Users\SIVA\.gemini\antigravity\brain\2f602d33-ccf8-4bdf-942b-6bf718b91831"
out_dir = "class9_verification"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(os.path.join(out_dir, "github_p2"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "official_p2"), exist_ok=True)
os.makedirs(os.path.join(out_dir, "rendered_images"), exist_ok=True)

# 8 In-scope State Board Books for Class 9
books = [
    {
        "subject_key": "tamil",
        "subject_name": "தமிழ் (Tamil)",
        "medium": "Tamil",
        "official_fn": "9th_Tamil_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Tamil_Text.pdf"
    },
    {
        "subject_key": "english",
        "subject_name": "ஆங்கிலம் (English)",
        "medium": "English",
        "official_fn": "9th English_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th English_Text.pdf"
    },
    {
        "subject_key": "maths_tm",
        "subject_name": "கணிதம் (Maths TM)",
        "medium": "Tamil",
        "official_fn": "9th_Maths_TM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Maths_TM_Text.pdf"
    },
    {
        "subject_key": "maths_em",
        "subject_name": "Mathematics (EM)",
        "medium": "English",
        "official_fn": "9th_Maths_EM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Maths_EM_Text.pdf"
    },
    {
        "subject_key": "science_tm",
        "subject_name": "அறிவியல் (Science TM)",
        "medium": "Tamil",
        "official_fn": "9th_Science_TM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Science_TM_Text.pdf"
    },
    {
        "subject_key": "science_em",
        "subject_name": "Science (EM)",
        "medium": "English",
        "official_fn": "9th_Science_EM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Science_EM_Text.pdf"
    },
    {
        "subject_key": "social_science_tm",
        "subject_name": "சமூக அறிவியல் (Social TM)",
        "medium": "Tamil",
        "official_fn": "9th_Social Science_TM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Social Science_TM_Text.pdf"
    },
    {
        "subject_key": "social_science_em",
        "subject_name": "Social Science (EM)",
        "medium": "English",
        "official_fn": "9th_Social Science_EM_Text.pdf",
        "official_url": "https://d21mc000xink7q.cloudfront.net/scert/textbook/syllabuspdf/9th_Social Science_EM_Text.pdf"
    }
]

results = []

for b in books:
    s_key = b["subject_key"]
    s_name = b["subject_name"]
    med = b["medium"]
    url = b["official_url"]
    
    print(f"\n=======================================================")
    print(f"Checking Class 9: {s_key} ({med})")
    print(f"=======================================================")
    
    # A. GitHub main: read pages.json and Page 2
    pj_url = f"https://raw.githubusercontent.com/{repo}/main/{s_key}/pages.json"
    r_pj = requests.get(pj_url, headers=headers)
    gh_pages_count = 0
    gh_p2_path = None
    if r_pj.status_code == 200:
        pj_list = r_pj.json()
        gh_pages_count = len(pj_list)
        # Find page 2 in pages.json
        for p in pj_list:
            if "page_002.pdf" in p or "page_02.pdf" in p or "page-002.pdf" in p:
                gh_p2_path = p[2:] if p.startswith("./") else p.lstrip("/")
                break
        if not gh_p2_path and len(pj_list) >= 2:
            gh_p2_path = pj_list[1][2:] if pj_list[1].startswith("./") else pj_list[1].lstrip("/")
            
    print(f"GitHub main pages count: {gh_pages_count}, Page 2 path: {gh_p2_path}")
    
    # Download GitHub main Page 2
    gh_p2_bytes = None
    gh_p2_txt = ""
    img_old_name = f"c9_gh_p2_{s_key}.png"
    if gh_p2_path:
        r_p2 = requests.get(f"https://raw.githubusercontent.com/{repo}/main/{gh_p2_path}", headers=headers)
        if r_p2.status_code == 200:
            gh_p2_bytes = r_p2.content
            with open(os.path.join(out_dir, "github_p2", f"{s_key}_p2.pdf"), "wb") as f_out:
                f_out.write(gh_p2_bytes)
            # Render PNG
            doc_gh = fitz.open(stream=gh_p2_bytes, filetype="pdf")
            if len(doc_gh) > 0:
                pix = doc_gh[0].get_pixmap(dpi=150)
                pix.save(os.path.join(out_dir, "rendered_images", img_old_name))
                pix.save(os.path.join(artifact_dir, img_old_name))
                gh_p2_txt = doc_gh[0].get_text()
            doc_gh.close()
            
    # B. Official SCERT: GET request and Page 2 inspection
    print(f"Probing official URL: {url}")
    off_status = "UNKNOWN"
    off_pages_count = 0
    off_p2_txt = ""
    img_new_name = f"c9_off_p2_{s_key}.png"
    
    try:
        r_head = requests.head(url, timeout=15)
        off_status = f"HTTP_{r_head.status_code}"
        if r_head.status_code == 200:
            # Download full master to temp to extract total pages & Page 2 safely
            tmp_pdf = os.path.join(tempfile.gettempdir(), f"c9_master_{s_key}.pdf")
            print(f"Downloading master to temp for exact inspection...")
            r_get = requests.get(url, stream=True, timeout=120)
            with open(tmp_pdf, "wb") as f_tmp:
                for chunk in r_get.iter_content(1024*1024):
                    if chunk: f_tmp.write(chunk)
            
            doc_off = fitz.open(tmp_pdf)
            off_pages_count = len(doc_off)
            print(f"Official master page count: {off_pages_count}")
            
            if off_pages_count >= 2:
                # Save page 2 pdf
                p2_doc = fitz.open()
                p2_doc.insert_pdf(doc_off, from_page=1, to_page=1)
                p2_doc.save(os.path.join(out_dir, "official_p2", f"{s_key}_p2.pdf"))
                p2_doc.close()
                
                # Render PNG
                pix_off = doc_off[1].get_pixmap(dpi=150)
                pix_off.save(os.path.join(out_dir, "rendered_images", img_new_name))
                pix_off.save(os.path.join(artifact_dir, img_new_name))
                off_p2_txt = doc_off[1].get_text()
                
            doc_off.close()
            if os.path.exists(tmp_pdf): os.remove(tmp_pdf)
            off_status = "200_OK"
        else:
            off_status = f"GET_{r_head.status_code}"
    except Exception as e:
        off_status = f"ERROR: {str(e)[:30]}"
        print(f"Official fetch error: {e}")
        
    # Save verbatim texts
    with open(os.path.join(out_dir, f"txt_gh_{s_key}.txt"), "w", encoding="utf-8") as f:
        f.write(gh_p2_txt)
    with open(os.path.join(out_dir, f"txt_off_{s_key}.txt"), "w", encoding="utf-8") as f:
        f.write(off_p2_txt)
        
    results.append({
        "subject_key": s_key,
        "subject_name": s_name,
        "medium": med,
        "official_url": url,
        "http_status": off_status,
        "gh_pages_count": gh_pages_count,
        "off_pages_count": off_pages_count,
        "img_old": img_old_name,
        "img_new": img_new_name,
        "gh_p2_lines": [l.strip() for l in gh_p2_txt.splitlines() if l.strip()],
        "off_p2_lines": [l.strip() for l in off_p2_txt.splitlines() if l.strip()]
    })

with open(os.path.join(out_dir, "class9_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nClass 9 Quick Verification Script finished successfully!")

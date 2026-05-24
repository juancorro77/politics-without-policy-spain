import json
import os
import re
import urllib.request
import ssl
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Disable SSL verification for urllib
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def make_request(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                return r.read().decode('utf-8')
        except Exception as e:
            if i < retries - 1:
                time.sleep(1)
    return None

def extract_metadata_from_detail(html):
    metadata = {"author": "", "group": "", "pub_id": ""}
    
    # Extract author and group
    author_match = re.search(r'<h3>\s*Autor\s*</h3>\s*<ul>\s*<li><a[^>]*>([^<]+)</a></li>', html, re.IGNORECASE)
    if author_match:
        author_text = author_match.group(1).strip()
        metadata["author"] = author_text
        if "(" in author_text and author_text.endswith(")"):
            parts = author_text.split("(")
            metadata["author"] = parts[0].strip()
            metadata["group"] = parts[1].replace(")", "").strip()
            
    # Extract publication ID
    pub_match = re.search(r'_publicaciones_id_texto=\((DSCD-[^\)]+)\.CODI\.\)', html)
    if pub_match:
        metadata["pub_id"] = pub_match.group(1).strip()
    else:
        pub_match_fallback = re.search(r'href="[^"]*(DSCD-\d+-PL-\d+)\.PDF', html, re.IGNORECASE)
        if pub_match_fallback:
            metadata["pub_id"] = pub_match_fallback.group(1).strip()
            
    return metadata

def process_detail_page(init):
    # This runs inside a thread
    detail_html = make_request(init["url"])
    if not detail_html:
        return init, None
        
    meta = extract_metadata_from_detail(detail_html)
    init_copy = dict(init)
    init_copy["author"] = meta["author"]
    init_copy["group"] = meta["group"]
    init_copy["pub_id"] = meta["pub_id"]
    return init_copy, meta["pub_id"]

def process_publication(pub_id, legislature_str):
    url_pub = f"https://www.congreso.es/busqueda-de-publicaciones?p_p_id=publicaciones&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_publicaciones_mode=mostrarTextoIntegro&_publicaciones_legislatura={legislature_str}&_publicaciones_id_texto=({pub_id}.CODI.)"
    pub_html = make_request(url_pub)
    if pub_html:
        import html
        clean_html = re.sub(r'<script[^>]*?>.*?</script>', '', pub_html, flags=re.DOTALL)
        clean_html = re.sub(r'<style[^>]*?>.*?</style>', '', clean_html, flags=re.DOTALL)
        text = re.sub(r'<[^>]*?>', ' ', clean_html)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text)
        return pub_id, text
    return pub_id, ""

def extract_debate_segment(transcript_text, init_id):
    idx = 0
    occurrences = []
    while True:
        found = transcript_text.find(init_id, idx)
        if found == -1:
            break
        occurrences.append(found)
        idx = found + len(init_id)
        
    if not occurrences:
        return ""
        
    start_idx = occurrences[-1]
    backtrack = 200
    segment_start = max(0, start_idx - backtrack)
    
    text_after = transcript_text[start_idx + len(init_id):]
    
    end_markers = [
        r'Número de expediente \d+/\d+',
        r'expediente \d+/\d+',
        r'Interpelaciones urgentes',
        r'Mociones consecuencia de interpelaciones',
        r'La señora PRESIDENTA:',
        r'El señor PRESIDENTE:'
    ]
    
    min_end = len(text_after)
    max_chars = 12000
    
    for marker in end_markers[:2]:
        matches = list(re.finditer(marker, text_after))
        if matches:
            for m in matches:
                if m.start() > 1500:
                    if m.start() < min_end:
                        min_end = m.start()
                    break
                    
    segment_end_relative = min(min_end, max_chars)
    
    backtracked_text = transcript_text[segment_start:start_idx]
    last_exp = [m.end() for m in re.finditer(r'expediente \d+/\d+|expediente', backtracked_text)]
    if last_exp:
        segment_start = segment_start + last_exp[-1]
        
    return transcript_text[segment_start : start_idx + len(init_id) + segment_end_relative].strip()

def main():
    parser = argparse.ArgumentParser(description="Scrape transcripts for Spain Congress Oral Questions")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of initiatives to process")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads")
    args = parser.parse_args()
    
    list_path = "scratch/initiatives_list.json"
    output_path = "scratch/transcripts_dataset.json"
    
    if not os.path.exists(list_path):
        print(f"Error: {list_path} no existe. Ejecuta scrape_initiatives_list.py primero.")
        return
        
    with open(list_path, "r", encoding="utf-8") as f:
        all_initiatives = json.load(f)
        
    # Filter for debated/answered initiatives
    debated_initiatives = [
        init for init in all_initiatives
        if "caducado" not in init["status"].lower() and "retirado" not in init["status"].lower()
    ]
    
    print(f"Total iniciativas cargadas: {len(all_initiatives)}")
    print(f"Iniciativas de control oral debatidas a procesar: {len(debated_initiatives)}")
    
    if args.limit:
        debated_initiatives = debated_initiatives[:args.limit]
        print(f"Limitando a las primeras {args.limit} iniciativas.")
        
    # Phase 1: Fetch all detail pages in parallel
    print(f"\n--- Fase 1: Descargando páginas de detalle (Hilos: {args.threads}) ---")
    processed_inits = []
    unique_pub_ids = set()
    
    start_time = time.time()
    completed_count = 0
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(process_detail_page, init): init for init in debated_initiatives}
        for future in as_completed(futures):
            init_copy, pub_id = future.result()
            completed_count += 1
            if completed_count % 50 == 0 or completed_count == len(debated_initiatives):
                print(f"  Progreso: {completed_count}/{len(debated_initiatives)} detail pages processed...")
            
            if init_copy:
                processed_inits.append(init_copy)
                if pub_id:
                    unique_pub_ids.add((pub_id, "XIV" if init_copy["legislature"] == 14 else "XV"))
                    
    print(f"Fase 1 completada en {time.time() - start_time:.2f} segundos.")
    print(f"Se encontraron {len(unique_pub_ids)} Diarios de Sesiones (publicaciones) únicos.")
    
    # Phase 2: Fetch unique publication transcripts in parallel
    print(f"\n--- Fase 2: Descargando Diarios de Sesiones (Hilos: 5) ---")
    transcripts_cache = {}
    completed_pubs = 0
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_publication, pub_id, leg): pub_id for pub_id, leg in unique_pub_ids}
        for future in as_completed(futures):
            pub_id, text = future.result()
            transcripts_cache[pub_id] = text
            completed_pubs += 1
            if completed_pubs % 10 == 0 or completed_pubs == len(unique_pub_ids):
                print(f"  Progreso: {completed_pubs}/{len(unique_pub_ids)} Diarios de Sesiones descargados...")
                
    print(f"Fase 2 completada en {time.time() - start_time:.2f} segundos.")
    
    # Phase 3: Segment transcripts for each initiative
    print(f"\n--- Fase 3: Extrayendo segmentos de debate y guardando dataset ---")
    final_dataset = []
    extracted_count = 0
    
    for init in processed_inits:
        pub_id = init.get("pub_id")
        if not pub_id or pub_id not in transcripts_cache:
            init["transcript"] = ""
            final_dataset.append(init)
            continue
            
        transcript_text = transcripts_cache[pub_id]
        if not transcript_text:
            init["transcript"] = ""
            final_dataset.append(init)
            continue
            
        segment = extract_debate_segment(transcript_text, init["id"])
        if segment:
            init["transcript"] = segment
            extracted_count += 1
        else:
            init["transcript"] = ""
            
        final_dataset.append(init)
        
    print(f"Fase 3 completada. Extraídas {extracted_count} transcripciones con éxito de {len(final_dataset)}.")
    
    # Save final dataset
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\nÉxito. Guardadas {len(final_dataset)} iniciativas con transcripción en {output_path}")

if __name__ == "__main__":
    main()

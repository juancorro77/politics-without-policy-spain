import asyncio
import json
import os
import urllib.parse
from playwright.async_api import async_playwright

async def scrape_legislature(page, leg_num):
    print(f"\n--- Iniciando scraping de Legislatura {leg_num} ---")
    url = "https://www.congreso.es/busqueda-de-iniciativas?p_p_id=iniciativas&_iniciativas_statusOpenData=true"
    await page.goto(url, timeout=90000)
    await page.wait_for_load_state("networkidle")
    
    # Accept cookies if visible
    cookie_link = page.locator("a:has-text('Aceptar todas')").first
    if await cookie_link.is_visible():
        await cookie_link.click()
        await page.wait_for_timeout(1000)
        
    # Expand advanced filters
    await page.click("#headingFilter2")
    await page.wait_for_timeout(1000)
    await page.click("#headingExp")
    await page.wait_for_timeout(1000)
    
    # Select Legislature
    await page.select_option("#_iniciativas_legislatura", str(leg_num))
    await page.fill("#_iniciativas_tipo", "Pregunta oral en Pleno")
    
    # Click Buscar
    submit_button = page.locator("button:has-text('Buscar')").first
    if not await submit_button.is_visible():
        print("Botón de búsqueda no encontrado.")
        return []
        
    await submit_button.click()
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)
    
    # Extract total results count
    results_text = await page.inner_text("#_iniciativas_resultsShowedIniciativas")
    print(f"Resultados reportados: {results_text}")
    
    initiatives = []
    page_idx = 1
    
    while True:
        print(f"Procesando página {page_idx}...")
        
        # Extract items on current page
        items = await page.eval_on_selector_all("#_iniciativas_contentPaginationIniciativas ul div", """
            elements => elements.map(el => {
                let a = el.querySelector('h6 a');
                let res = el.querySelector('.resultado');
                let pres = el.querySelector('.presentado');
                return {
                    text: a ? a.innerText.trim() : '',
                    href: a ? a.href : '',
                    resultado: res ? res.innerText.trim() : '',
                    presentado: pres ? pres.innerText.trim() : ''
                };
            }).filter(i => i.text !== '')
        """)
        
        # Parse items to clean them up and extract ID
        page_items_count = 0
        for item in items:
            text = item['text']
            # Remove leading bullet
            if text.startswith("•"):
                text = text[1:].strip()
            
            # Extract ID from text like "... (180/001290)"
            init_id = None
            if "(" in text and ")" in text:
                parts = text.split("(")
                last_part = parts[-1].replace(")", "").strip()
                if "/" in last_part and last_part.split("/")[0] == "180":
                    init_id = last_part
                    # Reconstruct text without ID
                    text = "(".join(parts[:-1]).strip()
            
            # If ID not found in text, try extracting from URL
            if not init_id and item['href']:
                parsed_url = urllib.parse.urlparse(item['href'])
                q_params = urllib.parse.parse_qs(parsed_url.query)
                init_id = q_params.get('_iniciativas_id', [None])[0]
            
            if init_id:
                # Parse presentado date
                pres_date = ""
                if "Presentado el" in item['presentado']:
                    try:
                        pres_date = item['presentado'].split("Presentado el")[1].split("y")[0].strip()
                    except Exception:
                        pass
                
                initiatives.append({
                    "id": init_id,
                    "legislature": leg_num,
                    "question": text,
                    "status": item['resultado'].replace("Resultado tramitación:", "").strip(),
                    "presentado_date": pres_date,
                    "url": item['href']
                })
                page_items_count += 1
                
        print(f"Página {page_idx}: extraídas {page_items_count} iniciativas. Acumulado: {len(initiatives)}")
        
        # Check if next page link is visible and click it
        # The next button is an anchor with text '>' inside the pagination container
        next_button = page.locator("#_iniciativas_paginationLinksIniciativas a:has-text('>')").first
        
        # Verify if next button is active (usually page-link classes, and has some style or is visible)
        # In Liferay, if we are on the last page, the '>' button might be disabled, or we can check if clicking does nothing
        # A simpler check: let's evaluate if there is a next page index select in the list
        # Let's get the selected page number
        current_page_num = await page.eval_on_selector("#_iniciativas_paginationLinksIniciativas a.select", "el => el.innerText.trim()")
        print(f"Página activa actual: {current_page_num}")
        
        # If we can click the next page button, click it
        if await next_button.is_visible():
            # Check if it has the class 'disabled' on parent or click does nothing
            # Let's click it
            await next_button.click()
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(3000)
            
            # Check the new active page
            new_page_num = await page.eval_on_selector("#_iniciativas_paginationLinksIniciativas a.select", "el => el.innerText.trim()")
            if new_page_num == current_page_num:
                print("Hicimos clic en '>' pero la página no cambió. Fin de la legislatura.")
                break
            page_idx += 1
        else:
            print("Botón '>' no visible. Fin de la legislatura.")
            break
            
    return initiatives

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Scrape XIV
            xiv_data = await scrape_legislature(page, 14)
            print(f"Total legislatura XIV: {len(xiv_data)}")
            
            # Scrape XV
            xv_data = await scrape_legislature(page, 15)
            print(f"Total legislatura XV: {len(xv_data)}")
            
            all_data = xiv_data + xv_data
            output_path = "scratch/initiatives_list.json"
            
            # Ensure scratch exists
            os.makedirs("scratch", exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
                
            print(f"\nÉxito. Guardadas {len(all_data)} iniciativas en {output_path}")
            
        except Exception as e:
            print(f"Error general en main: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

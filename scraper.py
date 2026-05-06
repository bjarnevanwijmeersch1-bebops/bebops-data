import requests
import pandas as pd
import json

def scrape_it(url, name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # We proberen alle tabellen van de pagina te lezen
        tables = pd.read_html(url, storage_options=headers)
        
        if tables:
            # De eerste tabel (index 0) is meestal de ranking
            df = tables[0]
            
            # Omzetten naar een lijst van dicts (JSON formaat)
            data_dict = df.to_dict(orient='records')
            
            with open(f"{name}_data.json", "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            print(f"✅ Bestand aangemaakt: {name}_data.json")
        else:
            print(f"❌ Geen tabellen gevonden op {url}")
            
    except Exception as e:
        print(f"⚠️ Fout bij {name}: {e}")

# Jouw ploegen
scrape_it("https://baseballsoftball.be", "D2")
scrape_it("https://baseballsoftball.be", "D3")

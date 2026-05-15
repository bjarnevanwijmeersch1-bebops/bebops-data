import requests
import pandas as pd
import json

def scrape_tables(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Bezig met scrapen van: {url}")
        tables = pd.read_html(url, storage_options=headers)
        
        if not tables:
            print(f"⚠️ Geen tabellen gevonden op {url}")
            return

        for i, df in enumerate(tables):
            if df.empty or len(df.columns) < 3:
                continue
                
            # CRUCIALE STAP: Vervang NaN door lege tekst zodat JSON geldig is
            df_clean = df.fillna("")
            
            data_dict = df_clean.to_dict(orient='records')
            
            filename = f"{name}_{i}.json" if len(tables) > 1 else f"{name}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            print(f"✅ Tabel opgeslagen als: {filename}")

    except Exception as e:
        print(f"⚠️ Fout bij {name}: {e}")

# Je ploegen
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d3-2026/standings", "D3")

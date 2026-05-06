import requests
import pandas as pd
import json

def scrape_tables(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Bezig met scrapen van: {url}")
        # We gebruiken Pandas om alle tabellen op de pagina te zoeken
        tables = pd.read_html(url, storage_options=headers)
        
        if not tables:
            print(f"⚠️ Geen tabellen gevonden op {url}")
            return

        # We lopen door alle gevonden tabellen op de pagina
        for i, df in enumerate(tables):
            # We checken of de tabel wel data bevat (niet leeg is)
            if df.empty or len(df.columns) < 3:
                continue
                
            # Omzetten naar een lijst van dicts
            data_dict = df.to_dict(orient='records')
            
            # Opslaan: als er meer dan 1 tabel is, voegen we het nummer toe
            filename = f"{name}_{i}.json" if len(tables) > 1 else f"{name}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            print(f"✅ Tabel opgeslagen als: {filename}")

    except Exception as e:
        print(f"⚠️ Fout bij {name}: {e}")

# Je ploegen
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d3-2026/standings", "D3")

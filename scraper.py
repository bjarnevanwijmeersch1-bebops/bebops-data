import requests
from bs4 import BeautifulSoup
import json

def scrape_ranking(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zoek de tabel (MyWBSC gebruikt vaak de klasse 'table')
        table = soup.find('table')
        if not table:
            print(f"Geen tabel gevonden op {url}")
            return

        rows = []
        # Loop door de rijen (sla de header over)
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) >= 5:
                team_data = {
                    "rank": cols[0].text.strip(),
                    "team": cols[1].text.strip().replace('\n', ' '),
                    "w": cols[2].text.strip(),
                    "l": cols[3].text.strip(),
                    "pct": cols[5].text.strip() if len(cols) > 5 else cols[4].text.strip()
                }
                rows.append(team_data)
        
        # Opslaan als JSON
        with open(f"{name}_data.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=4, ensure_ascii=False)
        print(f"✅ {name}_data.json succesvol bijgewerkt met echte data.")

    except Exception as e:
        print(f"⚠️ Fout bij {name}: {e}")

# Jouw ploegen
scrape_ranking("https://www.baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")
scrape_ranking("https://www.baseballsoftball.be/en/events/2026-baseball-d3-2026/standings", "D3")

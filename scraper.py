import requests
import json

def scrape_it(url, name):
    # MyWBSC sites laden data via een API. We halen de 'slug' uit jouw URL.
    # Voorbeeld: '2026-baseball-d2-2026'
    slug = url.split('/')[-2]
    api_url = f"https://wbsc.org{slug}/standings"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Origin': 'https://www.baseballsoftball.be'
    }
    
    try:
        print(f"Data ophalen voor {name} via API...")
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        raw_data = response.json()
        standings = []
        
        # We halen de relevante info uit de MyWBSC JSON-structuur
        for team in raw_data.get('standings', []):
            standings.append({
                "rank": team.get('rank'),
                "team": team.get('team_name'),
                "w": team.get('wins'),
                "l": team.get('losses'),
                "pct": team.get('percentage'),
                "logo": team.get('team_logo_url')
            })
            
        with open(f"{name}_data.json", "w", encoding="utf-8") as f:
            json.dump(standings, f, indent=4, ensure_ascii=False)
        print(f"✅ Gelukt: {name}_data.json bevat nu de echte ranking!")

    except Exception as e:
        print(f"⚠️ Fout bij {name}: {e}")

# Je kunt hier simpelweg de URL's van de bond blijven gebruiken
scrape_it("https://www.baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")
scrape_it("https://www.baseballsoftball.be/en/events/2026-baseball-d3-2026/standings", "D3")

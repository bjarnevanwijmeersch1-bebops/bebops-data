import requests
import json

def scrape_all_tables(url, base_name):
    slug = url.split('/')[-2]
    api_url = f"https://wbsc.org{slug}/standings"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Origin': 'https://baseballsoftball.be'
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
        
        # MyWBSC kan data groeperen per 'group' of 'phase'
        # We kijken of er meerdere groepen zijn in de data
        groups = raw_data.get('groups', [])
        
        if not groups:
            # Als er geen groepen zijn, is er maar één tabel (zoals je vorige script)
            save_standings(raw_data.get('standings', []), f"{base_name}_data.json")
        else:
            # Als er meerdere groepen zijn, lopen we erdoorheen
            for group in groups:
                group_name = group.get('group_name', 'Default').replace(' ', '')
                save_standings(group.get('standings', []), f"{base_name}_{group_name}_data.json")
                print(f"✅ Tabel voor {group_name} opgeslagen.")

    except Exception as e:
        print(f"⚠️ Fout bij {base_name}: {e}")

def save_standings(standings_list, filename):
    output = []
    for team in standings_list:
        output.append({
            "rank": team.get('rank'),
            "team": team.get('team_name'),
            "w": team.get('wins'),
            "l": team.get('losses'),
            "pct": team.get('percentage'),
            "logo": team.get('team_logo_url')
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

# Aanroepen voor je competities
scrape_all_tables("https://baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")

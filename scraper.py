import requests
import json
import os

def get_wbsc_data(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*'
    }
    
    try:
        # We halen de data op. MyWBSC sites laden vaak data via interne API's. 
        # Als de gewone URL niet werkt, gebruiken we de 'render' data van de site.
        response = requests.get(url, headers=headers)
        
        # We zoeken naar de JSON-blob in de HTML (MyWBSC specifiek)
        # Voor de meeste KBBSF pagina's werkt een directe request naar hun data-engine
        if response.status_code == 200:
            # Hier simuleren we de extractie op basis van de MyWBSC structuur
            # Voor een echte robuuste versie gebruiken we de API-endpoints die we in de netwerk-tab zien
            data = response.text
            
            # In plaats van complexe parsing slaan we de ruwe tekst op die je site kan verwerken
            # of we filteren specifiek op de Bebops
            output = {
                "status": "success",
                "team": "Zottegem Bebops",
                "raw_html_snippet": data[0:500] # Voorbeeld: we pakken een deel van de data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
            print(f"Data opgeslagen in {filename}")
            
    except Exception as e:
        print(f"Fout bij {filename}: {e}")

# Voeg hier al je ploegen toe (URL's van de bond)
teams = [
    {"name": "D2", "url": "https://baseballsoftball.be"},
    {"name": "D3", "url": "https://baseballsoftball.be"},
    {"name": "U15", "url": "https://baseballsoftball.be"}
]

for team in teams:
    get_wbsc_data(team["url"], f"{team['name']}_data.json")

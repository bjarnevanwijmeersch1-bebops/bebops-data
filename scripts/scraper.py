import requests
import pandas as pd
import json
import os
import re

# Base URL for GitHub Pages images
GITHUB_PAGES_BASE = "https://bjarnevanwijmeersch1-bebops.github.io/bebops-data"

# Get script directory to find images/clubs
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CLUBS_DIR = os.path.join(PROJECT_ROOT, "images", "clubs")
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "rankings")

def get_club_images():
    """Build a mapping of normalized team names to image URLs."""
    club_images = {}
    if os.path.exists(CLUBS_DIR):
        for filename in os.listdir(CLUBS_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Normalize: remove extension, replace underscores with spaces, lowercase
                name_without_ext = os.path.splitext(filename)[0]
                normalized = name_without_ext.replace('_', ' ').lower()
                club_images[normalized] = f"{GITHUB_PAGES_BASE}/images/clubs/{filename}"
    return club_images

def find_team_image(team_name, club_images):
    """Find the matching image for a team name."""
    if not team_name:
        return ""

    # Team.1 format: "CODE  Team Name" (e.g., "GEN  Gent Knights")
    # Remove the 3-letter code and spaces at the start
    match = re.match(r'^[A-Z]{2,4}\s+(.+)$', team_name)
    if match:
        team_name = match.group(1)

    # Remove trailing numbers like "2" for reserve teams
    team_name_base = re.sub(r'\s+\d+$', '', team_name)

    # Special case: Bebops use the main logo
    if 'bebops' in team_name.lower():
        return f"{GITHUB_PAGES_BASE}/images/logo.png"

    # Try exact match first
    normalized = team_name_base.lower()
    if normalized in club_images:
        return club_images[normalized]

    # Try partial matching
    for club_name, image_url in club_images.items():
        # Check if key parts of the name match
        if normalized in club_name or club_name in normalized:
            return image_url
        # Check individual words
        team_words = set(normalized.split())
        club_words = set(club_name.split())
        if team_words & club_words:  # If there's any overlap
            return image_url

    return ""

def scrape_tables(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Load club images mapping
    club_images = get_club_images()

    try:
        print(f"Bezig met scrapen van: {url}")
        tables = pd.read_html(url, storage_options=headers)

        if not tables:
            print(f"[WARN] Geen tabellen gevonden op {url}")
            return

        for i, df in enumerate(tables):
            if df.empty or len(df.columns) < 3:
                continue

            # CRUCIALE STAP: Vervang NaN door lege tekst zodat JSON geldig is
            df_clean = df.fillna("")

            # Only process tables that contain Zottegem Bebops
            if 'Team.1' in df_clean.columns:
                has_bebops = df_clean['Team.1'].str.contains('Zottegem Bebops', case=False, na=False).any()
                if not has_bebops:
                    continue

            data_dict = df_clean.to_dict(orient='records')

            # Add team images based on Team.1
            for record in data_dict:
                team_name = record.get('Team.1', '')
                record['Team'] = find_team_image(team_name, club_images)

            # Ensure data directory exists
            os.makedirs(DATA_DIR, exist_ok=True)

            filename = os.path.join(DATA_DIR, f"{name}.json")

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            print(f"[OK] Tabel opgeslagen als: {filename}")

    except Exception as e:
        print(f"[FOUT] Fout bij {name}: {e}")

# Je ploegen
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d2-2026/standings", "D2")
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-d3-2026/standings", "D3"),
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-u15-2026/standings", "U15"),
scrape_tables("https://www.baseballsoftball.be/en/events/2026-baseball-u12-2026/standings", "U12"),
scrape_tables("https://www.baseballsoftball.be/en/events/2026-softball-ladies-d3/standings", "SD3")

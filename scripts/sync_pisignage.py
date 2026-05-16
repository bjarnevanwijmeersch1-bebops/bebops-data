#!/usr/bin/env python3
"""
Sync sponsor pages to PiSignage via API.
Creates weblink assets for each sponsor and manages a Sponsors playlist.
"""

import json
import os
import re
import requests
from pathlib import Path

# PiSignage API - username is part of the URL
# Format: https://{username}.pisignage.com/api
PISIGNAGE_USERNAME = os.environ.get("PISIGNAGE_USERNAME", "")
PISIGNAGE_API_BASE = f"https://{PISIGNAGE_USERNAME}.pisignage.com/api" if PISIGNAGE_USERNAME else ""

# GitHub CDN base URL for sponsor pages
GITHUB_USER = "bjarnevanwijmeersch1-bebops"
GITHUB_REPO = "bebops-data"
GITHUB_BRANCH = "main"
CDN_BASE_URL = f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{GITHUB_REPO}@{GITHUB_BRANCH}"

# Local paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SPONSORS_HTML_DIR = PROJECT_ROOT / "frames" / "sponsors"

# Playlist name for sponsors
SPONSORS_PLAYLIST = "Sponsors"

# Prefix for sponsor link assets (to identify them)
SPONSOR_ASSET_PREFIX = "sponsor_"

# Duration per sponsor slide (seconds)
SLIDE_DURATION = 8


def get_auth_token() -> str:
    """Get authentication token from PiSignage API."""
    email = os.environ.get("PISIGNAGE_EMAIL", "")
    password = os.environ.get("PISIGNAGE_PASSWORD", "")

    if not PISIGNAGE_USERNAME:
        raise ValueError("PISIGNAGE_USERNAME must be set")

    if not email or not password:
        raise ValueError("PISIGNAGE_EMAIL and PISIGNAGE_PASSWORD must be set")

    url = f"{PISIGNAGE_API_BASE}/session"
    payload = {
        "email": email,
        "password": password,
        "getToken": True
    }
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Authenticating to: {url}")
    response = requests.post(url, json=payload, headers=headers)

    # Debug: print response if failed
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

    response.raise_for_status()
    data = response.json()

    token = data.get("token")
    if not token:
        raise ValueError("Failed to get token from PiSignage API")

    print("Successfully authenticated with PiSignage")
    return token


def get_existing_assets(token: str) -> dict:
    """Get all existing assets from PiSignage."""
    response = requests.get(
        f"{PISIGNAGE_API_BASE}/files",
        params={"token": token}
    )
    response.raise_for_status()
    data = response.json()

    # Return dict of filename -> asset info
    assets = {}
    if "files" in data:
        for f in data["files"]:
            if isinstance(f, dict):
                assets[f.get("name", "")] = f
            elif isinstance(f, str):
                assets[f] = {"name": f}

    return assets


def get_playlist(token: str, playlist_name: str) -> dict:
    """Get playlist details."""
    response = requests.get(
        f"{PISIGNAGE_API_BASE}/playlists/{playlist_name}",
        params={"token": token}
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def create_playlist(token: str, playlist_name: str) -> dict:
    """Create a new playlist."""
    response = requests.post(
        f"{PISIGNAGE_API_BASE}/playlists",
        params={"token": token},
        json={"file": playlist_name}
    )
    response.raise_for_status()
    print(f"Created playlist: {playlist_name}")
    return response.json()


def create_weblink(token: str, name: str, url: str, duration: int = 8) -> dict:
    """Create a weblink asset in PiSignage."""
    response = requests.post(
        f"{PISIGNAGE_API_BASE}/links",
        params={"token": token},
        json={
            "details": {
                "name": name,
                "link": url,
                "duration": duration,
                "type": "link"
            },
            "categories": ["sponsors"]
        }
    )
    response.raise_for_status()
    print(f"Created weblink: {name}")
    return response.json()


def delete_asset(token: str, filename: str) -> bool:
    """Delete an asset from PiSignage."""
    response = requests.delete(
        f"{PISIGNAGE_API_BASE}/files/{filename}",
        params={"token": token}
    )
    if response.status_code == 404:
        return False
    response.raise_for_status()
    print(f"Deleted asset: {filename}")
    return True


def update_playlist_assets(token: str, playlist_name: str, assets: list) -> dict:
    """Update the assets in a playlist."""
    response = requests.post(
        f"{PISIGNAGE_API_BASE}/playlistfiles",
        params={"token": token},
        json={
            "playlist": playlist_name,
            "assets": assets
        }
    )
    response.raise_for_status()
    print(f"Updated playlist {playlist_name} with {len(assets)} assets")
    return response.json()


def get_local_sponsor_pages() -> list:
    """Get list of local sponsor HTML pages."""
    if not SPONSORS_HTML_DIR.exists():
        return []

    pages = []
    for f in sorted(SPONSORS_HTML_DIR.iterdir()):
        if f.is_file() and f.suffix == ".html" and f.stem.startswith("sponsor_"):
            pages.append({
                "filename": f.name,
                "stem": f.stem,
                "url": f"{CDN_BASE_URL}/frames/sponsors/{f.name}"
            })
    return pages


def main():
    """Main sync function."""
    print("Starting PiSignage sync...")

    # Get auth token
    try:
        token = get_auth_token()
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

    # Get local sponsor pages
    local_sponsors = get_local_sponsor_pages()
    print(f"Found {len(local_sponsors)} local sponsor pages")

    if not local_sponsors:
        print("No sponsor pages found, skipping sync")
        return True

    # Get existing assets from PiSignage
    existing_assets = get_existing_assets(token)
    print(f"Found {len(existing_assets)} existing assets in PiSignage")

    # Find existing sponsor assets (by prefix)
    existing_sponsor_assets = {
        name: info for name, info in existing_assets.items()
        if name.startswith(SPONSOR_ASSET_PREFIX)
    }
    print(f"Found {len(existing_sponsor_assets)} existing sponsor assets")

    # Determine what needs to be added/removed
    local_stems = {s["stem"] for s in local_sponsors}
    existing_stems = {name.replace(".link", "").replace(".html", "") for name in existing_sponsor_assets.keys()}

    to_add = local_stems - existing_stems
    to_remove = existing_stems - local_stems

    print(f"Sponsors to add: {len(to_add)}")
    print(f"Sponsors to remove: {len(to_remove)}")

    # Remove old sponsor assets
    for stem in to_remove:
        # Try different possible filenames
        for suffix in [".link", ".html", ""]:
            asset_name = f"{stem}{suffix}"
            if asset_name in existing_assets:
                delete_asset(token, asset_name)
                break

    # Add new sponsor weblinks
    for sponsor in local_sponsors:
        if sponsor["stem"] in to_add:
            link_name = f"{sponsor['stem']}.link"
            create_weblink(token, link_name, sponsor["url"], SLIDE_DURATION)

    # Ensure playlist exists
    playlist = get_playlist(token, SPONSORS_PLAYLIST)
    if not playlist:
        create_playlist(token, SPONSORS_PLAYLIST)

    # Build list of all sponsor asset filenames for playlist
    # Re-fetch assets to get updated list
    updated_assets = get_existing_assets(token)
    sponsor_asset_names = sorted([
        name for name in updated_assets.keys()
        if name.startswith(SPONSOR_ASSET_PREFIX)
    ])

    # Update playlist with all sponsor assets
    if sponsor_asset_names:
        update_playlist_assets(token, SPONSORS_PLAYLIST, sponsor_asset_names)

    print(f"\nSync complete! {len(sponsor_asset_names)} sponsors in playlist")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

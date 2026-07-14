#!/usr/bin/env python3
"""
Sync EK sponsor pages to PiSignage via API.
Creates weblink assets for each EK sponsor and manages a Sponsors-EK playlist.
"""

import imaplib
import email
import json
import os
import re
import time
import requests
from pathlib import Path

# PiSignage API - username is part of the URL
# Format: https://{username}.pisignage.com/api
PISIGNAGE_USERNAME = os.environ.get("PISIGNAGE_USERNAME", "")
PISIGNAGE_API_BASE = f"https://{PISIGNAGE_USERNAME}.pisignage.com/api" if PISIGNAGE_USERNAME else ""

# GitHub Pages base URL for sponsor pages
GITHUB_USER = "bjarnevanwijmeersch1-bebops"
GITHUB_REPO = "bebops-data"
PAGES_BASE_URL = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"

# Local paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SPONSORS_HTML_DIR = PROJECT_ROOT / "frames" / "sponsors-ek"

# Playlist name for EK sponsors
SPONSORS_PLAYLIST = "Bebops-Sponsors-EK"

# Prefix for sponsor link assets (to identify them)
SPONSOR_ASSET_PREFIX = "sponsor_ek_"

# Duration per sponsor slide (seconds)
SLIDE_DURATION = 8

# IMAP settings for reading OTP from email
IMAP_HOST = os.environ.get("IMAP_HOST", "imap.gmail.com")
IMAP_EMAIL = os.environ.get("IMAP_EMAIL", "")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD", "")


def mark_old_otp_emails_as_read():
    """Mark all existing PiSignage OTP emails as read so we only find new ones."""
    if not IMAP_EMAIL or not IMAP_PASSWORD:
        return

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(IMAP_EMAIL, IMAP_PASSWORD)
        mail.select("INBOX")

        # Mark all unread PiSignage emails as read
        _, messages = mail.search(None, '(FROM "pisignage" UNSEEN)')
        email_ids = messages[0].split()

        for email_id in email_ids:
            mail.store(email_id, '+FLAGS', '\\Seen')

        if email_ids:
            print(f"Marked {len(email_ids)} old PiSignage emails as read")

        mail.logout()
    except Exception as e:
        print(f"Warning: Could not mark old emails as read: {e}")


def get_otp_from_email(max_wait: int = 60, check_interval: int = 5) -> str:
    """Read OTP code from email using IMAP. Only finds NEW emails."""
    if not IMAP_EMAIL or not IMAP_PASSWORD:
        raise ValueError("IMAP_EMAIL and IMAP_PASSWORD must be set for OTP retrieval")

    print(f"Connecting to {IMAP_HOST} to retrieve OTP...")
    print("Waiting for new OTP email to arrive...")

    # Give the email a moment to arrive
    time.sleep(3)

    # Connect to IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_EMAIL, IMAP_PASSWORD)
    mail.select("INBOX")

    start_time = time.time()
    otp_code = None

    while time.time() - start_time < max_wait:
        # Search for UNREAD emails from PiSignage
        _, messages = mail.search(None, '(FROM "pisignage" UNSEEN)')
        email_ids = messages[0].split()

        if email_ids:
            # Get the most recent email
            latest_email_id = email_ids[-1]
            _, msg_data = mail.fetch(latest_email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"] or ""

                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                            elif part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                    # Look for OTP code (typically 6 digits)
                    otp_match = re.search(r'\b(\d{6})\b', body)
                    if otp_match:
                        otp_code = otp_match.group(1)
                        print(f"Found OTP code: {otp_code}")

                        # Mark as read
                        mail.store(latest_email_id, '+FLAGS', '\\Seen')
                        break

            if otp_code:
                break

        print(f"Waiting for OTP email... ({int(time.time() - start_time)}s)")
        time.sleep(check_interval)

    mail.logout()

    if not otp_code:
        raise ValueError(f"Could not find OTP code in email after {max_wait} seconds")

    return otp_code


def get_auth_token() -> str:
    """Get authentication token from PiSignage API."""
    pisignage_email = os.environ.get("PISIGNAGE_EMAIL", "")
    password = os.environ.get("PISIGNAGE_PASSWORD", "")

    if not PISIGNAGE_USERNAME:
        raise ValueError("PISIGNAGE_USERNAME must be set")

    if not pisignage_email or not password:
        raise ValueError("PISIGNAGE_EMAIL and PISIGNAGE_PASSWORD must be set")

    # Mark old OTP emails as read BEFORE requesting new OTP
    mark_old_otp_emails_as_read()

    url = f"{PISIGNAGE_API_BASE}/session"
    payload = {
        "email": pisignage_email,
        "password": password,
        "getToken": True
    }
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Authenticating to: {url}")
    response = requests.post(url, json=payload, headers=headers)

    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")

    data = response.json()

    # Check if we got a token (even on 401, sometimes token is included)
    token = data.get("token")

    if response.status_code == 401 and not token:
        # OTP required - try to get it from email or environment
        otp_code = os.environ.get("PISIGNAGE_OTP", "")

        if not otp_code and IMAP_EMAIL and IMAP_PASSWORD:
            print("OTP required. Fetching from email...")
            otp_code = get_otp_from_email()

        if otp_code:
            print(f"Retrying with OTP code...")
            payload["code"] = otp_code
            response = requests.post(url, json=payload, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            data = response.json()
            token = data.get("token")
        else:
            raise ValueError(f"OTP required but no IMAP credentials configured. Message: {data.get('message', 'Unknown')}")

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

    # Files are in data.data.files (list of filenames)
    if "data" in data and "files" in data["data"]:
        for f in data["data"]["files"]:
            if isinstance(f, str):
                assets[f] = {"name": f}

    # Additional info is in data.data.dbdata
    if "data" in data and "dbdata" in data["data"]:
        for item in data["data"]["dbdata"]:
            if isinstance(item, dict) and "name" in item:
                assets[item["name"]] = item

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
    data = response.json()
    print(f"DEBUG: Playlist data: {json.dumps(data, indent=2)[:2000]}")
    return data


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
            "categories": ["sponsors-ek"]
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


def update_playlist_assets(token: str, playlist_name: str, asset_filenames: list, duration: int = 8) -> dict:
    """Update the playlist with assets."""
    # Build assets array with proper object structure
    assets = []
    for filename in asset_filenames:
        assets.append({
            "filename": filename,
            "duration": duration,
            "isVideo": False,
            "selected": True,
            "fullscreen": True,
            "option": {
                "main": True
            }
        })

    payload = {
        "name": playlist_name,
        "assets": assets
    }
    print(f"DEBUG: Updating playlist with {len(assets)} assets")

    response = requests.post(
        f"{PISIGNAGE_API_BASE}/playlists/{playlist_name}",
        params={"token": token},
        json=payload
    )
    print(f"DEBUG: Playlist update response: {response.status_code} - {response.text[:500]}")
    response.raise_for_status()
    print(f"Updated playlist {playlist_name} with {len(assets)} assets")
    return response.json()


def get_local_sponsor_pages() -> list:
    """Get list of local EK sponsor HTML pages."""
    if not SPONSORS_HTML_DIR.exists():
        return []

    pages = []
    for f in sorted(SPONSORS_HTML_DIR.iterdir()):
        if f.is_file() and f.suffix == ".html" and f.stem.startswith("sponsor_"):
            pages.append({
                "filename": f.name,
                "stem": f.stem,
                # Use sponsor_ek_ prefix for the asset name to distinguish from regular sponsors
                "asset_stem": f"sponsor_ek_{f.stem.replace('sponsor_', '')}",
                "url": f"{PAGES_BASE_URL}/frames/sponsors-ek/{f.name}"
            })
    return pages


def main():
    """Main sync function."""
    print("Starting PiSignage EK sponsors sync...")

    # Get auth token
    try:
        token = get_auth_token()
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

    # Get local sponsor pages
    local_sponsors = get_local_sponsor_pages()
    print(f"Found {len(local_sponsors)} local EK sponsor pages")

    if not local_sponsors:
        print("No EK sponsor pages found, skipping sync")
        return True

    # Get existing assets from PiSignage
    existing_assets = get_existing_assets(token)
    print(f"Found {len(existing_assets)} existing assets in PiSignage")

    # Find existing EK sponsor assets (by prefix)
    existing_sponsor_assets = {
        name: info for name, info in existing_assets.items()
        if name.startswith(SPONSOR_ASSET_PREFIX)
    }
    print(f"Found {len(existing_sponsor_assets)} existing EK sponsor assets")

    # Determine what needs to be added/removed
    local_asset_stems = {s["asset_stem"] for s in local_sponsors}
    existing_stems = {name.replace(".link", "").replace(".html", "") for name in existing_sponsor_assets.keys()}

    to_add = local_asset_stems - existing_stems
    to_remove = existing_stems - local_asset_stems

    print(f"EK sponsors to add: {len(to_add)}")
    print(f"EK sponsors to remove: {len(to_remove)}")

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
        if sponsor["asset_stem"] in to_add:
            # Add trailing dot - PiSignage appends "link" to make ".link"
            link_name = f"{sponsor['asset_stem']}."
            create_weblink(token, link_name, sponsor["url"], SLIDE_DURATION)

    # Ensure playlist exists
    playlist = get_playlist(token, SPONSORS_PLAYLIST)
    if not playlist:
        create_playlist(token, SPONSORS_PLAYLIST)

    # Build list of all EK sponsor asset filenames for playlist
    # Re-fetch assets to get updated list
    updated_assets = get_existing_assets(token)
    print(f"\nAll assets in PiSignage: {list(updated_assets.keys())}")

    sponsor_asset_names = sorted([
        name for name in updated_assets.keys()
        if name.startswith(SPONSOR_ASSET_PREFIX)
    ])
    print(f"EK sponsor assets found: {sponsor_asset_names}")

    # Update playlist with all EK sponsor assets
    if sponsor_asset_names:
        update_playlist_assets(token, SPONSORS_PLAYLIST, sponsor_asset_names)

        # Fetch playlist again to verify
        print("\nVerifying playlist contents...")
        get_playlist(token, SPONSORS_PLAYLIST)
    else:
        print("Warning: No EK sponsor assets found to add to playlist")

    print(f"\nSync complete! {len(sponsor_asset_names)} EK sponsors in playlist")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

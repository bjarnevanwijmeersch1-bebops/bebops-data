#!/usr/bin/env python3
"""
Download sponsor images from a shared Google Drive folder.
The folder must be shared with "Anyone with the link can view".
"""

import os
import subprocess
import sys
from pathlib import Path

# Get folder ID from environment variable or use default for testing
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_SPONSORS_FOLDER_ID", "")

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SPONSORS_DIR = PROJECT_ROOT / "images" / "sponsors"

# Supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def install_gdown():
    """Install gdown if not available."""
    try:
        import gdown
        return True
    except ImportError:
        print("Installing gdown...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown", "-q"])
        return True


def download_folder(folder_id: str, output_dir: Path) -> bool:
    """Download all files from a Google Drive folder using gdown."""
    import gdown

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Google Drive folder URL
    url = f"https://drive.google.com/drive/folders/{folder_id}"

    print(f"Downloading from: {url}")
    print(f"Output directory: {output_dir}")

    try:
        # Download entire folder
        gdown.download_folder(
            url=url,
            output=str(output_dir),
            quiet=False,
            use_cookies=False
        )
        return True
    except Exception as e:
        print(f"Error downloading folder: {e}")
        return False


def clean_non_images(directory: Path):
    """Remove non-image files from directory."""
    if not directory.exists():
        return

    for file in directory.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            if ext not in IMAGE_EXTENSIONS:
                print(f"  Removing non-image: {file.name}")
                file.unlink()


def main():
    """Main function to sync sponsors from Google Drive."""
    folder_id = GDRIVE_FOLDER_ID

    if not folder_id:
        folder_id = os.environ.get("GDRIVE_SPONSORS_FOLDER_ID", "")

    if not folder_id:
        print("Error: GDRIVE_SPONSORS_FOLDER_ID not set")
        print("\nTo use this script:")
        print("1. Share your Google Drive folder (Anyone with link can view)")
        print("2. Copy the folder ID from the URL:")
        print("   https://drive.google.com/drive/folders/FOLDER_ID_HERE")
        print("3. Set the environment variable or edit this script")
        return False

    # Install gdown if needed
    install_gdown()

    print(f"\nSyncing sponsors from Google Drive...")
    print(f"Folder ID: {folder_id}\n")

    # Clear existing sponsors (to handle deletions)
    if SPONSORS_DIR.exists():
        print("Clearing existing sponsors folder...")
        for file in SPONSORS_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
                file.unlink()

    # Download from Google Drive
    success = download_folder(folder_id, SPONSORS_DIR)

    if success:
        # Remove any non-image files (like PDFs)
        print("\nCleaning up non-image files...")
        clean_non_images(SPONSORS_DIR)

        # Count images
        images = [f for f in SPONSORS_DIR.iterdir()
                  if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
        print(f"\nSync complete! {len(images)} sponsor images ready")

    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

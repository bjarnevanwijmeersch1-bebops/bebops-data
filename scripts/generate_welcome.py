#!/usr/bin/env python3
"""
Generate welcome pages for visiting clubs.
Each club logo becomes a self-contained HTML welcome page with embedded Base64.
"""

import base64
import re
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
IMAGES_DIR = PROJECT_ROOT / "images"
CLUBS_IMAGES_DIR = IMAGES_DIR / "clubs"
OUTPUT_DIR = PROJECT_ROOT / "frames" / "welcome"
LOGO_PATH = IMAGES_DIR / "logo.png"

# Supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def get_mime_type(extension: str) -> str:
    """Get MIME type for image extension."""
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }
    return mime_types.get(extension.lower(), "image/png")


def image_to_base64(image_path: Path) -> str:
    """Convert image file to Base64 data URL."""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    mime_type = get_mime_type(image_path.suffix)
    return f"data:{mime_type};base64,{data}"


def get_club_name(filename: str) -> str:
    """Extract club name from filename."""
    # Remove extension
    name = Path(filename).stem
    # Replace underscores with spaces
    name = name.replace("_", " ")
    # Clean up multiple spaces
    name = re.sub(r"\s+", " ", name).strip()
    return name


def generate_welcome_html(club_name: str, club_logo_base64: str, bebops_logo_base64: str) -> str:
    """Generate HTML for a welcome page."""
    return f'''<!doctype html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Welkom {club_name} - Bebops Zottegem</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Open+Sans:wght@400;600;700&display=swap"
      rel="stylesheet"
    />
    <style>
      :root {{
        --primary-color: #c41e3a;
        --secondary-color: #ffffff;
        --accent-color: #1a1a1a;
        --text-light: #ffffff;
      }}

      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}

      html,
      body {{
        width: 100%;
        height: 100%;
        overflow: hidden;
        font-family: "Open Sans", sans-serif;
      }}

      .header-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100px;
        background: linear-gradient(135deg, var(--primary-color) 0%, #8b0000 100%);
        display: flex;
        align-items: center;
        padding: 0 50px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 1000;
      }}

      .header-overlay::after {{
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--secondary-color);
      }}

      .logo-container {{
        display: flex;
        align-items: center;
        gap: 25px;
      }}

      .club-logo {{
        height: 70px;
        width: auto;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
      }}

      .club-text {{
        display: flex;
        flex-direction: column;
      }}

      .club-name {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 3rem;
        color: var(--text-light);
        letter-spacing: 3px;
        line-height: 1;
      }}

      .club-subtitle {{
        font-family: "Open Sans", sans-serif;
        font-size: 1.1rem;
        color: var(--secondary-color);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 5px;
        opacity: 0.9;
      }}

      .frame {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 140px 60px 60px 60px;
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
      }}

      .welcome-title {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 4rem;
        color: var(--primary-color);
        text-transform: uppercase;
        letter-spacing: 6px;
        margin-bottom: 20px;
      }}

      .visitor-name {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 3rem;
        color: var(--accent-color);
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 40px;
      }}

      .visitor-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 1;
        width: 100%;
        max-width: 60%;
      }}

      .visitor-logo {{
        max-width: 100%;
        max-height: 45vh;
        object-fit: contain;
        filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.15));
      }}
    </style>
  </head>
  <body>
    <div class="header-overlay">
      <div class="logo-container">
        <img
          src="{bebops_logo_base64}"
          alt="Bebops"
          class="club-logo"
        />
        <div class="club-text">
          <span class="club-name">Bebops</span>
          <span class="club-subtitle">Baseball- & Softballclub</span>
        </div>
      </div>
    </div>

    <div class="frame">
      <div class="welcome-title">Welkom</div>
      <div class="visitor-name">{club_name}</div>
      <div class="visitor-container">
        <img
          src="{club_logo_base64}"
          alt="{club_name}"
          class="visitor-logo"
        />
      </div>
    </div>
  </body>
</html>
'''


def main():
    """Main function to generate all welcome pages."""
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load Bebops logo (or use placeholder)
    if LOGO_PATH.exists():
        bebops_logo_base64 = image_to_base64(LOGO_PATH)
        print(f"Loaded logo: {LOGO_PATH}")
    else:
        # Placeholder SVG
        bebops_logo_base64 = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%23fff'/%3E%3Ctext x='50' y='65' text-anchor='middle' font-size='40' font-family='Arial Black' fill='%23c41e3a'%3EB%3C/text%3E%3C/svg%3E"
        print(f"Warning: Logo not found at {LOGO_PATH}, using placeholder")

    # Check if clubs directory exists
    if not CLUBS_IMAGES_DIR.exists():
        print(f"Creating clubs directory: {CLUBS_IMAGES_DIR}")
        CLUBS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        print("Add club logos to this folder and run the script again.")
        return

    # Get all club images
    club_images = [
        f for f in CLUBS_IMAGES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not club_images:
        print(f"No images found in {CLUBS_IMAGES_DIR}")
        print(f"Supported formats: {', '.join(IMAGE_EXTENSIONS)}")
        return

    print(f"Found {len(club_images)} club logos")

    # Generate HTML for each club
    generated_files = []
    for image_path in sorted(club_images):
        club_name = get_club_name(image_path.name)
        club_logo_base64 = image_to_base64(image_path)

        # Create safe filename
        safe_filename = re.sub(r"[^a-zA-Z0-9_-]", "_", image_path.stem)
        output_file = OUTPUT_DIR / f"welcome_{safe_filename}.html"

        html_content = generate_welcome_html(club_name, club_logo_base64, bebops_logo_base64)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated_files.append(output_file.name)
        print(f"Generated: {output_file.name} ({club_name})")

    # Clean up old HTML files that no longer have club images
    generated_filenames = set(generated_files)
    for html_file in OUTPUT_DIR.iterdir():
        if html_file.is_file() and html_file.suffix == ".html":
            if html_file.name not in generated_filenames:
                print(f"Removing old welcome page: {html_file.name}")
                html_file.unlink()

    print(f"\nDone! Generated {len(generated_files)} welcome pages")


if __name__ == "__main__":
    main()

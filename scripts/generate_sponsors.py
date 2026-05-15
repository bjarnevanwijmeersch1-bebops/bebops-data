#!/usr/bin/env python3
"""
Generate sponsor HTML pages from images in the sponsors folder.
Each image becomes a self-contained HTML page with embedded Base64.
"""

import base64
import os
import re
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
IMAGES_DIR = PROJECT_ROOT / "images"
SPONSORS_IMAGES_DIR = IMAGES_DIR / "sponsors"
OUTPUT_DIR = PROJECT_ROOT / "frames" / "sponsors"
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


def get_sponsor_name(filename: str) -> str:
    """Extract sponsor name from filename."""
    # Remove extension
    name = Path(filename).stem
    # Remove common suffixes like (1), (2), etc.
    name = re.sub(r"\s*\(\d+\)\s*$", "", name)
    # Remove dimension patterns like 25x80mm, 1200x600, 625x625
    name = re.sub(r"\s*\d+x\d+(?:mm|cm|px)?\s*", " ", name, flags=re.IGNORECASE)
    # Remove page indicators like page-0001
    name = re.sub(r"\s*page[-_]?\d+\s*", "", name, flags=re.IGNORECASE)
    # Remove common file artifacts
    name = re.sub(r"\s*[-_]?(logo|rgb|ic|bord)\s*", " ", name, flags=re.IGNORECASE)
    # Replace underscores and hyphens with spaces
    name = re.sub(r"[-_]+", " ", name)
    # Clean up multiple spaces
    name = re.sub(r"\s+", " ", name).strip()
    # Title case
    return name.title()


def generate_sponsor_html(sponsor_name: str, sponsor_image_base64: str, logo_base64: str) -> str:
    """Generate HTML for a sponsor page."""
    return f'''<!doctype html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{sponsor_name} - Bebops Zottegem</title>
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

      .section-title {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 2.5rem;
        color: var(--primary-color);
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 40px;
      }}

      .sponsor-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 1;
        width: 100%;
        max-width: 80%;
      }}

      .sponsor-image {{
        max-width: 100%;
        max-height: 55vh;
        object-fit: contain;
        filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.1));
      }}
    </style>
  </head>
  <body>
    <div class="header-overlay">
      <div class="logo-container">
        <img
          src="{logo_base64}"
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
      <div class="section-title">Met dank aan onze Sponsor</div>
      <div class="sponsor-container">
        <img
          src="{sponsor_image_base64}"
          alt="{sponsor_name}"
          class="sponsor-image"
        />
      </div>
    </div>
  </body>
</html>
'''


def generate_carousel_html(sponsors: list, logo_base64: str, slide_duration: int = 8) -> str:
    """Generate a single HTML file that cycles through all sponsors."""
    sponsors_json = ",\n        ".join([
        f'{{ name: "{s["name"]}", image: "{s["image"]}" }}'
        for s in sponsors
    ])

    return f'''<!doctype html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sponsors - Bebops Zottegem</title>
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
        --slide-duration: {slide_duration}s;
      }}

      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}

      html, body {{
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
        padding: 140px 60px 80px 60px;
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
      }}

      .section-title {{
        font-family: "Bebas Neue", sans-serif;
        font-size: 2.5rem;
        color: var(--primary-color);
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 40px;
      }}

      .sponsor-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 1;
        width: 100%;
        max-width: 80%;
        position: relative;
      }}

      .sponsor-slide {{
        position: absolute;
        opacity: 0;
        transition: opacity 0.8s ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
      }}

      .sponsor-slide.active {{
        opacity: 1;
      }}

      .sponsor-image {{
        max-width: 100%;
        max-height: 55vh;
        object-fit: contain;
        filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.1));
      }}

      /* Progress bar */
      .progress-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: rgba(0, 0, 0, 0.1);
        z-index: 1000;
      }}

      .progress-bar {{
        height: 100%;
        background: var(--primary-color);
        width: 0%;
        animation: progress var(--slide-duration) linear infinite;
      }}

      @keyframes progress {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
      }}

      /* Slide counter */
      .slide-counter {{
        position: fixed;
        bottom: 20px;
        right: 30px;
        font-family: "Bebas Neue", sans-serif;
        font-size: 1.2rem;
        color: var(--accent-color);
        opacity: 0.5;
      }}
    </style>
  </head>
  <body>
    <div class="header-overlay">
      <div class="logo-container">
        <img src="{logo_base64}" alt="Bebops" class="club-logo" />
        <div class="club-text">
          <span class="club-name">Bebops</span>
          <span class="club-subtitle">Baseball- & Softballclub</span>
        </div>
      </div>
    </div>

    <div class="frame">
      <div class="section-title">Met dank aan onze Sponsors</div>
      <div class="sponsor-container" id="sponsorContainer"></div>
    </div>

    <div class="progress-container">
      <div class="progress-bar" id="progressBar"></div>
    </div>

    <div class="slide-counter" id="slideCounter"></div>

    <script>
      const sponsors = [
        {sponsors_json}
      ];

      let currentIndex = 0;
      const container = document.getElementById('sponsorContainer');
      const counter = document.getElementById('slideCounter');
      const progressBar = document.getElementById('progressBar');
      const slideDuration = {slide_duration} * 1000;

      // Create slides
      sponsors.forEach((sponsor, index) => {{
        const slide = document.createElement('div');
        slide.className = 'sponsor-slide' + (index === 0 ? ' active' : '');
        slide.innerHTML = `<img src="${{sponsor.image}}" alt="${{sponsor.name}}" class="sponsor-image">`;
        container.appendChild(slide);
      }});

      function updateCounter() {{
        counter.textContent = `${{currentIndex + 1}} / ${{sponsors.length}}`;
      }}

      function nextSlide() {{
        const slides = document.querySelectorAll('.sponsor-slide');
        slides[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % sponsors.length;
        slides[currentIndex].classList.add('active');
        updateCounter();

        // Reset progress bar animation
        progressBar.style.animation = 'none';
        progressBar.offsetHeight; // Trigger reflow
        progressBar.style.animation = `progress ${{slideDuration/1000}}s linear infinite`;
      }}

      updateCounter();
      setInterval(nextSlide, slideDuration);
    </script>
  </body>
</html>
'''


def main():
    """Main function to generate all sponsor pages."""
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load logo (or use placeholder)
    if LOGO_PATH.exists():
        logo_base64 = image_to_base64(LOGO_PATH)
        print(f"Loaded logo: {LOGO_PATH}")
    else:
        # Placeholder SVG
        logo_base64 = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%23fff'/%3E%3Ctext x='50' y='65' text-anchor='middle' font-size='40' font-family='Arial Black' fill='%23c41e3a'%3EB%3C/text%3E%3C/svg%3E"
        print(f"Warning: Logo not found at {LOGO_PATH}, using placeholder")

    # Check if sponsors directory exists
    if not SPONSORS_IMAGES_DIR.exists():
        print(f"Creating sponsors directory: {SPONSORS_IMAGES_DIR}")
        SPONSORS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        print("Add sponsor images to this folder and run the script again.")
        return

    # Get all sponsor images
    sponsor_images = [
        f for f in SPONSORS_IMAGES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not sponsor_images:
        print(f"No images found in {SPONSORS_IMAGES_DIR}")
        print(f"Supported formats: {', '.join(IMAGE_EXTENSIONS)}")
        return

    print(f"Found {len(sponsor_images)} sponsor images")

    # Collect all sponsors for carousel
    all_sponsors = []

    # Generate HTML for each sponsor
    generated_files = []
    for image_path in sorted(sponsor_images):
        sponsor_name = get_sponsor_name(image_path.name)
        sponsor_base64 = image_to_base64(image_path)

        # Add to carousel list
        all_sponsors.append({
            "name": sponsor_name,
            "image": sponsor_base64
        })

        # Create safe filename
        safe_filename = re.sub(r"[^a-zA-Z0-9_-]", "_", image_path.stem)
        output_file = OUTPUT_DIR / f"sponsor_{safe_filename}.html"

        html_content = generate_sponsor_html(sponsor_name, sponsor_base64, logo_base64)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated_files.append(output_file.name)
        print(f"Generated: {output_file.name} ({sponsor_name})")

    # Generate carousel HTML with all sponsors
    carousel_file = PROJECT_ROOT / "frames" / "sponsors_carousel.html"
    carousel_html = generate_carousel_html(all_sponsors, logo_base64, slide_duration=8)
    with open(carousel_file, "w", encoding="utf-8") as f:
        f.write(carousel_html)
    print(f"\nGenerated: sponsors_carousel.html (all {len(all_sponsors)} sponsors in one file)")

    print(f"\nDone! Generated {len(generated_files)} individual pages + 1 carousel in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

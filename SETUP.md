# Bebops Overlay - Setup Guide

## For the Non-Technical Person (Sponsor Manager)

### Managing Sponsor Images

1. **Open the shared Google Drive folder** (you'll receive a link)
2. **To add a sponsor:** Drag & drop the image into the folder
3. **To remove a sponsor:** Right-click the image → "Remove"
4. **That's it!** The TV display updates automatically every Sunday

### Image Requirements
- Formats: PNG, JPG, GIF (PNG recommended for logos)
- Name the file after the sponsor (e.g., `Brouwerij Roman.png`)
- Use clean, high-resolution images

---

## For the Technical Person (Initial Setup)

### Step 1: Create Google Drive Folder

1. Go to [Google Drive](https://drive.google.com)
2. Create a new folder called `Bebops Sponsors`
3. Right-click the folder → "Share"
4. Click "Change to anyone with the link"
5. Set permission to "Viewer"
6. Copy the folder link

The link looks like:
```
https://drive.google.com/drive/folders/1ABC123xyz...
```
The folder ID is the part after `/folders/`: `1ABC123xyz...`

### Step 2: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `GDRIVE_SPONSORS_FOLDER_ID` | Folder ID from Step 1 |
| `PISIGNAGE_EMAIL` | Your PiSignage login email |
| `PISIGNAGE_PASSWORD` | Your PiSignage password |

### Step 3: Upload Club Logo

Make sure `images/logo.png` exists in the repository with your club logo.

### Step 4: Test the Workflow

1. Go to **Actions** tab in GitHub
2. Click **Generate Sponsor Pages**
3. Click **Run workflow** → **Run workflow**
4. Wait for it to complete
5. Check `frames/sponsors_carousel.html` was generated

### Step 5: Set Up PiSignage

The workflow automatically syncs sponsors to PiSignage via API:

1. A "Sponsors" playlist is created automatically
2. Each sponsor becomes a weblink asset (8 seconds each)
3. When sponsors change, the playlist updates automatically

**Manual setup in PiSignage:**
1. Add the "Sponsors" playlist to your display rotation
2. The playlist contains individual sponsor pages that PiSignage manages

---

## How It Works

```
┌─────────────────────┐
│   Google Drive      │
│   Sponsors Folder   │
│  (drag & drop)      │
└─────────┬───────────┘
          │
          │ Every Sunday 6:00 AM
          ▼
┌─────────────────────┐
│   GitHub Actions    │
│  - Download images  │
│  - Generate HTML    │
│  - Commit changes   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ sponsors_carousel   │
│      .html          │
│  (upload to         │
│   PiSignage)        │
└─────────────────────┘
```

## Manual Update

To update immediately (not wait for Sunday):
1. Go to GitHub → Actions
2. Click "Generate Sponsor Pages"
3. Click "Run workflow"

## Files Generated

| File | Description |
|------|-------------|
| `frames/sponsors_carousel.html` | **Upload this to PiSignage** - cycles through all sponsors |
| `frames/sponsors/sponsor_*.html` | Individual pages (optional use) |

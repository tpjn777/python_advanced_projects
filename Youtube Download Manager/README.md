# YouTube Download Manager

A simple desktop app for downloading YouTube videos, built with Python, Tkinter and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Features

- Fetch video title, author and duration from a URL
- Choose quality: best available, any specific resolution, or audio only
- Merges separate video and audio streams for 1080p and above (requires ffmpeg)
- Audio-only download converted to MP3 (requires ffmpeg)
- Choose the download folder
- Live progress bar with a Cancel button
- Single-video downloads only (playlist links download just the linked video)

## Requirements

- Python 3.8 or newer (Tkinter is included with most Python installers)
- [yt-dlp](https://pypi.org/project/yt-dlp/)
- [ffmpeg](https://ffmpeg.org/download.html) (optional, but recommended)

### Without ffmpeg

The app still works, but:

- Quality is limited to pre-merged streams (usually up to 720p)
- Audio-only downloads keep the original format (e.g. `.m4a` or `.webm`) instead of MP3

## Installation

```bash
pip install yt-dlp
```

Install ffmpeg and make sure it is on your PATH. You can check with:

```bash
ffmpeg -version
```

Common ways to install it:

| System  | Command                         |
|---------|---------------------------------|
| Windows | `winget install ffmpeg`         |
| macOS   | `brew install ffmpeg`           |
| Ubuntu  | `sudo apt install ffmpeg`       |

On some Linux distributions you also need Tkinter: `sudo apt install python3-tk`.

## Usage

```bash
python youtube_download_manager.py
```

1. Paste a YouTube video URL.
2. Click **Fetch Video Information** (or press Enter).
3. Pick a quality from the dropdown.
4. Optionally click **Browse** to change the download folder (default: your `Downloads` folder).
5. Click **DOWNLOAD**. Use **CANCEL** to stop.

## Troubleshooting

**Fetch fails or downloads stop working**
YouTube changes often. Update yt-dlp first:

```bash
pip install -U yt-dlp
```

**Only low qualities are listed**
ffmpeg is probably missing or not on your PATH. Install it and restart the app.

**"Sign in to confirm you're not a bot" or age-restricted videos**
These can require a logged-in session, which this app does not support.

**`ModuleNotFoundError: No module named 'yt_dlp'`**
Run `pip install yt-dlp` using the same Python that launches the app.

## Legal notice

Downloading videos from YouTube may violate its Terms of Service. Only download content you own, that is in the public domain or under a license that allows it, or that you otherwise have permission to download. You are responsible for how you use this tool.
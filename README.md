# MediaDownloader

**MediaDownloader** is a simple, clean tool to download videos or extract audio (MP3) from online platforms like Facebook and YouTube, using `yt-dlp`.  
It supports selecting video quality, downloading audio directly, and saving files into a specified directory.

---

## Features
- 🎥 Download videos in your preferred quality (e.g.,720p, 480p, 360p).
- 🎵 Download and convert videos to MP3 audio.
- 📂 Save downloads automatically into a specified folder.
- 🔥 Supports Facebook, YouTube, and other platforms via `yt-dlp`.
- 🟡 Clean filename handling (illegal characters removed).

---

## Requirements
- Python 3.7+
- `yt-dlp`
- `ffmpeg` (for audio extraction)

## Installation
### Virtual Environment Setup
```cmd
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

# Install ffmpeg ( Debian/Ubuntu) Or download from https://ffmpeg.org/:
sudo apt install ffmpeg
```

## Usage
Run the script:
```bash
python downloader.py
```

## Example:
```text
Enter the video URL:
Choose media type (video/audio) [video]:
Choose quality (best/worst/720/480/360) [best]:
```

---

## Notes
+ Some URLs may not be downloadable due to platform restrictions or private settings.
+ ffmpeg is mandatory if you want to extract audio (MP3).
+ Only supports single video downloads (no playlist downloads).
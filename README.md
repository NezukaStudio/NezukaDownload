# Nezuka Video Downloader 3.0

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A powerful command-line tool to download videos and audio from TikTok, YouTube, Instagram, Facebook, Twitter, and more.

## Features

- 🎥 Download videos from 10+ platforms
- 🎵 Extract audio (MP3) with album art support
- 📊 Track user profiles (followers, stats, bio)
- 🌐 Multi-language support (7 languages)
- 🎨 Customizable colors (6 themes)
- 📁 Downloads directly to storage

## Supported Platforms

| Platform | Download | Tracker |
|----------|----------|---------|
| TikTok | ✅ | ✅ |
| YouTube | ✅ | ✅ |
| Instagram | ✅ | ✅ |
| Facebook | ✅ | ✅ |
| Twitter / X | ✅ | ✅ |
| CapCut | ✅ | ❌ |
| Snack Video | ✅ | ✅ |
| Doodstream | ✅ | ❌ |
| Pinterest | ✅ | ❌ |

## Installation

### Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python ffmpeg
pip install yt-dlp requests
git clone https://github.com/NezukaStudio/NezukaDownload.git
cd NezukaDownload
python main.py
```

Linux / macOS

```bash
# Install Python 3.10+, then:
pip install yt-dlp requests
git clone https://github.com/NezukaStudio/NezukaDownload.git
cd NezukaDownload
python main.py
```

Windows

```bash
pip install yt-dlp requests
git clone https://github.com/NezukaStudio/NezukaDownload.git
cd NezukaDownload
python main.py
```

Usage

Run without arguments to start interactive mode:

```bash
python main.py
```

Main Menu

· 1 - Downloader (download videos/audio)
· 2 - Tracker (view user profiles)
· 3 - Settings (change language & color)
· 4 - About (version info)
· 0 - Exit

Download Video

1. Select 1 from main menu
2. Choose platform (TikTok, YouTube, etc.)
3. Paste video URL
4. Choose format:
   · 1 = MP4 (video)
   · 2 = MP3 (audio only)
   · 3 = MP3 + Album Art (YouTube only)
5. Wait for download

Track Profile

1. Select 2 from main menu
2. Choose platform
3. Select 1 for Lookup (by username/handle)
4. Enter username without @

Search Users

1. Select 2 from main menu
2. Choose platform
3. Select 2 for Search
4. Enter keyword

Change Language

1. Select 3 (Settings)
2. Select 1 (Language)
3. Choose: English, Indonesia, 中文, हिन्दी, 日本語, 한국어, Русский

Change Color

1. Select 3 (Settings)
2. Select 2 (Primary Color)
3. Choose: Pink, Red, Green, Purple, Blue, Orange

Configuration File

Settings saved in /storage/emulated/0/nezuka_config.json (Android) or ./nezuka_config.json (others):

```json
{
  "language": "indonesia",
  "primary_color": "pink"
}
```

Custom API (Optional)

Edit secret_api.py:

```python
TIKWM_API = "https://your-custom-api.com/"
TIKTOK_API_URL = "https://your-custom-api.com/"
```

Requirements

· Python 3.10 or higher
· FFmpeg (for MP3 conversion)
· yt-dlp
· requests

Download Location

· Android: /storage/emulated/0/Download/
· Other: Current working directory

Troubleshooting

yt-dlp not found

```bash
pip install yt-dlp
```

FFmpeg not found

```bash
# Termux
pkg install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org
```

TikTok API error

Edit secret_api.py and change API endpoint, or try again later.

Detected dubious ownership in Termux

```bash
git config --global --add safe.directory /storage/emulated/0/Nezuka
```

Permission denied

```bash
termux-setup-storage
```

Building Binary

```bash
pip install pyinstaller
pyinstaller --onefile --name nezuka main.py
```

File Structure

```
NezukaDownload/
├── main.py              # Main script
├── language.json        # Translations (7 languages)
├── secret_api.py        # API configuration
├── nezuka_config.json   # User settings
└── README.md           # Documentation
```

License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

```
Copyright 2025 NezukaStudio

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Credits

· Developer: Nezuka
· Version: 3.0
· API: TikWM API
· Downloader: yt-dlp

Support

· GitHub Issues: https://github.com/NezukaStudio/NezukaDownload/issues
· Repository: https://github.com/NezukaStudio/NezukaDownload

---

⭐ Star this repository if you find it useful!
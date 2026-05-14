import requests
import os
import re
import subprocess
import sys
import json
import time
import threading
import shutil

try:
    from secret_api import TIKWM_API, TIKTOK_API_URL
except ImportError:
    TIKWM_API = "https://www.tikwm.com/api/"
    TIKTOK_API_URL = "https://www.tikwm.com/api/"

CONFIG_FILE = "/storage/emulated/0/Nezuka/nezuka_config.json"
LANG_FILE = "/storage/emulated/0/Nezuka/language.json"

config = {
    "language": "indonesia",
    "primary_color": "pink"
}

COLORS = {
    "pink": {"main": "\033[38;5;213m", "sec": "\033[38;5;205m"},
    "red": {"main": "\033[38;5;196m", "sec": "\033[38;5;203m"},
    "green": {"main": "\033[38;5;46m", "sec": "\033[38;5;120m"},
    "purple": {"main": "\033[38;5;129m", "sec": "\033[38;5;141m"},
    "blue": {"main": "\033[38;5;39m", "sec": "\033[38;5;45m"},
    "orange": {"main": "\033[38;5;214m", "sec": "\033[38;5;208m"}
}

TEXTS = {}

def load_languages():
    global TEXTS
    try:
        if os.path.exists(LANG_FILE):
            with open(LANG_FILE, 'r', encoding='utf-8') as f:
                TEXTS = json.load(f)
        else:
            print(f"Language file not found at {LANG_FILE}")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading language file: {e}")
        sys.exit(1)

def load_config():
    global config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                saved = json.load(f)
                config.update(saved)
    except:
        pass

def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

def t(key):
    lang = config["language"]
    if lang in TEXTS and key in TEXTS[lang]:
        return TEXTS[lang][key]
    for l in TEXTS:
        if key in TEXTS[l]:
            return TEXTS[l][key]
    return key

def get_colors():
    col = COLORS.get(config["primary_color"], COLORS["pink"])
    return col["main"], col["sec"]

PINK, PINK2 = get_colors()
WHITE  = "\033[97m"
GRAY   = "\033[38;5;245m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[38;5;203m"
GREEN  = "\033[38;5;120m"

def refresh_colors():
    global PINK, PINK2
    PINK, PINK2 = get_colors()

DOWNLOAD_DIR = "/storage/emulated/0/Download"

def get_dl_dir():
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        return DOWNLOAD_DIR
    except Exception:
        return os.getcwd()

def term_width():
    return min(shutil.get_terminal_size((60, 20)).columns, 80)

def divider():
    print(f"  {PINK}{'─' * (term_width() - 4)}{RESET}")

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def banner():
    w = term_width()
    print()
    if w >= 56:
        print(f"  {PINK}{BOLD}███╗   ██╗███████╗███████╗██╗   ██╗██╗  ██╗ █████╗{RESET}")
        print(f"  {PINK}{BOLD}████╗  ██║██╔════╝╚══███╔╝██║   ██║██║ ██╔╝██╔══██╗{RESET}")
        print(f"  {PINK}{BOLD}██╔██╗ ██║█████╗    ███╔╝ ██║   ██║█████╔╝ ███████║{RESET}")
        print(f"  {PINK}{BOLD}██║╚██╗██║██╔══╝   ███╔╝  ██║   ██║██╔═██╗ ██╔══██║{RESET}")
        print(f"  {PINK}{BOLD}██║ ╚████║███████╗███████╗╚██████╔╝██║  ██╗██║  ██║{RESET}")
        print(f"  {PINK}{BOLD}╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝{RESET}")
    else:
        print(f"  {PINK}{BOLD}{t('app_name')}{RESET}")
    print()
    print(f"  {WHITE}{BOLD}{t('subtitle')}{RESET}  {GRAY}{t('version')}{RESET}")
    divider()
    print()

def log_info(msg):  print(f"  {PINK}[*]{RESET} {WHITE}{msg}{RESET}")
def log_ok(msg):    print(f"  {GREEN}[✓]{RESET} {WHITE}{msg}{RESET}")
def log_err(msg):   print(f"  {RED}[!]{RESET} {WHITE}{msg}{RESET}")
def prompt(msg):    return input(f"  {PINK}›{RESET} {WHITE}{msg}:{RESET} ").strip()

def section_header(title):
    clear(); banner()
    print(f"  {PINK2}{BOLD}  {title}{RESET}")
    divider(); print()

def show_info(fields):
    w = term_width() - 4
    for label, value in fields:
        val = str(value)
        if len(val) > w - 14:
            val = val[:w - 15] + "…"
        print(f"  {GRAY}{label:<11}{RESET}{WHITE}{val}{RESET}")
    print()

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)[:60].strip()

def check_ytdlp():
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False

class ProgressSpinner:
    def __init__(self, label=None):
        self.label = label or t("downloading")
        self.stop = False
        self.thread = None
    
    def start(self):
        self.stop = False
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
    
    def _spin(self):
        frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while not self.stop:
            print(f"\r  {PINK}{frames[i % len(frames)]}{RESET} {WHITE}{self.label}...{RESET}   ", end="", flush=True)
            time.sleep(0.08)
            i += 1
        print(f"\r  {GREEN}✓{RESET} {WHITE}{self.label} done{RESET}              ")
    
    def stop_spinner(self):
        self.stop = True
        if self.thread:
            self.thread.join()

def progress_bar(downloaded, total):
    w = max(min(term_width() - 32, 28), 10)
    mb_down = downloaded / (1024 * 1024)
    if total > 0:
        pct = downloaded / total
        filled = int(w * pct)
        bar = "█" * filled + "░" * (w - filled)
        mb_tot = total / (1024 * 1024)
        print(f"\r  {PINK}[{PINK2}{bar}{PINK}]{RESET} {WHITE}{pct*100:5.1f}%{RESET} {GRAY}{mb_down:.1f}/{mb_tot:.1f} MB{RESET}  ", end="", flush=True)
    else:
        print(f"\r  {PINK}⣿{RESET} {WHITE}{t('downloading')}...{RESET} {GRAY}{mb_down:.1f} MB{RESET}  ", end="", flush=True)

def download_file_with_progress(url, filename, ext):
    dl_dir = get_dl_dir()
    filepath = os.path.join(dl_dir, f"{filename}.{ext}")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, stream=True, timeout=60)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        print()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_bar(downloaded, total)
        print()
        log_ok(f"{t('saved')}  →  {filepath}")
        return True
    except requests.exceptions.ConnectionError:
        print(); log_err(t("no_internet"))
    except requests.exceptions.Timeout:
        print(); log_err(t("timeout"))
    except Exception as e:
        print(); log_err(f"{t('download_failed')}: {e}")
    return False

def download_ytdlp_with_progress(url, filename, fmt, embed_meta=False):
    dl_dir = get_dl_dir()
    out = os.path.join(dl_dir, f"{filename}.%(ext)s")
    try:
        if fmt == "mp3":
            cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
                   "--add-metadata", "--no-keep-video", "--clean-info-json",
                   "--postprocessor-args", "ffmpeg:-id3v2_version 3"]
            if embed_meta:
                cmd += ["--write-thumbnail", "--convert-thumbnails", "jpg"]
            cmd += ["-o", out, url]
        else:
            cmd = ["yt-dlp",
                   "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                   "--merge-output-format", "mp4",
                   "-o", out, url]

        print()
        spinner = ProgressSpinner(t("downloading"))
        spinner.start()
        res = subprocess.run(cmd, capture_output=True, text=True)
        spinner.stop_spinner()

        if res.returncode != 0:
            log_err(f"{t('download_failed')}:")
            print(f"  {GRAY}{(res.stderr or res.stdout)[-500:]}{RESET}")
            return False

        if embed_meta and fmt == "mp3":
            mp3 = os.path.join(dl_dir, f"{filename}.mp3")
            thumb = os.path.join(dl_dir, f"{filename}.jpg")
            if os.path.exists(thumb) and os.path.exists(mp3):
                log_info("Processing cover art...")
                crop = os.path.join(dl_dir, f"{filename}_crop.jpg")
                tmp = os.path.join(dl_dir, f"{filename}_tmp.mp3")
                subprocess.run(["ffmpeg", "-y", "-i", thumb,
                                 "-vf", "crop='min(iw,ih)':'min(iw,ih)'",
                                 crop], capture_output=True)
                subprocess.run(["ffmpeg", "-y", "-i", mp3, "-i", crop,
                                 "-map", "0", "-map", "1", "-c", "copy",
                                 "-id3v2_version", "3",
                                 "-metadata:s:v", "title=Album cover",
                                 "-metadata:s:v", "comment=Cover (front)",
                                 tmp], capture_output=True)
                if os.path.exists(tmp):
                    os.replace(tmp, mp3)
                for f in [thumb, crop]:
                    if os.path.exists(f): os.remove(f)

        ext = "mp3" if fmt == "mp3" else "mp4"
        log_ok(f"{t('saved')}  →  {os.path.join(dl_dir, filename)}.{ext}")
        return True
    except FileNotFoundError:
        log_err("yt-dlp not found. Run: pip install yt-dlp")
    except Exception as e:
        log_err(f"{t('error')}: {e}")
    return False

def pick_format(with_album=False):
    print(f"  {PINK}[1]{RESET} {WHITE}{t('mp4')}{RESET}")
    print(f"  {PINK}[2]{RESET} {WHITE}{t('mp3')}{RESET}")
    if with_album:
        print(f"  {PINK}[3]{RESET} {WHITE}{t('mp3_album')}{RESET}")
    print()
    while True:
        c = prompt(t("format_prompt"))
        if c == "1": return "mp4", False
        if c == "2": return "mp3", False
        if c == "3" and with_album: return "mp3", True
        log_err(f"{t('invalid_format')} 1, 2" + (", 3." if with_album else "."))

def flow_tiktok():
    section_header(f"{t('menu_downloader')}  ›  TikTok")
    url = prompt(f"TikTok URL  ({t('back')})")
    if url.lower() == "back": return
    if "tiktok.com" not in url:
        log_err("Invalid URL. Must be from tiktok.com"); return

    log_info(f"{t('fetching_info')}...")
    try:
        r = requests.post(TIKWM_API, data={"url": url, "hd": 1}, timeout=15)
        data = r.json()
        if data.get("code") != 0:
            log_err(f"API error: {data.get('msg', 'unknown')}"); return
        inf = data.get("data", {})
    except requests.exceptions.ConnectionError:
        log_err(t("no_internet")); return
    except requests.exceptions.Timeout:
        log_err(t("timeout")); return
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    author = inf.get("author", {})
    username = author.get("unique_id", "unknown")
    nickname = author.get("nickname", username)
    desc = inf.get("title", "video")
    filename = sanitize(f"{username}_{desc}")

    print()
    show_info([
        (t("account"),  f"@{username}  ({nickname})"),
        (t("title"),    desc),
        (t("views"),    f"{inf.get('play_count', 0):,}"),
        (t("likes"),    f"{inf.get('digg_count', 0):,}"),
        (t("comments"), f"{inf.get('comment_count', 0):,}"),
    ])

    fmt, _ = pick_format()
    if fmt == "mp3":
        audio_url = inf.get("music")
        if not audio_url: log_err("Audio URL not found."); return
        download_file_with_progress(audio_url, filename, "mp3")
    else:
        video_url = inf.get("play") or inf.get("hdplay") or inf.get("wmplay")
        if not video_url: log_err("Video URL not found."); return
        download_file_with_progress(video_url, filename, "mp4")

def flow_youtube():
    section_header(f"{t('menu_downloader')}  ›  YouTube")
    url = prompt(f"YouTube URL  ({t('back')})")
    if url.lower() == "back": return
    if "youtube.com" not in url and "youtu.be" not in url:
        log_err("Invalid URL. Must be from youtube.com or youtu.be"); return

    log_info(f"{t('fetching_info')}...")
    try:
        res = subprocess.run(["yt-dlp", "--dump-json", "--no-playlist", url],
                              capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Failed to fetch info. Check URL and internet."); return
        inf = json.loads(res.stdout)
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    title = inf.get("title", "video")
    uploader = inf.get("uploader") or inf.get("channel", "unknown")
    duration = inf.get("duration") or 0
    views = inf.get("view_count") or 0
    filename = sanitize(f"{uploader}_{title}")

    print()
    show_info([
        (t("channel"),  uploader),
        (t("title"),    title),
        (t("duration"), f"{int(duration)//60}:{int(duration)%60:02d}"),
        (t("views"),    f"{views:,}"),
    ])

    fmt, embed_meta = pick_format(with_album=True)
    download_ytdlp_with_progress(url, filename, fmt, embed_meta=embed_meta)

def flow_generic(platform, domains):
    section_header(f"{t('menu_downloader')}  ›  {platform}")
    url = prompt(f"{platform} URL  ({t('back')})")
    if url.lower() == "back": return
    if domains and not any(d in url for d in domains):
        log_err(f"Invalid URL for {platform}."); return

    log_info(f"{t('fetching_info')}...")
    try:
        res = subprocess.run(["yt-dlp", "--dump-json", "--no-playlist", url],
                              capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Failed to fetch info. Make sure URL is valid and public."); return
        inf = json.loads(res.stdout)
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    title = inf.get("title", "video")
    uploader = inf.get("uploader") or inf.get("channel", "unknown")
    duration = inf.get("duration") or 0
    views = inf.get("view_count") or 0
    filename = sanitize(f"{uploader}_{title}")

    print()
    show_info([
        (t("account"),  uploader),
        (t("title"),    title),
        (t("duration"), f"{int(duration)//60}:{int(duration)%60:02d}"),
        (t("views"),    f"{views:,}"),
    ])

    fmt, _ = pick_format()
    download_ytdlp_with_progress(url, filename, fmt)

def tracker_tiktok():
    section_header(f"{t('menu_tracker')}  ›  TikTok")
    print(f"  {PINK}[1]{RESET}  {WHITE}{t('lookup')}{RESET}   {GRAY}— know the username{RESET}")
    print(f"  {PINK}[2]{RESET}  {WHITE}{t('search')}{RESET}   {GRAY}— find by keyword{RESET}")
    print()
    mode = prompt(t("select"))
    if mode == "1":
        u = prompt(f"{t('username')}  (without @, or '{t('back')}')")
        if u.lower() != "back": _tt_lookup(u.lstrip("@"))
    elif mode == "2":
        kw = prompt(f"{t('keyword')}  (or '{t('back')}')")
        if kw.lower() != "back": _tt_search(kw)

def _tt_lookup(username):
    log_info(f"{t('searching')} @{username}...")
    try:
        r = requests.get(f"{TIKWM_API}user/info?unique_id={username}", timeout=15)
        data = r.json()
        if data.get("code") != 0:
            log_err(f"{t('user_not_found')}: {data.get('msg', 'unknown')}"); return
        u = data.get("data", {}).get("user", {})
        s = data.get("data", {}).get("stats", {})
        if not u:
            log_err(t("user_not_found")); return
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return
    print()
    show_info([
        (t("username"),  f"@{u.get('uniqueId', username)}"),
        ("Name",      u.get("nickname", "-")),
        (t("bio"),       (u.get("signature") or "-")[:70]),
        (t("followers"), f"{s.get('followerCount', 0):,}"),
        (t("following"), f"{s.get('followingCount', 0):,}"),
        (t("likes"),     f"{s.get('heartCount', 0):,}"),
        (t("videos"),    f"{s.get('videoCount', 0):,}"),
        (t("verified"),  f"{t('yes')}" if u.get("verified") else t("no")),
        (t("avatar"),    u.get("avatarLarger", "-")),
    ])

def _tt_search(keyword):
    log_info(f"{t('searching')} '{keyword}'...")
    try:
        r = requests.get(f"{TIKWM_API}user/search?keyword={keyword}&count=10", timeout=15)
        data = r.json()
        if data.get("code") != 0:
            log_err(f"Search failed: {data.get('msg', 'unknown')}"); return
        users = data.get("data", {}).get("user_list", [])
        if not users:
            log_err(t("no_results")); return
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    print(); divider()
    print(f"\n  {PINK2}{BOLD}  {t('search')} {t('results')}{RESET}\n")
    for i, item in enumerate(users, 1):
        u = item.get("user_info", {})
        uid = u.get("unique_id", "-")
        nick = u.get("nickname", "-")
        fol = u.get("follower_count", 0)
        v = f" {GREEN}✓{RESET}" if u.get("is_verified") else ""
        print(f"  {PINK}[{i:>2}]{RESET}  {WHITE}@{uid:<20}{RESET}  {GRAY}{nick[:16]:<16}  {fol:>10,} {t('followers')}{RESET}{v}")
    print(); divider(); print()

    c = prompt(f"{t('select')} number to view profile  (or '{t('back')}')")
    if c.lower() == "back": return
    try:
        idx = int(c) - 1
        if not 0 <= idx < len(users): raise ValueError
        selected = users[idx].get("user_info", {}).get("unique_id", "")
        if selected:
            _tt_lookup(selected)
        else:
            log_err(t("user_not_found"))
    except ValueError:
        log_err(t("invalid"))

def tracker_youtube():
    section_header(f"{t('menu_tracker')}  ›  YouTube")
    print(f"  {PINK}[1]{RESET}  {WHITE}{t('lookup')}{RESET}   {GRAY}— know the @handle or URL{RESET}")
    print(f"  {PINK}[2]{RESET}  {WHITE}{t('search')}{RESET}   {GRAY}— find by keyword{RESET}")
    print()
    mode = prompt(t("select"))
    if mode == "1":
        h = prompt(f"@handle or channel URL  ({t('back')})")
        if h.lower() != "back": _yt_lookup(h)
    elif mode == "2":
        kw = prompt(f"{t('keyword')}  ({t('back')})")
        if kw.lower() != "back": _yt_search(kw)

def _yt_lookup(handle):
    log_info(f"{t('fetching_info')}...")
    try:
        if not handle.startswith("http"):
            handle = f"https://www.youtube.com/{handle if handle.startswith('@') else '@'+handle}"
        res = subprocess.run(
            ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "50", handle],
            capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Channel not found. Check handle/URL."); return
        inf = json.loads(res.stdout)
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return
    
    playlist_count = inf.get("playlist_count", 0)
    if playlist_count == 0:
        try:
            res2 = subprocess.run(
                ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "1", f"{handle}/videos"],
                capture_output=True, text=True, timeout=30)
            if res2.returncode == 0:
                inf2 = json.loads(res2.stdout)
                playlist_count = inf2.get("playlist_count", 0)
        except:
            pass
    
    print()
    show_info([
        (t("channel"),  inf.get("channel") or inf.get("title", "-")),
        ("Handle",   inf.get("uploader_id", "-")),
        (t("subscribers"), f"{inf.get('channel_follower_count', 0):,}" if inf.get("channel_follower_count") else "Hidden"),
        (t("total_videos"), str(playlist_count) if playlist_count > 0 else "-"),
        (t("joined"),    inf.get("upload_date", "-")[:4] if inf.get("upload_date") else "-"),
        ("URL",      inf.get("webpage_url", "-")),
    ])

def _yt_search(keyword):
    log_info(f"{t('searching')} '{keyword}'...")
    try:
        res = subprocess.run(
            ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "8",
             f"ytsearch8:{keyword}"],
            capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Search failed."); return
        results = [json.loads(l) for l in res.stdout.strip().splitlines() if l.strip()]
        if not results:
            log_err(t("no_results")); return
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    print(); divider()
    print(f"\n  {PINK2}{BOLD}  {t('search')} {t('results')}{RESET}\n")
    for i, item in enumerate(results, 1):
        title = (item.get("title") or "-")[:34]
        ch = (item.get("uploader") or item.get("channel") or "-")[:18]
        print(f"  {PINK}[{i}]{RESET}  {WHITE}{title:<34}{RESET}  {GRAY}{ch}{RESET}")
    print(); divider(); print()

    c = prompt(f"{t('select')} number  ({t('back')})")
    if c.lower() == "back": return
    try:
        idx = int(c) - 1
        if not 0 <= idx < len(results): raise ValueError
        _yt_lookup(results[idx].get("url") or results[idx].get("webpage_url", ""))
    except ValueError:
        log_err(t("invalid"))

def tracker_generic(platform, domains):
    section_header(f"{t('menu_tracker')}  ›  {platform}")
    print(f"  {PINK}[1]{RESET}  {WHITE}{t('lookup')}{RESET}   {GRAY}— know the profile URL{RESET}")
    print(f"  {PINK}[2]{RESET}  {WHITE}{t('search')}{RESET}   {GRAY}— find by keyword{RESET}")
    print()
    mode = prompt(t("select"))
    if mode == "1":
        url = prompt(f"{platform} profile URL  ({t('back')})")
        if url.lower() == "back": return
        if domains and not any(d in url for d in domains):
            log_err(f"Invalid URL for {platform}."); return
        _generic_lookup(platform, url)
    elif mode == "2":
        kw = prompt(f"{t('keyword')}  ({t('back')})")
        if kw.lower() != "back": _generic_search(platform, kw)

def _generic_lookup(platform, url):
    log_info(f"{t('fetching_info')}...")
    try:
        res = subprocess.run(
            ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "50", url],
            capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Failed. Make sure URL is public."); return
        inf = json.loads(res.stdout)
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return
    
    playlist_count = inf.get("playlist_count", 0)
    if playlist_count == 0 and "videos" in url.lower():
        try:
            res2 = subprocess.run(
                ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "1", url],
                capture_output=True, text=True, timeout=30)
            if res2.returncode == 0:
                inf2 = json.loads(res2.stdout)
                playlist_count = inf2.get("playlist_count", 0)
        except:
            pass
    
    print()
    show_info([
        ("Name",      inf.get("uploader") or inf.get("channel") or inf.get("title", "-")),
        ("ID",        inf.get("uploader_id") or inf.get("channel_id", "-")),
        (t("followers"), f"{inf.get('channel_follower_count', 0):,}" if inf.get("channel_follower_count") else "-"),
        (t("total_videos"), str(playlist_count) if playlist_count > 0 else "-"),
        (t("bio"),     (inf.get("description") or "-")[:80]),
        ("URL",       inf.get("webpage_url", url)),
    ])

def _generic_search(platform, keyword):
    log_info(f"{t('searching')} '{keyword}'...")
    try:
        res = subprocess.run(
            ["yt-dlp", "--dump-json", "--flat-playlist", "--playlist-end", "8",
             f"ytsearch8:{keyword}"],
            capture_output=True, text=True, timeout=30)
        if res.returncode != 0:
            log_err("Search failed."); return
        results = [json.loads(l) for l in res.stdout.strip().splitlines() if l.strip()]
        if not results:
            log_err(t("no_results")); return
    except Exception as e:
        log_err(f"{t('error')}: {e}"); return

    print(); divider()
    print(f"\n  {PINK2}{BOLD}  {t('search')} {t('results')}{RESET}\n")
    for i, item in enumerate(results, 1):
        title = (item.get("title") or "-")[:34]
        up = (item.get("uploader") or "-")[:18]
        print(f"  {PINK}[{i}]{RESET}  {WHITE}{title:<34}{RESET}  {GRAY}{up}{RESET}")
    print(); divider(); print()

    c = prompt(f"{t('select')} number  ({t('back')})")
    if c.lower() == "back": return
    try:
        idx = int(c) - 1
        if not 0 <= idx < len(results): raise ValueError
        _generic_lookup(platform, results[idx].get("url") or results[idx].get("webpage_url", ""))
    except ValueError:
        log_err(t("invalid"))

def menu_settings():
    global config
    while True:
        section_header(t("menu_settings"))
        print(f"  {PINK}[1]{RESET}  {WHITE}{t('language')}{RESET}     {GRAY}— {config['language'].upper()}{RESET}")
        print(f"  {PINK}[2]{RESET}  {WHITE}{t('primary_color')}{RESET}  {GRAY}— {config['primary_color'].upper()}{RESET}")
        print(f"\n  {PINK}[0]{RESET}  {GRAY}{t('back')}{RESET}")
        divider(); print()
        
        c = prompt(t("select"))
        if c == "0":
            save_config()
            return
        elif c == "1":
            section_header(t("choose_lang"))
            langs = ["english", "indonesia", "chinese", "hindi", "japanese", "korean", "russian"]
            lang_names = ["English", "Indonesia", "中文", "हिन्दी", "日本語", "한국어", "Русский"]
            for i, name in enumerate(lang_names, 1):
                print(f"  {PINK}[{i}]{RESET}  {name}")
            print()
            lc = prompt(t("select"))
            if lc.isdigit() and 1 <= int(lc) <= len(langs):
                config["language"] = langs[int(lc)-1]
                log_ok(f"Language changed to {lang_names[int(lc)-1]}")
            else:
                log_err(t("invalid"))
            time.sleep(1)
        elif c == "2":
            section_header(t("choose_color"))
            print(f"  {PINK}[1]{RESET}  Pink")
            print(f"  {RED}[2]{RESET}  Red")
            print(f"  {GREEN}[3]{RESET}  Green")
            print(f"  \033[38;5;129m[4]{RESET}  Purple")
            print(f"  \033[38;5;39m[5]{RESET}  Blue")
            print(f"  \033[38;5;214m[6]{RESET}  Orange")
            print()
            cc = prompt(t("select"))
            colors = ["pink", "red", "green", "purple", "blue", "orange"]
            if cc in ["1","2","3","4","5","6"]:
                config["primary_color"] = colors[int(cc)-1]
                refresh_colors()
                log_ok(t("color_changed"))
            else:
                log_err(t("invalid"))
            time.sleep(1)
        else:
            log_err(t("invalid"))
            time.sleep(1)

def menu_about():
    section_header(t("menu_about"))
    print(f"  {WHITE}{BOLD}Nezuka Video Downloader{RESET}")
    print()
    print(f"  {GRAY}Version:{RESET}     3.0")
    print(f"  {GRAY}Developer:{RESET}   Nezuka")
    print(f"  {GRAY}Language:{RESET}    {config['language'].upper()}")
    print(f"  {GRAY}Color:{RESET}       {config['primary_color'].upper()}")
    print()
    print(f"  {PINK}┌─────────────────────────────────────────┐{RESET}")
    print(f"  {PINK}│{RESET}  {WHITE}Supported Platforms:{RESET}                         {PINK}│{RESET}")
    print(f"  {PINK}│{RESET}  • TikTok    • YouTube   • Instagram               {PINK}│{RESET}")
    print(f"  {PINK}│{RESET}  • Facebook  • Twitter   • CapCut                  {PINK}│{RESET}")
    print(f"  {PINK}│{RESET}  • Pinterest • Doodstream • Snack Video            {PINK}│{RESET}")
    print(f"  {PINK}└─────────────────────────────────────────┘{RESET}")
    print()
    print(f"  {GRAY}A powerful video downloader with tracker features.{RESET}")
    print(f"  {GRAY}Made with ❤️ for content creators.{RESET}")
    print()
    prompt(t("press_enter"))

DL_MENU = [
    ("TikTok",      None),
    ("CapCut",      ["capcut.com"]),
    ("Instagram",   ["instagram.com"]),
    ("Facebook",    ["facebook.com", "fb.watch"]),
    ("YouTube",     None),
    ("Twitter / X", ["twitter.com", "x.com"]),
    ("Snack Video", ["snackvideo.com", "snack.video"]),
    ("Doodstream",  ["doodstream.com", "dood."]),
    ("Pinterest",   ["pinterest.com", "pin.it"]),
    ("Other URL",   None),
]

TK_MENU = [
    ("TikTok",      None),
    ("YouTube",     None),
    ("Instagram",   ["instagram.com"]),
    ("Facebook",    ["facebook.com", "fb.watch"]),
    ("Twitter / X", ["twitter.com", "x.com"]),
    ("Snack Video", ["snackvideo.com"]),
]

def menu_downloader():
    while True:
        section_header(t("menu_downloader"))
        for i, (name, _) in enumerate(DL_MENU, 1):
            print(f"  {PINK}[{i:>2}]{RESET}  {WHITE}{name}{RESET}")
        print(f"\n  {PINK}[ 0]{RESET}  {GRAY}{t('back')}{RESET}")
        divider(); print()
        c = prompt(t("select"))
        if c == "0": return
        try:
            idx = int(c) - 1
            if not 0 <= idx < len(DL_MENU): raise ValueError
        except ValueError:
            log_err(t("invalid")); time.sleep(1); continue

        name, domains = DL_MENU[idx]
        if name == "TikTok":    flow_tiktok()
        elif name == "YouTube": flow_youtube()
        else:                   flow_generic(name, domains)
        print(); prompt(t("press_enter"))

def menu_tracker():
    while True:
        section_header(t("menu_tracker"))
        for i, (name, _) in enumerate(TK_MENU, 1):
            print(f"  {PINK}[{i}]{RESET}  {WHITE}{name}{RESET}")
        print(f"\n  {PINK}[0]{RESET}  {GRAY}{t('back')}{RESET}")
        divider(); print()
        c = prompt(t("select"))
        if c == "0": return
        try:
            idx = int(c) - 1
            if not 0 <= idx < len(TK_MENU): raise ValueError
        except ValueError:
            log_err(t("invalid")); time.sleep(1); continue

        name, domains = TK_MENU[idx]
        if name == "TikTok":    tracker_tiktok()
        elif name == "YouTube": tracker_youtube()
        else:                   tracker_generic(name, domains)
        print(); prompt(t("press_enter"))

def main():
    load_languages()
    load_config()
    refresh_colors()
    
    if not check_ytdlp():
        clear(); banner()
        log_err("yt-dlp not found!")
        print(f"\n  {GRAY}Install:{RESET} {PINK}pip install yt-dlp{RESET}\n")
        sys.exit(1)

    while True:
        clear(); banner()
        print(f"  {PINK}[1]{RESET}  {WHITE}{t('menu_downloader')}{RESET}  {GRAY}— Download videos & audio{RESET}")
        print(f"  {PINK}[2]{RESET}  {WHITE}{t('menu_tracker')}{RESET}     {GRAY}— View account profiles{RESET}")
        print(f"  {PINK}[3]{RESET}  {WHITE}{t('menu_settings')}{RESET}     {GRAY}— Language & color{RESET}")
        print(f"  {PINK}[4]{RESET}  {WHITE}{t('menu_about')}{RESET}        {GRAY}— Info{RESET}")
        print(f"\n  {PINK}[0]{RESET}  {GRAY}{t('menu_exit')}{RESET}")
        divider(); print()
        c = prompt(t("select"))

        if c == "0":
            clear()
            print(f"\n  {PINK}{BOLD}{t('app_name')}{RESET} {WHITE}— See you!{RESET}\n")
            break
        elif c == "1": menu_downloader()
        elif c == "2": menu_tracker()
        elif c == "3": menu_settings()
        elif c == "4": menu_about()
        else:
            log_err(t("invalid")); time.sleep(1)

if __name__ == "__main__":
    main()
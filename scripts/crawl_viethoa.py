"""Automated Vietnamese Localization (Viet Hoa) Web Crawler & Validator.

Discovers community Vietnamese game localization patches from:
1. GitHub Repositories & Releases API (direct release archive assets)
2. Steam Community Vietnamese Guides (exact Steam AppID + direct GitHub/GDrive/Pixeldrain links)
3. Existing GitHub-backed catalog entries (automatic version bump on new releases)

Every candidate passes a strict zero-trust safety gate before entering vietnamese_catalog.json:
- HTTPS direct-host allowlist (GitHub, Google Drive, Pixeldrain; no ad-shorteners)
- Exact Steam Store AppID & game-type verification (strict sequel-number symmetry)
- Live HTTP stream probe + magic-byte verification (ZIP / 7Z / RAR / TAR.GZ; rejects .exe/HTML)
- Full SHA-256 hashing, password/encryption rejection, installer-only rejection, and
  automatic strip_components inference for 1-click extraction into game roots.

Pure Python stdlib + requests (zero GUI dependencies) so the exact same module runs inside
GitHub Actions (`ubuntu-latest`) and local unit/integration tests.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import html
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unicodedata
from urllib.parse import parse_qs, unquote, urlparse
import zipfile
from typing import Any

import requests

logger = logging.getLogger(__name__)
TAG = "[VietHoa/Crawler]"

USER_AGENT = "BobGameCenter-VietHoaCrawler/1.0 (+https://github.com/vodacthe/bob_gaming_game_center_public)"
HTTP_TIMEOUT = (10, 45)
DEFAULT_MAX_INSPECT_BYTES = 150 * 1024 * 1024  # 150 MiB per patch in CI
MIN_ARCHIVE_BYTES = 512

ALLOWED_DOWNLOAD_HOSTS = frozenset(
    {
        "github.com",
        "objects.githubusercontent.com",
        "release-assets.githubusercontent.com",
        "codeload.github.com",
        "drive.google.com",
        "drive.usercontent.google.com",
        "pixeldrain.com",
    }
)

ARCHIVE_EXTENSIONS = (".zip", ".7z", ".rar", ".tar.gz", ".tgz")
SKIP_ASSET_KEYWORDS = (
    "source",
    "src",
    "linux",
    "macos",
    "darwin",
    "osx",
    "android",
    ".apk",
    ".ipa",
    ".deb",
    ".rpm",
    ".appimage",
    "installer",
    "setup",
    ".exe",
    ".msi",
    "server",
    "bepinex_unix",
)

NON_GAME_REPO_KEYWORDS = frozenset(
    {
        "wordpress",
        "woocommerce",
        "magento",
        "prestashop",
        "opencart",
        "xenforo",
        "flarum",
        "discuz",
        "phpbb",
        "laravel",
        "django",
        "fastapi",
        "nextjs",
        "react",
        "vue",
        "angular",
        "flutter",
        "android",
        "xiaomi",
        "miui",
        "hyperos",
        "magisk",
        "ibus",
        "fcitx",
        "unikey",
        "evkey",
        "telegram",
        "discord",
        "chatbot",
        "anki",
        "leetcode",
        "algorithm",
        "coursera",
        "udemy",
        "youtube",
        "subtitle",
        "whisper",
        "openai",
        "chatgpt",
        "claude",
        "gemini",
        "llm",
        "ollama",
        "tts",
        "ocr",
        "odoo",
        "erp",
        "home-assistant",
        "homeassistant",
        "vscode",
        "neovim",
        "vim",
        "emacs",
        "obsidian",
        "notion",
        "zotero",
        "calibre",
        "koreader",
        "jellyfin",
        "plex",
        "kodi",
        "spigot",
        "bukkit",
        "paper",
        "purpur",
        "pterodactyl",
        "pocketmine",
        "esphome",
        "openwrt",
        "pfsense",
        "proxmox",
        "docker",
        "kubernetes",
        "ublock",
        "adguard",
        "userscript",
        "tampermonkey",
    }
)

GAME_ROOT_KNOWN_DIRS = frozenset(
    {
        "bepinex",
        "melonloader",
        "mono",
        "dotnet",
        "data",
        "gamedata",
        "game_data",
        "content",
        "mods",
        "mod",
        "dlc",
        "x64",
        "x86",
        "bin",
        "binaries",
        "engine",
        "archive",
        "game",
        "renpy",
        "www",
        "pak",
        "paks",
        "~mods",
        "streamingassets",
        "locales",
        "localization",
        "languages",
        "lang",
        "resources",
        "assets",
        "media",
        "romfs",
        "patch",
        "patches",
        "plugins",
        "scripts",
    }
)

DOC_OR_NOISE_EXTS = frozenset(
    {
        ".md",
        ".txt",
        ".pdf",
        ".doc",
        ".docx",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".bmp",
        ".ico",
        ".url",
        ".lnk",
        ".html",
        ".htm",
        ".ds_store",
    }
)

INSTALLER_BINARY_EXTS = frozenset({".exe", ".msi", ".bat", ".cmd", ".vbs", ".ps1"})

GITHUB_SEARCH_QUERIES = (
    '"viet hoa" in:name,description',
    '"việt hóa" in:name,description',
    '"việt hoá" in:name,description',
    "vietnamese localization mod in:name,description",
    "vietnamese translation patch game in:name,description",
)

STEAM_GUIDE_QUERIES = (
    "Viet Hoa",
    "Việt Hóa",
    "Việt Hoá",
)

_GDRIVE_ID_RE = re.compile(
    r"(?:drive\.google\.com/file/d/|drive\.google\.com/open\?[^#\"\s<>]*?\bid=|"
    r"drive\.(?:usercontent\.)?google\.com/(?:uc|download)\?[^#\"\s<>]*?\bid=)([A-Za-z0-9_-]{15,})"
)
_PIXELDRAIN_RE = re.compile(r"https?://pixeldrain\.com/(?:u|api/file)/([A-Za-z0-9_-]{6,})")
_GH_RELEASE_DL_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/releases/download/[^\s\"'<>)]+"
)
_GH_REPO_RE = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
_STEAM_APP_RE = re.compile(r"(?:store\.steampowered\.com|steamcommunity\.com)/app/(\d+)")
_STEAM_GUIDE_URL_RE = re.compile(r"https://steamcommunity\.com/sharedfiles/filedetails/\?id=\d+")
_STEAM_LINKFILTER_RE = re.compile(r"https?://steamcommunity\.com/linkfilter/\?(?:u|url)=([^\"'&\s<>]+)")
_PASSWORD_HINT_RE = re.compile(
    r"(?:\bpass(?:word)?\s*(?:giải\s*nén|rar|zip|7z)?\s*[:=]|mật\s*khẩu\s*(?:giải\s*nén)?\s*[:=])",
    re.IGNORECASE,
)

_VIETHOA_STRIP_PATTERNS = (
    r"\[[^\]]*\]",
    r"\([^\)]*(?:việt\s*h[oó][aá]|viet\s*hoa|vietnamese|tiếng\s*việt|tieng\s*viet|patch|mod|vh)[^\)]*\)",
    r"\bv?\d+(?:\.\d+){1,3}[a-z]?\b",
    r"\b(?:bản\s*dịch|ban\s*dich|dự\s*án|du\s*an|nhóm\s*dịch|nhom\s*dich)\b",
    r"\b(?:việt\s*hóa|việt\s*hoá|viet\s*hoa|viethoa|tiếng\s*việt|tieng\s*viet)\b",
    r"\b(?:vietnamese\s*localization|vietnamese\s*translation|vietnamese\s*language|vietnamese\s*patch|vietnamese\s*mod|vietnamese)\b",
    r"\b(?:localization|localisation|translation|language\s*pack|subtitles?|patch|mod|vh)\b",
)

_ROMAN_TO_INT = {
    "ii": "2",
    "iii": "3",
    "iv": "4",
    "v": "5",
    "vi": "6",
    "vii": "7",
    "viii": "8",
    "ix": "9",
    "x": "10",
}

_STOP_TOKENS = frozenset({"the", "a", "an", "of", "and", "for", "in", "on", "to", "edition", "game"})
_BANNED_STEAM_TITLE_WORDS = frozenset(
    {"soundtrack", "ost", "artbook", "demo", "playtest", "dedicated server", "sdk", "wallpaper", "trailer", "teaser"}
)


@dataclass
class RawCandidate:
    """Unverified localization candidate discovered from an external source."""

    source: str
    raw_title: str
    download_url: str
    team: str
    team_url: str
    version: str = "1.0"
    steam_appid: int | None = None
    notes: str = ""


@dataclass
class VerifiedArchive:
    """Result of probing, hashing, and inspecting a candidate archive."""

    download_url: str
    download_type: str
    sha256: str
    size_bytes: int
    strip_components: int


def _strip_accents(text: str) -> str:
    norm = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    return "".join(ch for ch in norm if unicodedata.category(ch) != "Mn")


def slugify_game_id(title: str) -> str:
    """Convert canonical game title into a clean snake_case catalog key."""
    ascii_text = _strip_accents(title or "").lower()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_text).strip("_")
    return slug[:64] or "unknown_game"


def extract_clean_game_title(raw_title: str) -> str:
    """Strip Vietnamese localization boilerplate from repo/guide names to isolate the game title."""
    t = html.unescape(str(raw_title or "")).strip()
    t = t.replace("_", " ").replace("-", " ")
    # Strip version tags before letter-digit splitting so 'v1.2.0' never leaves standalone 'v'
    t = re.sub(r"\bv?\d+(?:\.\d+){1,3}[a-z]?\b", " ", t, flags=re.IGNORECASE)
    # Split CamelCase ('HollowKnight' -> 'Hollow Knight') and letter-digit boundaries ('DarkSouls3' -> 'Dark Souls 3')
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)
    t = re.sub(r"([A-Za-z])(\d)", r"\1 \2", t)
    t = re.sub(r"(\d)([A-Za-z])", r"\1 \2", t)
    for pat in _VIETHOA_STRIP_PATTERNS:
        t = re.sub(pat, " ", t, flags=re.IGNORECASE)
    t = t.replace(".", " ")
    t = re.sub(r"\s*[-:|/–—+]+\s*", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" -_:|/–—()[]{}")
    return t


def _title_tokens(title: str) -> set[str]:
    ascii_t = _strip_accents(title or "").lower()
    raw_tokens = re.findall(r"[a-z0-9]+", ascii_t)
    normalized: set[str] = set()
    for tok in raw_tokens:
        mapped = _ROMAN_TO_INT.get(tok, tok)
        if mapped not in _STOP_TOKENS:
            normalized.add(mapped)
    return normalized


def titles_match_strictly(candidate_title: str, steam_title: str) -> bool:
    """Verify candidate game title matches Steam Store canonical title without sequel cross-matching."""
    low_steam = (steam_title or "").lower()
    if any(bad in low_steam for bad in _BANNED_STEAM_TITLE_WORDS):
        return False

    c_tokens = _title_tokens(candidate_title)
    s_tokens = _title_tokens(steam_title)
    if not c_tokens or not s_tokens:
        return False

    # Require at least one non-numeric token of length >= 3
    if not any((not tok.isdigit() and len(tok) >= 3) for tok in c_tokens):
        return False

    # Strict sequel-number symmetry: e.g. 'Witcher 2' must never match 'The Witcher 3'
    c_nums = {t for t in c_tokens if t.isdigit()}
    s_nums = {t for t in s_tokens if t.isdigit()}
    if c_nums != s_nums:
        return False

    if c_tokens == s_tokens:
        return True

    # Allow Steam title to have subtitle suffix ('The Witcher 3: Wild Hunt' vs 'The Witcher 3')
    if ":" in steam_title or " - " in steam_title or " – " in steam_title:
        base_steam = re.split(r":|\s[-–—]\s", steam_title, maxsplit=1)[0]
        base_tokens = _title_tokens(base_steam)
        base_nums = {t for t in base_tokens if t.isdigit()}
        if base_tokens and c_tokens == base_tokens and c_nums == base_nums:
            return True

    overlap = len(c_tokens & s_tokens)
    union = len(c_tokens | s_tokens)
    return union > 0 and (overlap / union) >= 0.8 and len(c_tokens) >= 2


def normalize_download_url(raw_url: str) -> tuple[str, str] | None:
    """Normalize supported direct/GDrive/Pixeldrain URLs and reject untrusted hosts."""
    u = html.unescape(str(raw_url or "")).strip().rstrip(").,;\"'>]")
    if not u.startswith("https://"):
        return None

    gd = _GDRIVE_ID_RE.search(u)
    if gd:
        fid = gd.group(1)
        return f"https://drive.google.com/file/d/{fid}/view", "gdrive"

    pd = _PIXELDRAIN_RE.search(u)
    if pd:
        fid = pd.group(1)
        return f"https://pixeldrain.com/api/file/{fid}", "direct"

    parsed = urlparse(u)
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_DOWNLOAD_HOSTS:
        return None

    low_path = parsed.path.lower()
    if low_path.endswith((".exe", ".msi", ".bat", ".apk", ".dmg", ".deb")):
        return None
    if host == "github.com" and "/releases/download/" not in low_path and "/archive/" not in low_path:
        return None
    return u, "direct"


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    }
    token = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _http_get_json(
    session: requests.Session,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
) -> Any | None:
    started = time.monotonic()
    try:
        resp = session.get(url, headers=headers, params=params, timeout=HTTP_TIMEOUT)
        dur = time.monotonic() - started
        if resp.status_code != 200:
            logger.warning(f"{TAG} HTTP GET failed: url={url} status={resp.status_code} duration={dur:.2f}s")
            return None
        return resp.json()
    except Exception as e:
        dur = time.monotonic() - started
        logger.warning(f"{TAG} HTTP GET error: url={url} status=ERR duration={dur:.2f}s ({e})")
        return None


def _is_non_game_repo(name: str, description: str, topics: list[str]) -> bool:
    haystack = f"{name} {description} {' '.join(topics)}".lower()
    for kw in NON_GAME_REPO_KEYWORDS:
        if kw in haystack:
            return True
    return False


def _pick_best_release_asset(assets: list[dict[str, Any]], max_bytes: int) -> dict[str, Any] | None:
    scored: list[tuple[int, dict[str, Any]]] = []
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        name = str(asset.get("name") or "").strip()
        low = name.lower()
        url = str(asset.get("browser_download_url") or "").strip()
        size = int(asset.get("size") or 0)
        if not url.startswith("https://") or size < MIN_ARCHIVE_BYTES or size > max_bytes:
            continue
        if not low.endswith(ARCHIVE_EXTENSIONS):
            continue
        if any(skip in low for skip in SKIP_ASSET_KEYWORDS):
            continue

        score = 10
        if any(k in low for k in ("viethoa", "viet_hoa", "viet-hoa", "vietnamese", "tiengviet", "vh")):
            score += 20
        if low.endswith(".zip"):
            score += 5
        if "win" in low or "pc" in low:
            score += 3
        scored.append((score, asset))

    if not scored:
        return None
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def discover_github_candidates(
    session: requests.Session,
    *,
    per_query: int = 20,
    max_inspect_bytes: int = DEFAULT_MAX_INSPECT_BYTES,
) -> list[RawCandidate]:
    """Search public GitHub repositories & releases for Vietnamese game localization archives."""
    headers = _github_headers()
    seen_repos: set[str] = set()
    candidates: list[RawCandidate] = []

    for query in GITHUB_SEARCH_QUERIES:
        data = _http_get_json(
            session,
            "https://api.github.com/search/repositories",
            headers=headers,
            params={"q": query, "sort": "updated", "order": "desc", "per_page": per_query},
        )
        items = data.get("items") if isinstance(data, dict) else None
        if not isinstance(items, list):
            continue

        for repo in items:
            if not isinstance(repo, dict) or repo.get("fork") or repo.get("disabled"):
                continue
            full_name = str(repo.get("full_name") or "").strip()
            if not full_name or full_name.lower() in seen_repos:
                continue
            seen_repos.add(full_name.lower())

            name = str(repo.get("name") or "")
            desc = str(repo.get("description") or "")
            topics = [str(t) for t in (repo.get("topics") or []) if t]
            if _is_non_game_repo(name, desc, topics):
                logger.debug(f"{TAG} Skipping non-game repository '{full_name}'")
                continue

            releases = _http_get_json(
                session,
                f"https://api.github.com/repos/{full_name}/releases",
                headers=headers,
                params={"per_page": 3},
            )
            if not isinstance(releases, list) or not releases:
                continue

            chosen_release = None
            chosen_asset = None
            for rel in releases:
                if not isinstance(rel, dict) or rel.get("draft"):
                    continue
                body_text = str(rel.get("body") or "")
                if _PASSWORD_HINT_RE.search(body_text) or _PASSWORD_HINT_RE.search(desc):
                    logger.debug(f"{TAG} Skipping password-hinted release in '{full_name}'")
                    continue
                asset = _pick_best_release_asset(rel.get("assets") or [], max_inspect_bytes)
                if asset is not None:
                    chosen_release = rel
                    chosen_asset = asset
                    break

            if not chosen_release or not chosen_asset:
                continue

            combined_text = f"{desc}\n{chosen_release.get('body') or ''}"
            app_m = _STEAM_APP_RE.search(combined_text)
            appid = int(app_m.group(1)) if app_m else None

            raw_title = extract_clean_game_title(name) or extract_clean_game_title(desc)
            if not raw_title and not appid:
                continue

            owner_login = str((repo.get("owner") or {}).get("login") or full_name.split("/")[0])
            tag_name = str(chosen_release.get("tag_name") or "1.0").lstrip("vV") or "1.0"
            candidates.append(
                RawCandidate(
                    source="github_release",
                    raw_title=raw_title or name,
                    download_url=str(chosen_asset["browser_download_url"]),
                    team=owner_login,
                    team_url=str(repo.get("html_url") or f"https://github.com/{full_name}"),
                    version=tag_name,
                    steam_appid=appid,
                    notes=desc[:200].strip() or f"Ban Viet Hoa tu GitHub ({full_name})",
                )
            )

    logger.info(f"{TAG} GitHub discovery found {len(candidates)} release archive candidates from {len(seen_repos)} repos")
    return candidates


def _unwrap_steam_links(page_html: str) -> list[str]:
    """Extract both linkfilter-wrapped and direct external links from Steam Guide HTML."""
    urls: list[str] = []
    unescaped = html.unescape(page_html or "")
    for m in _STEAM_LINKFILTER_RE.finditer(unescaped):
        decoded = unquote(m.group(1)).strip()
        if decoded.startswith("https://"):
            urls.append(decoded)
    for regex in (_GH_RELEASE_DL_RE, _PIXELDRAIN_RE):
        for m in regex.finditer(unescaped):
            urls.append(m.group(0))
    for m in _GDRIVE_ID_RE.finditer(unescaped):
        urls.append(f"https://drive.google.com/file/d/{m.group(1)}/view")

    deduped: list[str] = []
    seen: set[str] = set()
    for u in urls:
        norm = normalize_download_url(u)
        if norm and norm[0] not in seen:
            seen.add(norm[0])
            deduped.append(norm[0])
    return deduped


def discover_steam_guide_candidates(
    session: requests.Session,
    *,
    existing_appids: set[int] | None = None,
    max_guides: int = 20,
) -> list[RawCandidate]:
    """Scan Steam Community Vietnamese localization guides for exact AppID + direct archive links."""
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "vi,en-US;q=0.9,en;q=0.8"}
    guide_urls: list[str] = []
    seen_guides: set[str] = set()
    known_ids = existing_appids or set()

    for q in STEAM_GUIDE_QUERIES:
        started = time.monotonic()
        search_url = "https://steamcommunity.com/workshop/browse/"
        try:
            resp = session.get(
                search_url,
                headers=headers,
                params={
                    "appid": 0,
                    "searchtext": q,
                    "browsesort": "trend",
                    "section": "readytouseitems",
                    "actualsort": "trend",
                    "days": 365,
                    "p": 1,
                },
                timeout=HTTP_TIMEOUT,
            )
            dur = time.monotonic() - started
            if resp.status_code != 200:
                logger.warning(
                    f"{TAG} Steam guide search failed: url={search_url} status={resp.status_code} duration={dur:.2f}s"
                )
                continue
            for m in _STEAM_GUIDE_URL_RE.finditer(resp.text):
                g_url = m.group(0)
                if g_url not in seen_guides:
                    seen_guides.add(g_url)
                    guide_urls.append(g_url)
        except Exception as e:
            dur = time.monotonic() - started
            logger.warning(f"{TAG} Steam guide search error: url={search_url} status=ERR duration={dur:.2f}s ({e})")

    # Also scan Vietnamese-tagged guides on Steam's top-played games (covers non-Workshop games)
    top_data = _http_get_json(
        session,
        "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/",
        headers=headers,
    )
    ranks = ((top_data or {}).get("response") or {}).get("ranks") if isinstance(top_data, dict) else None
    if isinstance(ranks, list):
        scanned_apps = 0
        for r_item in ranks:
            if scanned_apps >= 20 or len(guide_urls) >= max_guides * 2:
                break
            aid = int((r_item or {}).get("appid") or 0)
            if aid <= 0 or aid in known_ids:
                continue
            scanned_apps += 1
            app_guides_url = f"https://steamcommunity.com/app/{aid}/guides/"
            started = time.monotonic()
            try:
                resp = session.get(
                    app_guides_url,
                    headers=headers,
                    params={"browsesort": "toprated", "browsefilter": "toprated", "requiredtags[0]": "vietnamese", "p": 1},
                    timeout=HTTP_TIMEOUT,
                )
                if resp.status_code == 200:
                    for m in _STEAM_GUIDE_URL_RE.finditer(resp.text):
                        g_url = m.group(0)
                        if g_url not in seen_guides:
                            seen_guides.add(g_url)
                            guide_urls.append(g_url)
            except Exception as e:
                dur = time.monotonic() - started
                logger.warning(f"{TAG} Steam app guides error: url={app_guides_url} status=ERR duration={dur:.2f}s ({e})")

    candidates: list[RawCandidate] = []
    for g_url in guide_urls[:max_guides]:
        started = time.monotonic()
        try:
            resp = session.get(g_url, headers=headers, timeout=HTTP_TIMEOUT)
            dur = time.monotonic() - started
            if resp.status_code != 200:
                logger.warning(f"{TAG} Steam guide fetch failed: url={g_url} status={resp.status_code} duration={dur:.2f}s")
                continue
            body = resp.text
        except Exception as e:
            dur = time.monotonic() - started
            logger.warning(f"{TAG} Steam guide fetch error: url={g_url} status=ERR duration={dur:.2f}s ({e})")
            continue

        if _PASSWORD_HINT_RE.search(body):
            logger.debug(f"{TAG} Skipping Steam guide '{g_url}' due to archive password requirement")
            continue

        app_m = _STEAM_APP_RE.search(body)
        if not app_m:
            continue
        appid = int(app_m.group(1))
        if appid in known_ids:
            continue

        links = _unwrap_steam_links(body)
        if not links:
            continue

        title_m = re.search(r'<div class="workshopItemTitle">\s*([^<]+?)\s*</div>', body)
        if not title_m:
            title_m = re.search(r"<title>\s*(?:Steam Community\s*::\s*Guide\s*::\s*)?([^<]+?)\s*</title>", body)
        guide_title = html.unescape(title_m.group(1)).strip() if title_m else ""
        ascii_title = _strip_accents(guide_title).lower()
        if guide_title and not any(k in ascii_title for k in ("viet hoa", "viethoa", "tieng viet", "vietnamese")):
            continue

        author_m = re.search(r"steamcommunity\.com/(?:id|profiles)/([^/\"'?<\s]+)", body)
        team = author_m.group(1) if author_m else "Steam Community VN"

        candidates.append(
            RawCandidate(
                source="steam_guide",
                raw_title=extract_clean_game_title(guide_title) or f"SteamApp {appid}",
                download_url=links[0],
                team=team,
                team_url=g_url,
                version="1.0",
                steam_appid=appid,
                notes=guide_title[:200] or "Ban Viet Hoa tu Steam Community Guide",
            )
        )

    logger.info(f"{TAG} Steam Guides discovery found {len(candidates)} candidates (scanned {min(len(guide_urls), max_guides)} guides)")
    return candidates


def resolve_steam_game(
    session: requests.Session,
    raw_title: str,
    hint_appid: int | None = None,
    cache: dict[str, tuple[int, str] | None] | None = None,
) -> tuple[int, str] | None:
    """Resolve and verify canonical Steam (appid, name) for a candidate game."""
    memo = cache if cache is not None else {}
    cache_key = f"id:{hint_appid}" if hint_appid else f"q:{raw_title.strip().lower()}"
    if cache_key in memo:
        return memo[cache_key]

    headers = {"User-Agent": USER_AGENT}
    if hint_appid and hint_appid > 0:
        details = _http_get_json(
            session,
            "https://store.steampowered.com/api/appdetails",
            headers=headers,
            params={"appids": str(hint_appid), "l": "english", "cc": "US"},
        )
        app_block = (details or {}).get(str(hint_appid)) if isinstance(details, dict) else None
        if isinstance(app_block, dict) and app_block.get("success") and isinstance(app_block.get("data"), dict):
            gdata = app_block["data"]
            if gdata.get("type") == "game" and gdata.get("name"):
                res = (int(hint_appid), str(gdata["name"]).strip())
                memo[cache_key] = res
                return res
        memo[cache_key] = None
        return None

    clean_q = extract_clean_game_title(raw_title)
    if len(clean_q) < 3:
        memo[cache_key] = None
        return None

    search = _http_get_json(
        session,
        "https://store.steampowered.com/api/storesearch/",
        headers=headers,
        params={"term": clean_q, "l": "english", "cc": "US"},
    )
    items = search.get("items") if isinstance(search, dict) else None
    if not isinstance(items, list):
        memo[cache_key] = None
        return None

    for item in items[:5]:
        if not isinstance(item, dict):
            continue
        appid = int(item.get("id") or 0)
        name = str(item.get("name") or "").strip()
        if appid <= 0 or not name:
            continue
        if not titles_match_strictly(clean_q, name):
            continue
        verified = resolve_steam_game(session, name, hint_appid=appid, cache=memo)
        if verified is not None:
            memo[cache_key] = verified
            return verified

    memo[cache_key] = None
    return None


def _detect_archive_kind(magic: bytes, url: str) -> str | None:
    if magic.startswith(b"PK\x03\x04"):
        return "zip"
    if magic.startswith(b"7z\xbc\xaf\x27\x1c"):
        return "7z"
    if magic.startswith(b"Rar!\x1a\x07"):
        return "rar"
    if magic.startswith(b"\x1f\x8b"):
        return "tgz"
    return None


def _list_archive_members(archive_path: str, kind: str) -> tuple[bool, list[str]]:
    """Return (is_safe_and_unencrypted, relative_file_paths) without extracting untrusted files."""
    members: list[str] = []
    if kind == "zip":
        try:
            with zipfile.ZipFile(archive_path, "r") as zf:
                for info in zf.infolist():
                    if info.flag_bits & 0x1:
                        logger.warning(f"{TAG} Rejecting password-encrypted ZIP archive: {archive_path}")
                        return False, []
                    if info.is_dir():
                        continue
                    members.append(info.filename.replace("\\", "/"))
            return True, members
        except Exception as e:
            logger.warning(f"{TAG} Invalid ZIP archive '{archive_path}': {e}")
            return False, []

    if kind == "tgz":
        try:
            with tarfile.open(archive_path, "r:*") as tf:
                for m in tf.getmembers():
                    if m.issym() or m.islnk():
                        logger.warning(f"{TAG} Rejecting symlink-containing TAR archive: {archive_path}")
                        return False, []
                    if m.isfile():
                        members.append(m.name.replace("\\", "/"))
            return True, members
        except Exception as e:
            logger.warning(f"{TAG} Invalid TAR.GZ archive '{archive_path}': {e}")
            return False, []

    seven_z = shutil.which("7z") or shutil.which("7zz")
    if not seven_z:
        logger.warning(f"{TAG} Skipping {kind} member inspection (7z not installed on host)")
        return False, []

    try:
        proc = subprocess.run(
            [seven_z, "l", "-slt", "-ba", archive_path],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if proc.returncode != 0:
            logger.warning(f"{TAG} 7z failed listing '{archive_path}' (rc={proc.returncode})")
            return False, []
        cur_path = ""
        cur_dir = False
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                if cur_path and not cur_dir:
                    members.append(cur_path.replace("\\", "/"))
                cur_path = ""
                cur_dir = False
                continue
            if line.startswith("Path = "):
                cur_path = line[len("Path = ") :].strip()
            elif line.startswith("Folder = +") or (line.startswith("Attributes = ") and "D" in line.split("=", 1)[1]):
                cur_dir = True
            elif line.startswith("Encrypted = +"):
                logger.warning(f"{TAG} Rejecting encrypted {kind} archive: {archive_path}")
                return False, []
        if cur_path and not cur_dir:
            members.append(cur_path.replace("\\", "/"))
        return True, members
    except Exception as e:
        logger.warning(f"{TAG} Error inspecting {kind} archive '{archive_path}': {e}")
        return False, []


def analyze_archive_members(members: list[str]) -> tuple[bool, int]:
    """Validate archive file paths and infer strip_components (0 or 1)."""
    if not members:
        return False, 0

    payload_files: list[list[str]] = []
    for raw in members:
        norm = raw.replace("\\", "/").strip()
        if not norm or "\x00" in norm or norm.startswith("/") or ":" in norm.split("/")[0]:
            return False, 0
        parts = [p for p in norm.split("/") if p and p != "."]
        if not parts or any(p == ".." for p in parts):
            return False, 0

        leaf_low = parts[-1].lower()
        ext = os.path.splitext(leaf_low)[1]
        if ext in DOC_OR_NOISE_EXTS or leaf_low in {"readme", "license", "changelog"}:
            continue
        payload_files.append(parts)

    if not payload_files:
        return False, 0

    # Reject archives whose payload consists exclusively of .exe / .msi / .bat setup wizards
    non_installer_files = [
        parts for parts in payload_files if os.path.splitext(parts[-1].lower())[1] not in INSTALLER_BINARY_EXTS
    ]
    if not non_installer_files:
        return False, 0

    # Check if every non-doc payload file sits inside a single wrapper directory
    top_dirs = {parts[0] for parts in non_installer_files if len(parts) >= 2}
    has_root_level_payload = any(len(parts) == 1 for parts in non_installer_files)
    if not has_root_level_payload and len(top_dirs) == 1:
        wrapper = next(iter(top_dirs)).lower()
        if wrapper not in GAME_ROOT_KNOWN_DIRS and not wrapper.endswith("_data"):
            second_level = {parts[1].lower() for parts in non_installer_files if len(parts) >= 2}
            if any(
                seg in GAME_ROOT_KNOWN_DIRS
                or seg.endswith("_data")
                or seg.endswith((".pak", ".utoc", ".ucas", ".rpf", ".archive", ".dll", ".pck", ".assets", ".bundle"))
                for seg in second_level
            ):
                return True, 1

    return True, 0


def _open_candidate_stream(session: requests.Session, url: str) -> requests.Response:
    headers = {"User-Agent": USER_AGENT}
    gd = _GDRIVE_ID_RE.search(url)
    if not gd:
        return session.get(url, stream=True, timeout=HTTP_TIMEOUT, headers=headers, allow_redirects=True)

    fid = gd.group(1)
    direct = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    resp = session.get(direct, stream=True, timeout=HTTP_TIMEOUT, headers=headers, allow_redirects=True)
    if resp.status_code == 200 and "text/html" in (resp.headers.get("Content-Type") or "").lower():
        html_body = resp.text
        resp.close()
        uuid_m = re.search(r'name="uuid"\s+value="([^"]+)"', html_body)
        if uuid_m:
            confirm_url = f"{direct}&uuid={uuid_m.group(1)}"
            resp = session.get(confirm_url, stream=True, timeout=HTTP_TIMEOUT, headers=headers, allow_redirects=True)
    return resp


def probe_and_inspect_archive(
    session: requests.Session,
    raw_url: str,
    *,
    max_inspect_bytes: int = DEFAULT_MAX_INSPECT_BYTES,
) -> VerifiedArchive | None:
    """Stream, hash, and inspect a candidate archive URL before trusting it in the catalog."""
    norm = normalize_download_url(raw_url)
    if not norm:
        logger.warning(f"{TAG} Rejected untrusted or non-HTTPS download URL: {raw_url}")
        return None

    clean_url, dl_type = norm
    started = time.monotonic()
    tmp_path = ""
    try:
        with _open_candidate_stream(session, clean_url) as resp:
            dur = time.monotonic() - started
            if resp.status_code != 200:
                logger.warning(
                    f"{TAG} Candidate probe failed: url={clean_url} status={resp.status_code} duration={dur:.2f}s"
                )
                return None

            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "text/html" in ctype or "application/json" in ctype:
                logger.warning(f"{TAG} Rejected non-binary Content-Type '{ctype}' from {clean_url}")
                return None

            clen_raw = resp.headers.get("Content-Length") or ""
            if clen_raw.isdigit() and int(clen_raw) > max_inspect_bytes:
                logger.warning(
                    f"{TAG} Skipping oversized archive ({int(clen_raw)} bytes > {max_inspect_bytes}) at {clean_url}"
                )
                return None

            hasher = hashlib.sha256()
            total = 0
            kind: str | None = None

            fd, tmp_path = tempfile.mkstemp(prefix="vh_crawl_", suffix=".bin")
            with os.fdopen(fd, "wb") as out_f:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue
                    if kind is None:
                        kind = _detect_archive_kind(chunk[:16], clean_url)
                        if kind is None:
                            logger.warning(f"{TAG} Rejected non-archive magic header from {clean_url}")
                            return None
                    total += len(chunk)
                    if total > max_inspect_bytes:
                        logger.warning(f"{TAG} Stream exceeded max_inspect_bytes ({max_inspect_bytes}): {clean_url}")
                        return None
                    out_f.write(chunk)
                    hasher.update(chunk)

        if total < MIN_ARCHIVE_BYTES or kind is None:
            logger.warning(f"{TAG} Rejected tiny/empty file ({total} bytes) from {clean_url}")
            return None

        ok_list, members = _list_archive_members(tmp_path, kind)
        if not ok_list:
            return None

        is_valid_payload, strip_components = analyze_archive_members(members)
        if not is_valid_payload:
            logger.warning(f"{TAG} Rejected unsafe or installer-only archive structure from {clean_url}")
            return None

        return VerifiedArchive(
            download_url=clean_url,
            download_type=dl_type,
            sha256=hasher.hexdigest().lower(),
            size_bytes=total,
            strip_components=strip_components,
        )
    except Exception as e:
        dur = time.monotonic() - started
        logger.warning(f"{TAG} Candidate stream error: url={clean_url} status=ERR duration={dur:.2f}s ({e})")
        return None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def ensure_backward_compat_fields(catalog_data: dict[str, Any]) -> bool:
    """Ensure every translation includes flat download_url alongside nested download.primary.url."""
    changed = False
    raw_cat = catalog_data.get("catalog")
    if not isinstance(raw_cat, dict):
        return False
    for entry in raw_cat.values():
        if not isinstance(entry, dict):
            continue
        for tr in entry.get("translations") or []:
            if not isinstance(tr, dict):
                continue
            dl = tr.get("download")
            prim = dl.get("primary") if isinstance(dl, dict) else None
            prim_url = str((prim.get("url") if isinstance(prim, dict) else None) or "").strip()
            if prim_url and tr.get("download_url") != prim_url:
                tr["download_url"] = prim_url
                changed = True
    return changed


def refresh_existing_github_entries(
    catalog_data: dict[str, Any],
    session: requests.Session,
    *,
    max_inspect_bytes: int = DEFAULT_MAX_INSPECT_BYTES,
) -> int:
    """Check existing GitHub-backed catalog translations for newer release tags."""
    raw_cat = catalog_data.get("catalog")
    if not isinstance(raw_cat, dict):
        return 0

    headers = _github_headers()
    updated_count = 0

    for entry in raw_cat.values():
        if not isinstance(entry, dict):
            continue
        for tr in entry.get("translations") or []:
            if not isinstance(tr, dict):
                continue
            dl = tr.get("download") if isinstance(tr.get("download"), dict) else {}
            prim = dl.get("primary") if isinstance(dl.get("primary"), dict) else {}
            prim_url = str(prim.get("url") or tr.get("download_url") or "")
            if "/releases/download/" not in prim_url:
                continue
            m = _GH_REPO_RE.match(prim_url)
            if not m:
                continue
            full_name = f"{m.group(1)}/{m.group(2)}"
            latest = _http_get_json(
                session,
                f"https://api.github.com/repos/{full_name}/releases/latest",
                headers=headers,
            )
            if not isinstance(latest, dict) or latest.get("draft"):
                continue
            latest_tag = str(latest.get("tag_name") or "").strip()
            clean_ver = latest_tag.lstrip("vV") or latest_tag
            cur_ver = str(tr.get("version") or "").strip()
            if not latest_tag or clean_ver == cur_ver or latest_tag in prim_url:
                continue

            asset = _pick_best_release_asset(latest.get("assets") or [], max_inspect_bytes)
            if not asset:
                continue
            new_url = str(asset.get("browser_download_url") or "")
            if not new_url or new_url == prim_url:
                continue

            verified = probe_and_inspect_archive(session, new_url, max_inspect_bytes=max_inspect_bytes)
            if verified is None:
                continue

            tr["version"] = clean_ver
            tr["download_url"] = verified.download_url
            prim["type"] = verified.download_type
            prim["url"] = verified.download_url
            prim["sha256"] = verified.sha256
            prim["size_bytes"] = verified.size_bytes
            updated_count += 1
            logger.info(
                f"{TAG} Auto-updated '{entry.get('canonical_title')}' ({full_name}) -> version {clean_ver}"
            )

    return updated_count


def merge_verified_candidate(
    catalog_data: dict[str, Any],
    candidate: RawCandidate,
    steam_appid: int,
    canonical_title: str,
    verified: VerifiedArchive,
) -> bool:
    """Insert a verified localization entry if the game AppID/key is not already covered."""
    raw_cat = catalog_data.setdefault("catalog", {})

    # Skip if Steam AppID already exists in catalog (preserve curated/existing entries)
    for existing in raw_cat.values():
        if isinstance(existing, dict) and int(existing.get("steam_appid") or 0) == steam_appid:
            return False

    entry_id = slugify_game_id(canonical_title)
    if entry_id in raw_cat:
        entry_id = f"{entry_id}_{steam_appid}"

    team_slug = slugify_game_id(candidate.team)[:20] or "community"
    tr_id = f"{entry_id}_{team_slug}"
    online_slug = entry_id.replace("_", "-")

    aliases: list[str] = []
    if candidate.raw_title and candidate.raw_title.lower() != canonical_title.lower():
        aliases.append(candidate.raw_title)

    raw_cat[entry_id] = {
        "id": entry_id,
        "canonical_title": canonical_title,
        "aliases": aliases,
        "steam_appid": steam_appid,
        "online_fix_ids": [online_slug, str(steam_appid)],
        "translations": [
            {
                "id": tr_id,
                "team": candidate.team,
                "team_url": candidate.team_url,
                "version": candidate.version or "1.0",
                "game_version_min": "1.0",
                "game_version_max": "",
                "notes": candidate.notes or f"Ban Viet Hoa cho {canonical_title}",
                "download_url": verified.download_url,
                "download": {
                    "primary": {
                        "type": verified.download_type,
                        "url": verified.download_url,
                        "sha256": verified.sha256,
                        "size_bytes": verified.size_bytes,
                    },
                    "mirrors": [],
                },
                "install_rules": {
                    "type": "extract_and_copy",
                    "strip_components": verified.strip_components,
                    "target_subdir": "",
                    "backup_patterns": [],
                },
                "is_active": True,
            }
        ],
    }
    logger.info(
        f"{TAG} Added new game '{canonical_title}' (AppID={steam_appid}, source={candidate.source}, "
        f"size={verified.size_bytes}B, strip={verified.strip_components})"
    )
    return True


def run_crawler(
    catalog_path: str,
    *,
    mirror_paths: list[str] | None = None,
    max_new_entries: int = 15,
    max_inspect_bytes: int = DEFAULT_MAX_INSPECT_BYTES,
    dry_run: bool = False,
    session: requests.Session | None = None,
) -> tuple[bool, int, int]:
    """Execute full crawl-validate-merge pipeline on vietnamese_catalog.json.

    Returns:
        Tuple (changed: bool, added_count: int, updated_count: int).
    """
    started = time.monotonic()
    logger.info(f"{TAG} Starting Vietnamese localization crawl on '{catalog_path}' (dry_run={dry_run})")

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog_data = json.load(f)

    if not isinstance(catalog_data, dict) or not isinstance(catalog_data.get("catalog"), dict):
        raise ValueError(f"Invalid catalog JSON structure in {catalog_path}")

    own_session = session is None
    http = session or requests.Session()
    added_count = 0
    updated_count = 0
    compat_changed = ensure_backward_compat_fields(catalog_data)

    try:
        try:
            updated_count += refresh_existing_github_entries(
                catalog_data, http, max_inspect_bytes=max_inspect_bytes
            )
        except Exception as e:
            logger.error(f"{TAG} Error refreshing existing GitHub entries: {e}", exc_info=True)

        existing_appids = {
            int(entry.get("steam_appid") or 0)
            for entry in catalog_data["catalog"].values()
            if isinstance(entry, dict) and int(entry.get("steam_appid") or 0) > 0
        }

        raw_candidates: list[RawCandidate] = []
        try:
            raw_candidates.extend(discover_github_candidates(http, max_inspect_bytes=max_inspect_bytes))
        except Exception as e:
            logger.error(f"{TAG} Error during GitHub candidate discovery: {e}", exc_info=True)

        try:
            raw_candidates.extend(
                discover_steam_guide_candidates(http, existing_appids=existing_appids)
            )
        except Exception as e:
            logger.error(f"{TAG} Error during Steam Guide candidate discovery: {e}", exc_info=True)

        steam_cache: dict[str, tuple[int, str] | None] = {}
        seen_urls: set[str] = set()

        for cand in raw_candidates:
            if added_count >= max_new_entries:
                break
            if cand.download_url in seen_urls:
                continue
            seen_urls.add(cand.download_url)

            if cand.steam_appid and cand.steam_appid in existing_appids:
                continue

            resolved = resolve_steam_game(
                http, cand.raw_title, hint_appid=cand.steam_appid, cache=steam_cache
            )
            if resolved is None:
                logger.debug(f"{TAG} Could not map '{cand.raw_title}' to a verified Steam game")
                continue

            appid, canonical_title = resolved
            if appid in existing_appids:
                continue

            verified = probe_and_inspect_archive(
                http, cand.download_url, max_inspect_bytes=max_inspect_bytes
            )
            if verified is None:
                continue

            if merge_verified_candidate(catalog_data, cand, appid, canonical_title, verified):
                existing_appids.add(appid)
                added_count += 1
    finally:
        if own_session:
            http.close()

    changed = (added_count > 0) or (updated_count > 0) or compat_changed
    dur = time.monotonic() - started

    if not changed:
        logger.info(
            f"{TAG} Crawl finished in {dur:.2f}s: no catalog changes ({len(catalog_data['catalog'])} total games)"
        )
        return False, 0, 0

    if added_count > 0 or updated_count > 0:
        catalog_data["version"] = int(catalog_data.get("version") or 1) + 1
        catalog_data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not dry_run:
        serialized = json.dumps(catalog_data, ensure_ascii=False, indent=2) + "\n"
        targets = [catalog_path] + list(mirror_paths or [])
        for path in targets:
            parent = os.path.dirname(os.path.abspath(path))
            if parent:
                os.makedirs(parent, exist_ok=True)
            tmp = f"{path}.tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write(serialized)
            os.replace(tmp, path)

    logger.info(
        f"{TAG} Crawl finished in {dur:.2f}s: added={added_count}, updated={updated_count}, "
        f"compat_fixed={compat_changed}, version={catalog_data.get('version')}, total={len(catalog_data['catalog'])}"
    )
    return True, added_count, updated_count


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Crawl and validate public Vietnamese game localizations.")
    ap.add_argument("--catalog", required=True, help="Primary vietnamese_catalog.json path")
    ap.add_argument(
        "--mirror",
        action="append",
        default=[],
        help="Additional catalog path(s) to mirror atomically (e.g. release-candidates/vietnamese_catalog.json)",
    )
    ap.add_argument("--max-new", type=int, default=15, help="Maximum new games to add per run")
    ap.add_argument("--dry-run", action="store_true", help="Scan and validate without writing files")
    args = ap.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    try:
        run_crawler(
            args.catalog,
            mirror_paths=args.mirror,
            max_new_entries=args.max_new,
            dry_run=args.dry_run,
        )
        return 0
    except Exception as e:
        logger.error(f"{TAG} Fatal crawler failure: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

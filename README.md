# scrapling-browse

An [Openclaw](https://openclaw.org) skill for web scraping, powered by [Scrapling](https://github.com/D4Vinci/Scrapling). Three scraping modes cover everything from simple HTTP fetches to full browser automation with anti-bot bypass.

## Scripts

| Script | Fetcher | Use case |
|---|---|---|
| `scrape.py` | `Fetcher` | Fast HTTP fetch. Plain public pages, JSON endpoints. |
| `scrape_stealth.py` | `StealthyFetcher` | Stealth headless browser. Bypasses Cloudflare and fingerprinting. |
| `scrape_dynamic.py` | `DynamicFetcher` | Full browser automation with JS rendering, session persistence, and network idle detection. |

All scripts output JSON to stdout and accept `--css` or `--xpath` selectors.

## Usage

```bash
# Basic fetch
python scripts/scrape.py --url "https://example.com" --css "h1" --text

# Stealth mode (Cloudflare bypass)
python scripts/scrape_stealth.py --url "https://protected-site.com" --css ".title" --text --solve-cloudflare

# Stealth with delay
python scripts/scrape_stealth.py --url "https://linkedin.com/in/someone" --css ".top-card" --text --delay 3

# Dynamic with network idle wait
python scripts/scrape_dynamic.py --url "https://spa-site.com" --css ".row" --wait-for-idle

# Dynamic with session persistence
python scripts/scrape_dynamic.py --url "https://login-required.com" --css ".data" --session ./session.json
```

## Options

**All scripts:**
- `--url` — target URL (required)
- `--css` / `--xpath` — element selector (one required)
- `--text` — extract text content only (default: returns HTML)

**scrape_stealth.py** adds:
- `--delay` — seconds to wait after page load
- `--solve-cloudflare` — enable Cloudflare challenge solving
- `--headless` / `--no-headless` — toggle headless mode (default: headless)

**scrape_dynamic.py** adds:
- `--wait-for-idle` — wait for network idle before extracting
- `--session` — path to a `storage_state` JSON file for session persistence
- `--headless` / `--no-headless` — toggle headless mode (default: headless)

## Install

```bash
pip install scrapling
```

For stealth and dynamic modes, Scrapling will prompt you to install browser dependencies on first run.

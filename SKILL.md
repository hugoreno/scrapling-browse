Use this skill to fetch or scrape any web page. Pick the right mode:

- **scrape.py** - fast, no browser. Use for plain public pages (ACRIS static pages, JSON endpoints).
- **scrape_stealth.py** - stealth headless browser, bypasses Cloudflare and fingerprinting. Use for LinkedIn, PropertyShark, any site with bot protection.
- **scrape_dynamic.py** - full browser automation with JS rendering, form interaction, and session persistence. Use for multi-step flows or login-required pages (broker.olr.com, ACRIS property search).

All scripts accept `--url`, `--css` or `--xpath`, and `--text` (extract text only). Output is JSON to stdout.

```
python skills/scrapling-browse/scripts/scrape.py --url "https://target.com" --css ".item" --text
python skills/scrapling-browse/scripts/scrape_stealth.py --url "https://linkedin.com/..." --css ".title" --text --delay 3
python skills/scrapling-browse/scripts/scrape_dynamic.py --url "https://target.com" --css ".row" --wait-for-idle --session ./session.json
```

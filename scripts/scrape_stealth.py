#!/usr/bin/env python3
import argparse
import json
import sys
import time

from scrapling.fetchers import StealthyFetcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stealth scraper using Scrapling StealthyFetcher")
    parser.add_argument("--url", required=True, help="Target URL")
    selectors = parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--css", help="CSS selector")
    selectors.add_argument("--xpath", help="XPath selector")
    parser.add_argument("--text", action="store_true", help="Extract text only")
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds to sleep after fetch")
    parser.add_argument("--solve-cloudflare", action="store_true", help="Enable Cloudflare solving")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True, help="Run browser headless")
    return parser.parse_args()


def select_elements(page, css: str | None, xpath: str | None):
    if css:
        return page.css(css)
    return page.xpath(xpath)


def element_value(element, text_only: bool):
    if text_only:
        return getattr(element, "text", "")
    return getattr(element, "html", str(element))


def main() -> int:
    args = parse_args()
    try:
        page = StealthyFetcher.fetch(
            args.url,
            headless=args.headless,
            network_idle=True,
            solve_cloudflare=args.solve_cloudflare,
        )
        if args.delay > 0:
            time.sleep(args.delay)
        elements = select_elements(page, args.css, args.xpath)
        values = [element_value(element, args.text) for element in elements]
        print(json.dumps(values, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

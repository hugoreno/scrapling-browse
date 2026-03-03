#!/usr/bin/env python3
import argparse
import json
import sys

from scrapling.fetchers import Fetcher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fast HTTP scraper using Scrapling Fetcher")
    parser.add_argument("--url", required=True, help="Target URL")
    selectors = parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--css", help="CSS selector")
    selectors.add_argument("--xpath", help="XPath selector")
    parser.add_argument("--text", action="store_true", help="Extract text only")
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
        page = Fetcher.get(args.url, stealthy_headers=True)
        elements = select_elements(page, args.css, args.xpath)
        values = [element_value(element, args.text) for element in elements]
        print(json.dumps(values, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

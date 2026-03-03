#!/usr/bin/env python3
import argparse
import json
import sys

from scrapling.fetchers import DynamicFetcher, DynamicSession


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dynamic scraper using Scrapling DynamicFetcher")
    parser.add_argument("--url", required=True, help="Target URL")
    selectors = parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument("--css", help="CSS selector")
    selectors.add_argument("--xpath", help="XPath selector")
    parser.add_argument("--text", action="store_true", help="Extract text only")
    parser.add_argument("--wait-for-idle", action="store_true", help="Wait for network idle before returning")
    parser.add_argument("--session", help="Path to storage_state JSON file")
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
        if args.session:
            with DynamicSession(
                storage_state=args.session,
                headless=args.headless,
                network_idle=args.wait_for_idle,
            ) as session:
                page = session.fetch(args.url)
        else:
            page = DynamicFetcher.fetch(
                args.url,
                headless=args.headless,
                network_idle=args.wait_for_idle,
            )

        elements = select_elements(page, args.css, args.xpath)
        values = [element_value(element, args.text) for element in elements]
        print(json.dumps(values, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

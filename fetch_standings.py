"""Fetch a bfu-tournaments.com standings page, waiting out Cloudflare's JS challenge."""

import sys

from playwright.sync_api import sync_playwright

URL = "https://bfu-tournaments.com/tournaments/1/371?tid=261&season=1360&view=standings"


def fetch(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
        )
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Cloudflare's managed challenge redirects once it passes; wait for the
        # real page title to replace "Just a moment...".
        page.wait_for_function(
            "document.title !== 'Just a moment...'", timeout=30000
        )
        page.wait_for_load_state("networkidle")

        html = page.content()
        browser.close()
        return html


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else URL
    print(fetch(url))

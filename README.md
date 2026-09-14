# bfu-tournaments

Fetches pages from `bfu-tournaments.com` (the Bulgarian Football Union tournaments
site). The site sits behind a Cloudflare "managed challenge" that blocks plain
HTTP clients (curl, requests, etc.) even with a browser User-Agent set, since it
requires actual JavaScript execution to pass. This uses Playwright to drive a
real (headless) Chromium browser instead, which solves the challenge like a
normal visitor would.

## Setup

Requires Python 3 and `virtualenv`.

```bash
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
source .venv/bin/activate
python fetch_standings.py "https://bfu-tournaments.com/tournaments/1/371?tid=261&season=1360&view=standings"
```

If no URL is passed, it defaults to the standings page hardcoded in the script.

The script prints the fully rendered page HTML (post-challenge) to stdout. To
extract readable text instead of raw HTML, pipe it through BeautifulSoup, e.g.:

```bash
python fetch_standings.py > page.html
python -c "
from bs4 import BeautifulSoup
with open('page.html') as f:
    print(BeautifulSoup(f.read(), 'html.parser').get_text('\n', strip=True))
"
```

## Notes

- `tid`, `season`, and `view` are query params on the URL — swap them to target
  a different tournament/season/view.
- The script waits for the page `<title>` to stop being "Just a moment..."
  before returning, which is Cloudflare's challenge placeholder title.

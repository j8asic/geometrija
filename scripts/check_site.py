#!/usr/bin/env python3
"""Check rendered local links and basic media accessibility; no network/dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import csv
import sys
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.errors = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        key = "href" if tag in ("a", "link") else "src"
        if tag in ("a", "link", "img", "script", "iframe") and a.get(key):
            self.links.append(a[key])
        if tag == "img" and "alt" not in a:
            self.errors.append("Image has no alt attribute")
        if tag == "iframe" and not a.get("title", "").strip():
            self.errors.append("Iframe has no accessible title")


def check(root):
    root = root.resolve()
    required = ["index.html", "exercises/01-first-steps.html", "exercises/02-hull-modelling.html",
                "resources.html", "search.json", "downloads/practice-body-plan.png",
                "downloads/practice-body-plan.svg", "downloads/practice-offsets.csv",
                "downloads/practice-stations.csv"]
    errors = [f"Missing required output: {p}" for p in required if not (root/p).is_file()]
    pages = {p.resolve(): Page(p) for p in root.rglob("*.html")}
    if not pages:
        errors.append("No HTML pages found")
    for path, page in pages.items():
        label = path.relative_to(root)
        errors.extend(f"{label}: {e}" for e in page.errors)
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            rel = unquote(url.path)
            if rel.startswith("/geometrija/"):
                rel = rel[len("/geometrija"):]
            target = ((root / rel.lstrip("/")) if rel.startswith("/")
                      else (path.parent / rel if rel else path)).resolve()
            if not target.is_relative_to(root):
                errors.append(f"{label}: link leaves output directory: {href}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{label}: missing link target: {href}")
            elif url.fragment and target.suffix == ".html":
                fragment = unquote(url.fragment)
                if target in pages and fragment not in pages[target].ids:
                    errors.append(f"{label}: missing fragment: {href}")
    png = root / "downloads/practice-body-plan.png"
    if png.is_file() and not png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append("Practice PNG has an invalid signature")
    offsets = root / "downloads/practice-offsets.csv"
    if offsets.is_file():
        with offsets.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if len(rows) != 35 or {r["station"] for r in rows} != {f"S{i}" for i in range(5)}:
            errors.append("Practice offsets must contain 7 points for each of 5 stations")
    if errors:
        print("Site validation failed:\n" + "\n".join(sorted(set(errors))), file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} HTML pages; local links/fragments, media attributes and practice downloads")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_site.py _book")
    raise SystemExit(check(Path(sys.argv[1])))

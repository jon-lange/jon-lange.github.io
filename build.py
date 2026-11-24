#!/usr/bin/env python3
"""Build the personal terminal and its historical research archive.

    python3 build.py            # write index.html and archive.html
    python3 build.py --check    # fail if either generated page is not current

The terminal's initial About output is generated from its own view-about
template. Historical not-evidence records are generated from register.json
into a separate, fully static archive; verdicts are not entered separately.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
DATA = HERE / "register.json"
SOURCE = HERE / "template.html"
OUT = HERE / "index.html"
ARCHIVE_SOURCE = HERE / "archive.template.html"
ARCHIVE_OUT = HERE / "archive.html"

VERDICT = {
    "central-claim-failed": ("failed", "did not hold"),
    "narrowed": ("narrowed", "held, narrowed"),
    "confirmed": ("confirmed", "held"),
}


RECORD_TITLES = {
    "01": "Answering without retrieved evidence",
    "02": "Whole-class input refusal",
    "03": "A six-step prompt defense",
    "04": "Two classes of prompt injection",
    "05": "Judge family and answer order",
    "06": "Changing scorecard weights",
    "07": "Refusals across model versions",
    "08": "Reusing a remembered figure",
    "09": "Prompt injection through images",
    "10": "Transcribing inputs with no speech",
    "11": "An absence test under mutation",
    "12": "Re-identifying a sanitized release",
}


def strip_md(text: str) -> str:
    """Escape source prose while retaining emphasis on measured figures."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    parts, out = re.split(r"`([^`]+)`", text), []
    for i, part in enumerate(parts):
        out.append(f"<strong>{html.escape(part)}</strong>" if i % 2 else html.escape(part))
    return "".join(out)


def register_rows(rows: list[dict]) -> str:
    """Render each source verdict as a keyboard-accessible disclosure."""
    out = []
    for r in rows:
        cls, verdict = VERDICT[r["adj"]]
        out.append(
            f'<details class="study study--{cls}"><summary>'
            f'<span class="study-number">{html.escape(r["n"])}</span>'
            f'<span class="study-name">{html.escape(RECORD_TITLES.get(r["n"], r["name"]))}</span>'
            f'<span class="verdict">{verdict}</span>'
            f'</summary><div class="study-body">'
            f'<dl><div><dt>Original title</dt><dd>{html.escape(r["name"])}</dd></div>'
            f'<div><dt>Recorded verdict</dt><dd>{verdict}</dd></div>'
            f'<div><dt>Original boundary</dt><dd>{html.escape(r["refuses"])}</dd></div>'
            f'<div><dt>Measured</dt><dd>{strip_md(r["measured"])}</dd></div>'
            f'<div><dt>Result</dt><dd>{strip_md(r["result"])}</dd></div></dl>'
            f'<a href="https://github.com/jon-lange/not-evidence/blob/main/'
            f'specimens/{r["spec"]}/RESULTS.md">Read study {html.escape(r["n"])} results '
            f'</a></div></details>'
        )
    return "\n".join(out)


def build() -> dict[Path, str]:
    """Generate both committed pages from their respective source templates."""
    source = SOURCE.read_text(encoding="utf-8")
    if source.count("$about") != 1:
        raise ValueError("template.html must contain exactly one $about placeholder")
    about = re.findall(
        r'<template\b[^>]*\bid\s*=\s*["\']view-about["\'][^>]*>(.*?)</template\s*>',
        source,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if len(about) != 1:
        raise ValueError("template.html must contain exactly one view-about template")
    index = Template(source).substitute(about=about[0].strip())
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 12:
        raise ValueError("register.json must retain its twelve historical records")
    if any(not isinstance(row, dict) or row.get("adj") not in VERDICT for row in rows):
        raise ValueError("register.json contains an unknown historical verdict")
    if sorted(row.get("n", "") for row in rows) != sorted(RECORD_TITLES):
        raise ValueError("register.json must contain each historical record 01–12 once")
    counts = {v: sum(1 for r in rows if r["adj"] == k)
              for k, (v, _) in VERDICT.items()}
    archive = Template(ARCHIVE_SOURCE.read_text(encoding="utf-8")).substitute(
        rows=register_rows(rows),
        total=len(rows),
        failed=counts["failed"],
        narrowed=counts["narrowed"],
        confirmed=counts["confirmed"],
        survived=counts["narrowed"] + counts["confirmed"],
    )
    return {OUT: index, ARCHIVE_OUT: archive}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        pages = build()
    except (ValueError, KeyError, OSError) as error:
        print(f"BLOCKED - {error}")
        return 1
    if args.check:
        stale = False
        for path, page in pages.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != page:
                print(f"BLOCKED - {path.name} is not current. Run: python3 build.py")
                stale = True
            else:
                print(f"  {path.name} current")
        return int(stale)
    for path, page in pages.items():
        path.write_text(page, encoding="utf-8")
        print(f"  {path.name} written ({len(page):,} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


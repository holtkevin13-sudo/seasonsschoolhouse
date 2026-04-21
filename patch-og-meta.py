#!/usr/bin/env python3
"""
patch-og-meta.py
================

Normalizes Open Graph / Twitter Card meta tags across every .html page
in the Seasons Schoolhouse repo.

USAGE
-----
From the repo root:
    python3 patch-og-meta.py

WHAT IT DOES
------------
For each .html file in the current directory:

1. Replaces any og:image pointing at logo.png with og-image.png (absolute URL)
2. Replaces any twitter:image pointing at logo.png with og-image.png (absolute URL)
3. Inserts og:image:width (1200), og:image:height (630), and og:image:alt
   immediately after og:image, if not already present
4. For any page missing twitter:title / twitter:description / twitter:image,
   mirrors the og:title / og:description / og:image values into them

The script is IDEMPOTENT — safe to run multiple times. It only writes a file
if something actually changed.

REQUIREMENTS
------------
The og-image.png file must be uploaded to the repo root and deployed to
https://seasonsschoolhouse.org/og-image.png before this patch takes effect
in the wild.

AFTER RUNNING
-------------
1. git diff  # eyeball the changes
2. git add -A && git commit -m "Normalize OG/Twitter meta across all pages"
3. git push  # GitHub Pages will rebuild
4. Clear Facebook's cache for each page using the Sharing Debugger:
   https://developers.facebook.com/tools/debug/
"""

import os
import re
import sys

SITE_BASE = "https://seasonsschoolhouse.org"
OG_IMAGE_URL = f"{SITE_BASE}/og-image.png"
OG_IMAGE_ALT = (
    "Seasons Schoolhouse — Homeschool Enrichment Program, Flagler County, FL"
)

REQUIRED = [
    "og:title",
    "og:description",
    "og:image",
    "og:image:width",
    "og:image:height",
    "og:url",
    "og:type",
    "twitter:card",
    "twitter:image",
]


def patch(html: str) -> tuple[str, list[str]]:
    changes = []

    # 1. og:image → og-image.png (handle both relative and absolute-to-logo)
    new_html, n = re.subn(
        r'(<meta property="og:image" content=")'
        r'(?:https?://seasonsschoolhouse\.org/)?logo\.png'
        r'(" ?/?>)',
        rf"\1{OG_IMAGE_URL}\2",
        html,
    )
    if n:
        html = new_html
        changes.append(f"og:image → {OG_IMAGE_URL}")

    # 2. twitter:image → og-image.png
    new_html, n = re.subn(
        r'(<meta name="twitter:image" content=")'
        r'(?:https?://seasonsschoolhouse\.org/)?logo\.png'
        r'(" ?/?>)',
        rf"\1{OG_IMAGE_URL}\2",
        html,
    )
    if n:
        html = new_html
        changes.append(f"twitter:image → {OG_IMAGE_URL}")

    # 3. Insert og:image:width/height/alt after og:image if missing
    if "og:image:width" not in html:
        new_html, n = re.subn(
            r'(<meta property="og:image" content="[^"]+" ?/?>)',
            r"\1"
            '\n  <meta property="og:image:width" content="1200" />'
            '\n  <meta property="og:image:height" content="630" />'
            f'\n  <meta property="og:image:alt" content="{OG_IMAGE_ALT}" />',
            html,
            count=1,
        )
        if n:
            html = new_html
            changes.append("added og:image:width, og:image:height, og:image:alt")

    # 4. Fill in missing twitter:title/description/image by mirroring og values
    head = html[: html.find("</head>")] if "</head>" in html else html

    def find_meta(tag, source):
        pattern = rf'<meta\s+(?:property|name)="{re.escape(tag)}"\s+content="([^"]+)"'
        m = re.search(pattern, source)
        return m.group(1) if m else None

    og_title = find_meta("og:title", head)
    og_desc = find_meta("og:description", head)

    # insert missing twitter:title after twitter:card
    def insert_after_twitter_card(snippet, label):
        nonlocal html
        new_html, n = re.subn(
            r'(<meta name="twitter:card" content="[^"]+" ?/?>)',
            r"\1\n" + snippet,
            html,
            count=1,
        )
        if n:
            html = new_html
            changes.append(f"added {label}")

    if find_meta("twitter:title", head) is None and og_title:
        insert_after_twitter_card(
            f'  <meta name="twitter:title" content="{og_title}" />',
            "twitter:title",
        )
    if find_meta("twitter:description", head) is None and og_desc:
        insert_after_twitter_card(
            f'  <meta name="twitter:description" content="{og_desc}" />',
            "twitter:description",
        )
    if find_meta("twitter:image", head) is None:
        insert_after_twitter_card(
            f'  <meta name="twitter:image" content="{OG_IMAGE_URL}" />',
            "twitter:image",
        )

    return html, changes


def audit(html: str) -> list[str]:
    head = html[: html.find("</head>")] if "</head>" in html else html
    missing = []
    for tag in REQUIRED:
        pattern = rf'<meta\s+(?:property|name)="{re.escape(tag)}"\s+content="([^"]+)"'
        if not re.search(pattern, head):
            missing.append(tag)
    og_img_match = re.search(
        r'<meta property="og:image" content="([^"]+)"', head
    )
    if og_img_match:
        val = og_img_match.group(1)
        if not val.startswith("http"):
            missing.append(f"og:image is relative ({val}) — must be absolute")
        elif "logo.png" in val:
            missing.append(f"og:image still points to logo.png ({val})")
    return missing


def main():
    root = os.path.dirname(os.path.abspath(sys.argv[0]))
    # If the script is in repo root, walk . — otherwise let user cd first
    target_dir = os.getcwd()
    html_files = sorted(
        f for f in os.listdir(target_dir)
        if f.endswith(".html") and not f.startswith(".")
    )
    if not html_files:
        print(f"No .html files found in {target_dir}")
        return 1

    print(f"Patching {len(html_files)} HTML files in {target_dir}\n")
    any_changes = False
    for fn in html_files:
        path = os.path.join(target_dir, fn)
        with open(path, encoding="utf-8") as f:
            original = f.read()

        patched, changes = patch(original)

        if patched != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(patched)
            any_changes = True
            print(f"✓ {fn}")
            for c in changes:
                print(f"    - {c}")
        else:
            print(f"  {fn} (no changes)")

    # Final audit
    print("\nFinal audit:")
    all_clean = True
    for fn in html_files:
        path = os.path.join(target_dir, fn)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        issues = audit(html)
        if issues:
            all_clean = False
            print(f"  ✗ {fn}")
            for i in issues:
                print(f"      {i}")
        else:
            print(f"  ✓ {fn} — all 9 required tags present and valid")

    if any_changes:
        print("\nDone. Review with `git diff`, then commit & push.")
    else:
        print("\nNo changes made — all files already compliant.")
    return 0 if all_clean else 2


if __name__ == "__main__":
    sys.exit(main())

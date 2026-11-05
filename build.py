#!/usr/bin/env python3
"""Build the Listing Photo Basics static site from docs/ into site/.

Local-first: pure Python standard library plus the `markdown` package.
No network access, no external fonts, no CDNs.

Run:
    python3 build.py

Then open site/index.html in a browser.
"""

import html
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown as md
except ImportError:
    sys.exit(
        "The 'markdown' package is required but not installed.\n"
        "Install it with:  python3 -m pip install markdown"
    )

ROOT = Path(__file__).parent.resolve()
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# Pages in manual reading order, grouped for the sidebar.
PAGES = {
    "start": [
        ("index.md", "Listing Photo Basics"),
        ("01-corner-lab.md", "The Corner Lab"),
        ("02-light.md", "Light Without a Rig"),
    ],
    "the shots": [
        ("03-condition.md", "Honest Condition Shots"),
        ("04-backgrounds.md", "Backgrounds and Scale"),
        ("05-cleaning.md", "Before/After Cleaning"),
        ("06-editing.md", "Phone Editing Without Fakery"),
        ("07-marketplaces.md", "Per-Marketplace Size Habits"),
    ],
    "reference": [
        ("08-shot-lists.md", "Shot-List Cards"),
        ("09-editing-checklist.md", "Editing Checklist"),
        ("10-glossary.md", "Glossary"),
    ],
}

SIGNOFF_TEXT = (
    "Listing Photo Basics — a reseller's guide by Asdale Dynamics, LLC. "
    "MIT licensed; see LICENSE. Marketplace specs are summarized from "
    "public help pages; when they change, the platform wins."
)


def reading_order():
    return [entry for section in PAGES.values() for entry in section]


def title_from_h1(text):
    for line in text.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
    return None


def md_link_to_html(text):
    """Rewrite hrefs pointing at .md docs so they point at the built .html pages."""
    return re.sub(r'href="([0-9A-Za-z_.\-/]+)\.md"', r'href="\1.html"', text)


def nav_title(doc_name):
    for file, label in reading_order():
        if file == doc_name:
            return label
    return doc_name


def build_sidebar(current, order):
    out = ['<nav class="sidebar">',
           '<a class="site-title" href="index.html">Listing Photo Basics</a>']
    for section, entries in PAGES.items():
        out.append('<h2 class="sec">%s</h2>' % html.escape(section.title()))
        out.append("<ul>")
        for doc_file, label in entries:
            href = doc_file.replace(".md", ".html")
            cls = ' class="current"' if doc_file == current else ""
            out.append('<li><a%s href="%s">%s</a></li>'
                       % (cls, href, html.escape(label)))
        out.append("</ul>")
    out.append("</nav>")
    return "\n".join(out)


def build_pager(current, order):
    filenames = [file for file, _ in order]
    i = filenames.index(current)
    prev_entry = order[i - 1] if i > 0 else None
    next_entry = order[i + 1] if i + 1 < len(order) else None

    pager = ['<nav class="pager">']
    if prev_entry:
        pager.append('<a href="%s">&larr; %s</a>'
                     % (prev_entry[0].replace(".md", ".html"),
                        html.escape(prev_entry[1])))
    else:
        pager.append("<span></span>")
    if next_entry:
        pager.append('<a href="%s">%s &rarr;</a>'
                     % (next_entry[0].replace(".md", ".html"),
                        html.escape(next_entry[1])))
    else:
        pager.append("<span></span>")
    pager.append("</nav>")
    return "\n".join(pager)


def build_page(doc_file, label, order):
    text = (DOCS / doc_file).read_text(encoding="utf-8")
    title = title_from_h1(text) or label
    body = md.markdown(
        text,
        extensions=["tables", "sane_lists", "smarty", "fenced_code"],
    )
    body = md_link_to_html(body)
    # Render task-list checkboxes as symbols (no markdown 'pymdown' dependency).
    body = re.sub(r"<li>\[ \]", "<li>\u2610", body)
    body = re.sub(r"<li>\[[xX]\]", "<li>\u2611", body)

    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Listing Photo Basics</title>
<meta name="description" content="Small-business manual for resale listing photos that sell: light without a rig, honest condition shots, phone editing without fakery, and per-marketplace size habits.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="layout">
{sidebar}
<main>
<article>
{body}
</article>
{pager}
<div class="pagefooter">{signoff}</div>
</main>
</div>
</body>
</html>
""".format(
        title=html.escape(title),
        sidebar=build_sidebar(doc_file, order),
        body=body,
        pager=build_pager(doc_file, order),
        signoff=html.escape(SIGNOFF_TEXT),
    )

    out_file = SITE / doc_file.replace(".md", ".html")
    out_file.write_text(page, encoding="utf-8")
    return out_file.name, title


def main():
    order = reading_order()
    missing = [name for name, _ in order if not (DOCS / name).exists()]
    if missing:
        sys.exit("ERROR: pages in build order missing from docs/: "
                 + ", ".join(missing))

    known = {name for name, _ in order}
    strays = sorted(p.name for p in DOCS.glob("*.md") if p.name not in known)
    if strays:
        print("WARNING: docs not in build order (skipped): " + ", ".join(strays))

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    built = []
    for doc_file, label in order:
        out_name, title = build_page(doc_file, label, order)
        built.append(out_name)
        print("  site/%s  (%s)" % (out_name, title))

    (SITE / "style.css").write_text(CSS, encoding="utf-8")
    print("Built %d pages + style.css into site/" % len(built))
    print("Open site/index.html in a browser to read it.")


CSS = """\
:root {
  --ink: #26221c; --muted: #6b655c; --paper: #faf7f2; --card: #fff;
  --accent: #2e5f4f; --accent-soft: #e4efe9; --line: #e4ded4; --code-bg: #f1ede6;
}
* { box-sizing: border-box; }
html { font-size: 17px; }
body { margin: 0; font-family: Georgia, 'Times New Roman', serif;
  line-height: 1.6; color: var(--ink); background: var(--paper); }
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
h1, h2, h3, h4 { font-family: 'Gill Sans', 'Gill Sans MT', Verdana, sans-serif; line-height: 1.25; }
h1 { font-size: 1.9rem; margin: 0.2rem 0 1rem; }
h2 { font-size: 1.35rem; margin: 2rem 0 0.6rem; border-bottom: 2px solid var(--line); padding-bottom: 0.25rem; }
h3 { font-size: 1.1rem; margin: 1.5rem 0 0.4rem; }
.layout { display: flex; min-height: 100vh; max-width: 1220px; margin: 0 auto; }
nav.sidebar { flex: 0 0 250px; padding: 1.6rem 1.2rem; border-right: 1px solid var(--line);
  background: var(--card); }
nav.sidebar .site-title { font-size: 1.05rem; font-weight: 700; color: var(--ink);
  display: block; margin-bottom: 1rem; }
nav.sidebar h2.sec { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--muted); font-weight: normal; margin: 1.2rem 0 0.4rem;
  border-bottom: 1px dotted var(--line); padding-bottom: 2px; }
nav.sidebar ul { list-style: none; margin: 0; padding: 0; }
nav.sidebar li { margin: 0.15rem 0; }
nav.sidebar a { display: block; font-size: 0.87rem; color: #3d4b44; font-family: Georgia, serif; }
nav.sidebar a:hover { color: var(--accent); }
nav.sidebar a.current { background: var(--accent-soft); color: var(--ink); font-weight: 700;
  border-radius: 4px; padding-left: 6px; }
main { flex: 1; padding: 2rem 2.4rem 3rem; max-width: 63rem; }
.pagefooter { margin-top: 3rem; padding-top: 0.8rem; border-top: 1px solid var(--line);
  font-size: 0.85rem; color: var(--muted); }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.92rem; }
th, td { text-align: left; vertical-align: top; padding: 0.5rem 0.7rem; border: 1px solid var(--line); }
th { background: var(--accent-soft); font-size: 0.85rem; }
tr:nth-child(even) td { background: #fbfaf6; }
code { background: var(--code-bg); border-radius: 3px; padding: 0.1em 0.35em;
  font-size: 0.88em; font-family: Consolas, Menlo, monospace; }
pre { overflow-x: auto; background: var(--code-bg); padding: 0.9rem; border-radius: 6px; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid var(--accent-soft); margin-left: 0; padding: 0.1rem 1rem; color: #42403c; }
hr { border: none; border-top: 1px solid var(--line); margin: 2rem 0; }
nav.pager { display: flex; justify-content: space-between; font-size: 0.88rem; margin-top: 2rem; }
nav.pager a { padding: 0.5rem 0.9rem; background: var(--accent-soft); border-radius: 5px;
  text-decoration: none; color: #29473c; }
nav.pager a:hover { background: #d6e6dd; }
@media (max-width: 880px) {
  .layout { flex-direction: column; }
  nav.sidebar { border-right: none; border-bottom: 1px solid var(--line); }
  main { padding: 1.4rem 1.2rem 2.4rem; }
  html { font-size: 16px; }
}
"""


if __name__ == "__main__":
    main()

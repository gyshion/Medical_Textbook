# Medical Textbooks

A static site for browsing medical textbook chapter PDFs, served via GitHub Pages.

**Live site:** https://gyshion.github.io/Medical_Textbook/

Currently hosts *First Aid for the USMLE Step 1 (2025, 35th ed.)* as 78 section PDFs grouped
by subject. Clicking a section opens its PDF in a new browser tab.

## How it works

- `index.html` — self-contained two-pane reader: sidebar navigation + inline PDF viewer,
  with a full-text search box.
- `manifest.js` — auto-generated data (`window.MANIFEST`) describing each textbook, its
  subjects, and section PDFs. Loaded by `index.html`.
- `generate_manifest.py` — scans the PDF folders and writes `manifest.js`.
- `search-docs.js` — auto-generated per-page text (`window.SEARCH_DOCS`) for search.
- `build_search_index.py` — extracts per-page PDF text and writes `search-docs.js`.
- `minisearch.min.js` — vendored client-side search library (loaded lazily on first search).
- PDFs live under `First Aid/PDFs/`, named `Subject-Section.pdf`.

## Search

Typing in the search box runs full-text search over the PDF content (client-side, no server).
Results show *subject · section · page* with a snippet; clicking jumps the viewer to that page.
The search index (`search-docs.js`) and library load lazily on first use, so the reader's
initial load stays light.

Regenerate the search index whenever the PDFs change (added textbook, or after
`strip_annotations.py`):

    python build_search_index.py

## To add a textbook

See **[ADDING_TEXTBOOKS.md](ADDING_TEXTBOOKS.md)** for the full step-by-step guide. In short:

1. Drop the textbook's PDFs in a new folder (e.g. `Pathoma/PDFs`), named `Subject-Section.pdf`.
2. Add an entry to the `TEXTBOOKS` list at the top of `generate_manifest.py`
   (`id`, `title`, `edition`, `icon`, `pdf_dir`).
3. Run `python generate_manifest.py` to regenerate `manifest.js`.
4. Commit and push — GitHub Pages redeploys automatically.

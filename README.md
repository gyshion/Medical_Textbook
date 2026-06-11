# Medical Textbooks

A static site for browsing medical textbook chapter PDFs, served via GitHub Pages.

**Live site:** https://gyshion.github.io/Medical_Textbook/

Currently hosts *First Aid for the USMLE Step 1 (2025, 35th ed.)* as 78 section PDFs grouped
by subject. Clicking a section opens its PDF in a new browser tab.

## How it works

- `index.html` — self-contained landing page (no build step, no external dependencies).
- `manifest.js` — auto-generated data (`window.MANIFEST`) describing each textbook, its
  subjects, and section PDFs. Loaded by `index.html`.
- `generate_manifest.py` — scans the PDF folders and writes `manifest.js`.
- PDFs live under `First Aid/PDFs/`, named `Subject-Section.pdf`.

## To add a textbook

1. Drop the textbook's PDFs in a new folder (e.g. `Pathoma/PDFs`), named `Subject-Section.pdf`.
2. Add an entry to the `TEXTBOOKS` list at the top of `generate_manifest.py`
   (`id`, `title`, `edition`, `icon`, `pdf_dir`).
3. Run `python generate_manifest.py` to regenerate `manifest.js`.
4. Commit and push — GitHub Pages redeploys automatically.

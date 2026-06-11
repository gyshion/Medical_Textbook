# Adding a Textbook & Redeploying

Step-by-step for adding a new textbook (or updating PDFs) and refreshing the live site at
**https://gyshion.github.io/Medical_Textbook/**.

Everything is static — there is no server. You regenerate two data files locally, then push;
GitHub Pages rebuilds automatically.

---

## 1. Add the PDF files

Create a folder for the textbook anywhere in the repo (a `PDFs` subfolder keeps it tidy) and
drop the PDFs in. Name each file `Subject-Section.pdf`:

```
Pathoma/PDFs/Cardiac-Pathology.pdf
Pathoma/PDFs/Cardiac-Physiology.pdf
Pathoma/PDFs/Renal-Pathology.pdf
```

**Naming rules** (parsed by `generate_manifest.py`):
- The filename is split on the **first hyphen** → left = **Subject**, right = **Section**.
  `Cardiac-Pathology.pdf` → subject *Cardiac*, section *Pathology*.
- Multi-word subjects are fine: `Hematology And Oncology-Anatomy.pdf`.
- A file with **no hyphen** goes into a catch-all **"Rapid Review"** chapter
  (e.g. `Classic Presentations.pdf`).
- Avoid renaming after the fact unless you also rerun the steps below — the filenames *are*
  the data.

## 2. Register the textbook

Edit the `TEXTBOOKS` list at the top of **`generate_manifest.py`** and add one entry:

```python
TEXTBOOKS = [
    {
        "id": "first-aid",
        "title": "First Aid for the USMLE Step 1",
        "edition": "2025 · 35th ed.",
        "icon": "\U0001F4D5",
        "pdf_dir": "First Aid/PDFs",
    },
    {                                   # <-- new textbook
        "id": "pathoma",
        "title": "Pathoma",
        "edition": "2023",
        "icon": "\U0001F4D8",           # any emoji; see note below
        "pdf_dir": "Pathoma/PDFs",      # path relative to repo root, forward slashes
    },
]
```

- `id` — short unique slug (lowercase, no spaces).
- `pdf_dir` — folder from step 1, **relative to the repo root**, using forward slashes.
- `icon` — an emoji. Use a `\U0001Fxxx` escape (e.g. 📕 `\U0001F4D5`, 📘 `\U0001F4D8`,
  📗 `\U0001F4D7`) or paste the emoji directly between quotes.

**Subject order (optional):** subjects render in the order defined by `SUBJECT_ORDER` in the
same file; any subject not listed there is appended alphabetically (with "Rapid Review" last).
Add your new subjects to `SUBJECT_ORDER` if you want a specific order.

## 3. (Optional) Strip highlights/underlines

If the new PDFs contain highlight/underline annotations you don't want published:

```powershell
# edit PDF_GLOB in strip_annotations.py if your folder isn't "First Aid/PDFs", then:
python strip_annotations.py
```

> Note: `strip_annotations.py` currently targets `First Aid/PDFs/*.pdf`. To clean a different
> folder, change the `PDF_GLOB` constant near the top, or run it once per folder.

## 4. Regenerate the data files

Run **both** scripts from the repo root. They re-scan every registered textbook:

```powershell
python generate_manifest.py      # rebuilds manifest.js  (sidebar navigation)
python build_search_index.py     # rebuilds search-docs.js (full-text search)
```

Expected output, e.g.:

```
First Aid for the USMLE Step 1: 17 subjects, 78 sections
Pathoma: 3 subjects, 12 sections
Wrote manifest.js
...
Wrote search-docs.js: 740 page docs, 1.60 MB
```

- `manifest.js` → drives the **sidebar** (textbook → subject → section).
- `search-docs.js` → the **full-text search** index (per-page text).

**Always run both whenever PDFs change** (added, removed, or after `strip_annotations.py`) —
otherwise the navigation or search will be out of sync with the files.

## 5. Commit and push

```powershell
git add -A
git commit -m "Add Pathoma textbook"
git push
```

GitHub Pages redeploys automatically on push (no manual step). `__pycache__/`, `*.pyc`, and
`*.tmp` are already git-ignored.

## 6. Verify the live site

The Pages build takes ~1 minute. Check status and the result:

```powershell
gh api repos/gyshion/Medical_Textbook/pages/builds/latest --jq .status   # -> "built"
```

Then open https://gyshion.github.io/Medical_Textbook/ and confirm:
- the new textbook card appears in the sidebar and expands to its subjects/sections,
- clicking a section opens its PDF in the right pane,
- searching a term unique to the new book returns a result that deep-links to the right page.

---

## File reference

| File | Purpose | Edit by hand? |
|------|---------|---------------|
| `index.html` | The whole UI (reader + search) | Yes, for UI changes |
| `generate_manifest.py` | Scans PDFs → `manifest.js`; holds the `TEXTBOOKS` registry | Yes, to add textbooks |
| `build_search_index.py` | Extracts per-page text → `search-docs.js` | Rarely |
| `strip_annotations.py` | Removes highlight/underline annotations | Edit `PDF_GLOB` per folder |
| `manifest.js` | Generated navigation data | No — regenerated |
| `search-docs.js` | Generated search index | No — regenerated |
| `minisearch.min.js` | Vendored search library | No |
| `<Textbook>/PDFs/*.pdf` | The source PDFs | — |

## Quick checklist

1. Drop PDFs in `NewBook/PDFs/`, named `Subject-Section.pdf`.
2. Add a `TEXTBOOKS` entry in `generate_manifest.py`.
3. (Optional) `python strip_annotations.py`.
4. `python generate_manifest.py` **and** `python build_search_index.py`.
5. `git add -A && git commit -m "..." && git push`.
6. Wait ~1 min, verify at the live URL.

## Requirements

```powershell
pip install pymupdf      # used by build_search_index.py and strip_annotations.py
```

`generate_manifest.py` needs only the Python standard library. No Node.js is required —
`minisearch.min.js` is already vendored in the repo.

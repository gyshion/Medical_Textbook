"""Remove Highlight and Underline annotations from the textbook PDFs.

Rewrites each affected PDF in place (with garbage collection so the file does
not bloat). Other annotation types, if any, are left untouched.
"""

import glob
import os

import fitz  # PyMuPDF

REMOVE = {"Highlight", "Underline"}
PDF_GLOB = "First Aid/PDFs/*.pdf"

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    total_removed = 0
    files_changed = 0

    for path in sorted(glob.glob(os.path.join(ROOT, PDF_GLOB))):
        doc = fitz.open(path)
        removed = 0
        for page in doc:
            # Collect first; deleting while iterating annots() is unsafe.
            to_delete = [a for a in (page.annots() or []) if a.type[1] in REMOVE]
            for a in to_delete:
                page.delete_annot(a)
                removed += 1

        if removed:
            tmp = path + ".tmp"
            doc.save(tmp, garbage=4, deflate=True)
            doc.close()
            os.replace(tmp, path)
            files_changed += 1
            total_removed += removed
            print(f"  {os.path.basename(path)}: removed {removed}")
        else:
            doc.close()

    print(f"Done: removed {total_removed} annotation(s) from {files_changed} file(s).")


if __name__ == "__main__":
    main()

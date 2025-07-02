#!/usr/bin/env python3
"""
keep_page.py
Behält nur eine gewünschte Seite aus PDF-Dateien.
Nutzung:
    python3 keep_page.py 9 <PDF oder Ordner> ...
"""
import sys, os, re
from PyPDF2 import PdfReader, PdfWriter

def keep_page(pdf_path: str, page_no: int) -> None:
    idx = page_no - 1                        # nullbasiert
    reader = PdfReader(pdf_path)
    if idx >= len(reader.pages):
        print(f"⚠️  {os.path.basename(pdf_path)} hat nur {len(reader.pages)} Seiten – übersprungen.")
        return
    writer = PdfWriter()
    writer.add_page(reader.pages[idx])

    out = re.sub(r"\.pdf$", f"_Seite{page_no}.pdf", pdf_path, flags=re.I)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"✅  {os.path.basename(pdf_path)} → {os.path.basename(out)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Aufruf: python3 keep_page.py <Seitenzahl> <PDF/Ordner> …")
        sys.exit(1)

    page_no = int(sys.argv[1])
    targets = sys.argv[2:]

    for t in targets:
        if os.path.isdir(t):
            for f in os.listdir(t):
                if f.lower().endswith(".pdf"):
                    keep_page(os.path.join(t, f), page_no)
        elif t.lower().endswith(".pdf"):
            keep_page(t, page_no)
        else:
            print(f"⚠️  {t} ist weder PDF noch Ordner – übersprungen.")

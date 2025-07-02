"""
rename_pdfs.py
Benennt alle PDFs in einem angegebenen Ordner anhand der ersten Betreffzeile
(oder ersten nicht-leeren Zeile) auf Seite 1 um.

Nutzung:
    python rename_pdfs.py /pfad/zum/ordner

Abhängigkeit:
    pip install PyPDF2
"""

import os
import re
import sys
from PyPDF2 import PdfReader


def extract_subject(pdf_path: str) -> str | None:
    """Liest Zeilen, überspringt Kopf-/Fußzeilen und liefert die 1. relevante Zeile."""
    try:
        reader = PdfReader(pdf_path)
        if not reader.pages:
            return None

        text = reader.pages[0].extract_text() or ""
        for line in text.splitlines():
            cleaned = line.strip()
            if not cleaned:
                continue

            # Kopfzeilen überspringen:
            #  1. alles mit Doppelpunkt (colon) => typischerweise 'Tel.:', 'Fax:', 'Sitz:' …
            #  2. alles, was eine E-Mail-Adresse enthält
            if ":" in cleaned or "@" in cleaned:
                continue

            # Passt – erste wirkliche Inhaltszeile
            return cleaned
    except Exception as exc:
        print(f"Fehler beim Lesen von {pdf_path}: {exc}")
        return None



def slugify(text: str) -> str:
    """Macht aus beliebigem Text einen dateisystemfreundlichen Dateinamen."""
    text = text.strip()
    replacements = {
        "ä": "ae", "ö": "oe", "ü": "ue",
        "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
        "ß": "ss",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r"[^A-Za-z0-9 _\\-]", "_", text)
    text = re.sub(r"\\s+", "_", text)
    return text[:100]  # Länge begrenzen


def main(directory: str) -> None:
    """Durchläuft alle PDFs in einem Ordner und benennt sie um."""
    for filename in os.listdir(directory):
        if not filename.lower().endswith(".pdf"):
            continue

        src_path = os.path.join(directory, filename)
        subject = extract_subject(src_path)
        if not subject:
            print(f"Kein Betreff in {filename} gefunden – wird übersprungen.")
            continue

        base_name = slugify(subject)
        new_name = f"{base_name}.pdf"
        counter = 1
        while os.path.exists(os.path.join(directory, new_name)):
            new_name = f"{base_name}_{counter}.pdf"
            counter += 1

        dst_path = os.path.join(directory, new_name)
        os.rename(src_path, dst_path)
        print(f"{filename}  →  {new_name}")


if __name__ == "__main__":
    dir_path = sys.argv[1] if len(sys.argv) > 1 else "."
    if not os.path.isdir(dir_path):
        print("Bitte einen gültigen Ordnerpfad angeben.")
        sys.exit(1)
    main(dir_path)

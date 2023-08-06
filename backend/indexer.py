from PyPDF2 import PdfReader
import csv

SOURCE_FILE = "The Mercedes-Benz A-Class Limousine.pdf"
OUTPUT_CSV = "Mercedes-Benz-A-Class-Limousine.csv"

reader = PdfReader(SOURCE_FILE)
n_pages = len(reader.pages)

header = False
for n in range(n_pages):
    page = reader.pages[n]
    text = page.extract_text()

    with open(SOURCE_FILE, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=["page", "content"])
        if not header:
            writer.writeheader()
            header = True

        writer.writerow({"page": n + 1, "content": text.lower()})
        f.close()

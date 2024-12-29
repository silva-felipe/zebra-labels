from pypdf import PdfWriter
from datetime import datetime

def merge_pdf(batch_files_pdf, now):
    merger = PdfWriter()
    for file_path in batch_files_pdf:
        merger.append(file_path)
    merger.write(f"zebras_pdf/{now}_zebra_labels.pdf")
    merger.close()

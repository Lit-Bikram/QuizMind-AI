import os
from app.services.ingestion.pdf_loader import extract_text_from_pdf


def parse_uploaded_file(file_path: str) -> dict:
    """
    Parse uploaded file based on extension.
    Currently supports only PDF.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError(f"Unsupported file type: {ext}")
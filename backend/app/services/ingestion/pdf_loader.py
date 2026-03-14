import fitz  # PyMuPDF # type: ignore


def extract_text_from_pdf(file_path: str) -> dict:
    """
    Extract text from a PDF file using PyMuPDF.

    Returns:
        {
            "text": full_text,
            "num_pages": int
        }
    """
    doc = fitz.open(file_path)

    extracted_text = []
    num_pages = len(doc)

    for page in doc:
        extracted_text.append(page.get_text())

    doc.close()

    full_text = "\n".join(extracted_text).strip()

    return {
        "text": full_text,
        "num_pages": num_pages
    }
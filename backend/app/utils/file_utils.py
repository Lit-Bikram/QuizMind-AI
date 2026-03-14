import os
from uuid import uuid4
from fastapi import UploadFile # type: ignore

UPLOAD_DIR = "uploaded_docs"


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_unique_filename(original_filename: str) -> str:
    file_ext = os.path.splitext(original_filename)[1]
    unique_name = f"{uuid4().hex}{file_ext}"
    return unique_name


def save_uploaded_file(file: UploadFile) -> str:
    ensure_upload_dir()
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path
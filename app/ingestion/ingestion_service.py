import fitz
import re
from fastapi import UploadFile
from langchain_text_splitters import CharacterTextSplitter
from vector_database import vector_db_service
from typing import List

splitter = CharacterTextSplitter()

def process_files(files: List[UploadFile]):
    for file in files:
        text: str = extract_text(file)
        chunks: list[str] = splitter.split_text(text)
        vector_db_service.upload_text_chunks(chunks, file)


def extract_text(file: UploadFile) -> str:
    content: bytes = file.file.read()

    if file.filename.endswith(".pdf"):
        return extract_from_pdf(content)
    return ""

def extract_from_pdf(file_content: bytes) -> str:
    document = fitz.open(stream=file_content, filetype="pdf").pages(start=1)
    pages_text = []

    for page in document:
        text: str = re.sub(" +", " ", page.get_text().replace("\n", " "))
        pages_text.append(text)
    return "\n\n".join(pages_text)
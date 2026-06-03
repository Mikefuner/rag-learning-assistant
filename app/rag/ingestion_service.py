from io import BytesIO
import fitz, re
from fastapi import UploadFile
from docx import Document as Docs
from video_converter import video_converter_service
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from . import vector_db_service
from typing import List

char_splitter = CharacterTextSplitter()
recs_splitter = RecursiveCharacterTextSplitter()

def process_files(files: List[UploadFile]):
    for file in files:
        chunks: list[str] = get_chunks(file)
        print(chunks)
        # vector_db_service.upload_text_chunks(chunks)


def get_chunks(file: UploadFile) -> list[str]:
    content: bytes = file.file.read()

    if file.filename.endswith(".pdf"): return split_pdf_text(content)
    elif file.filename.endswith(".docx"): return split_docx_document(content)
    elif file.filename.endswith(".mp4"): return split_video_text(file)
    return []

def split_pdf_text(file_content: bytes) -> list[str]:
    document = fitz.open(stream=file_content, filetype="pdf").pages(start=1)
    pages_text = [re.sub(" +", " ", page.get_text().replace("\n", " ")) for page in document]
    return pages_text

def split_docx_document(file_content: bytes) -> list[str]:
    document = Docs(BytesIO(file_content))
    text = "\n\n".join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())
    if not text: return []
    return [doc.page_content for doc in char_splitter.split_documents([Document(page_content=text)])]

def split_video_text(file: UploadFile) -> list[str]:
    video_text: str = video_converter_service.from_video_to_text(file)
    return recs_splitter.split_text(video_text)
import fitz
from fastapi import UploadFile
from docx import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from io import BytesIO
from dotenv import load_dotenv
from typing import List

load_dotenv()

splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10, separator=" ")
embedding_function = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
vector_database = Chroma(collection_name="study_material", embedding_function=embedding_function)

def process_files(files: List[UploadFile]):
    for file in files:
        text: str = extract_text(file)
        chunks: list[str] = splitter.split_text(text)
        vector_database.add_texts(texts=chunks, metadatas=[{"source": file.filename, "chunk": i} for i in range(len(chunks))])


def extract_text(file: UploadFile) -> str:
    content: bytes = file.file.read()

    if file.filename.endswith(".pdf"):
        return extract_from_pdf(content)
    elif file.filename.endswith(".docx"):
        return extract_from_docx(content)
    return ""

def extract_from_pdf(file_content: bytes) -> str:
    doc = fitz.open(stream=file_content, filetype="pdf")
    file_text: str = " ".join([page.get_text() for page in doc])
    return file_text.replace("\n", " ")

def extract_from_docx(file_content:bytes) -> str:
    doc = Document(BytesIO(file_content))
    file_text: str = " ".join([page.text for page in doc.paragraphs])
    return file_text.replace("\n", " ")
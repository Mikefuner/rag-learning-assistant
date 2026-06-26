import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
db_path = PROJECT_ROOT / "db" / "db_path"
embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
vector_database = Chroma(collection_name="study_material", embedding_function=embedding_function, persist_directory=str(db_path))

def upload_text_chunks(chunks: list[str], file: UploadFile):
    vector_database.add_texts(texts=chunks, metadatas=[{"source": file.filename, "chunk": i}
        for i in range(len(chunks))
    ])

def upload_document_chunks(chunks: list[Document], file: UploadFile):
    vector_database.add_documents(chunks, metadatas=[{"source": file.filename, "chunk": i}
        for i in range(len(chunks))
    ])

def retrieve_chunks(query: str) -> list[str]:
    docs: list[Document] = vector_database.similarity_search(query, k=10)
    return [doc.page_content for doc in docs]

def delete_database():
    os.remove(db_path)
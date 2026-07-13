import os, shutil
from dotenv import load_dotenv
from pathlib import Path
from fastapi import UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
db_path = PROJECT_ROOT / "db" / "chroma_db"
embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")

class VectorDatabase:

    def __init__(self):
        self.vector_database = Chroma(
            collection_name="study_material",
            embedding_function=embedding_function,
            persist_directory=str(db_path)
        )

    def upload_text_chunks(self, chunks: list[str], file: UploadFile):
        self.vector_database.add_texts(texts=chunks, metadatas=[{"source": file.filename, "chunk": i}
            for i in range(len(chunks))
        ])

    def upload_document_chunks(self, chunks: list[Document], file: UploadFile):
        self.vector_database.add_documents(chunks, metadatas=[{"source": file.filename, "chunk": i}
            for i in range(len(chunks))
        ])

    def retrieve_chunks(self, query: str) -> list[str]:
        docs: list[Document] = self.vector_database.similarity_search(query, k=10)
        return [doc.page_content for doc in docs]

    def reset_database(self):
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        self.vector_database = Chroma(
            collection_name="study_material",
            embedding_function=embedding_function,
            persist_directory=str(db_path)
        )
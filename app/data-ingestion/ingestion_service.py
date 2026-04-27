from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from typing import List

class IngestionService:

    def __init__(self):
        load_dotenv()

    def prepare_files(self, files: List[UploadFile]):
        
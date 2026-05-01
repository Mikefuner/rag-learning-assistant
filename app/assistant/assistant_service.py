from typing import List
from ingestion.ingestion_service import process_files
from retrieval_generation.retrieval_generation_service import retrieve_user_query
from fastapi import UploadFile

class AssistantService:

    def upload_files(self, files: List[UploadFile]):
        process_files(files)

    def user_query(self, query: str):
        retrieve_user_query(query)
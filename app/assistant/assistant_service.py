from typing import List
from ingestion import ingestion_service
from retrieval_generation import retrieval_generation_service
from fastapi import UploadFile

class AssistantService:

    def upload_files(self, files: List[UploadFile]):
        ingestion_service.process_files(files)

    def delete_collection(self, collection_name: str):
        ingestion_service.delete_collection(collection_name)

    def user_query(self, query: str):
        return retrieval_generation_service.generate_response(query)
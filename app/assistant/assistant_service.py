from typing import List
from rag import ingestion_service, generation_service
from fastapi import UploadFile

class AssistantService:

    def upload_files(self, files: List[UploadFile]):
        ingestion_service.process_files(files)

    def delete_collection(self, collection_name: str):
        return None

    def user_query(self, query: str):
        return generation_service.generate_response(query)
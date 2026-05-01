from typing import List
from data_ingestion.ingestion_service import process_files
from fastapi import UploadFile

class AssistantService:

    def upload_files(self, files: List[UploadFile]):
        process_files(files)

    def ask_question(self, file: UploadFile):
        return None
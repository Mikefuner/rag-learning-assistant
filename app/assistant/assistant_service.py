from typing import List
from fastapi import UploadFile

class AssistantService:

    def upload_files(self, files: List[UploadFile]):
        return None

    def ask_question(self, file: UploadFile):
        return None
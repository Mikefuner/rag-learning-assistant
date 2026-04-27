from fastapi import APIRouter, UploadFile
from assistant.assistant_service import AssistantService
from typing import List
router = APIRouter()
service = AssistantService()

@router.post("/upload_file")
async def upload_file(file: UploadFile):
    return service.upload_file(file)

@router.post("/upload_files")
async def upload_files(files: List[UploadFile]):
    for file in files:
        service.upload_file(file)
    return None

@router.post("/ask_question")
async def ask_question(prompt: str):
    return service.ask_question(prompt)
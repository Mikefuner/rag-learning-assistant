from fastapi import APIRouter, UploadFile
from assistant.assistant_service import AssistantService
from typing import List
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
router = APIRouter()
service = AssistantService()

@router.post("/upload_files")
async def upload_files(files: List[UploadFile]):
    service.upload_files(files)

@router.post("/user_query")
async def user_query(request: QueryRequest):
    return service.user_query(request.query)
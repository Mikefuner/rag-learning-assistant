from fastapi import APIRouter, UploadFile
from assistant import assistant_service
from typing import List
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
router = APIRouter()

@router.post("/upload_files")
async def upload_files(files: List[UploadFile]):
    assistant_service.upload_files(files)

@router.post("/query_request")
async def query_request(request: QueryRequest):
    return QueryResponse(response=assistant_service.query_request(request.query))

@router.post("/audio_request")
async def audio_request(audio_file: UploadFile):
    return QueryResponse(response=assistant_service.audio_request(audio_file))

@router.delete("/delete_all")
async def delete_all_info():
    assistant_service.delete_all_info()
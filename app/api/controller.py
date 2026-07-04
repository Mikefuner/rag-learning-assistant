from fastapi import APIRouter, UploadFile, Depends
from assistant import assistant_service
from security.auth import verify_access
from typing import List
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
router = APIRouter()

@router.post("/upload_files", dependencies=[Depends(verify_access)])
async def upload_files(files: List[UploadFile]):
    assistant_service.upload_files(files)

@router.post("/query_request", dependencies=[Depends(verify_access)])
async def query_request(request: QueryRequest):
    return QueryResponse(response=assistant_service.query_request(request.query))

@router.post("/audio_request", dependencies=[Depends(verify_access)])
async def audio_request(audio_file: UploadFile):
    return QueryResponse(response=assistant_service.audio_request(audio_file))

@router.delete("/delete_all", dependencies=[Depends(verify_access)])
async def delete_all_info():
    assistant_service.delete_all_info()
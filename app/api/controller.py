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

@router.post("/user_query")
async def user_query(request: QueryRequest):
    return QueryResponse(response=assistant_service.user_query(request.query))

@router.delete("delete_collection/{collection_name}")
async def delete_collection(collection_name: str):
    assistant_service.delete_collection(collection_name)
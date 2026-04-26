from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile):
    return None

@router.post("/send_prompt")
async def send_prompt(prompt: str):
    return None
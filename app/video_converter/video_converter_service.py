import shutil
from pathlib import Path
import time
from fastapi import UploadFile
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = PROJECT_ROOT / "files" / "video"
FILE_NAME = "video.mp4"
WHISPER_MODEL = "whisper-1"

def from_video_to_text(file: UploadFile) -> str:
    save_video_as_mp4(file)
    time.sleep(2)
    text: str = transcribe_mp4_to_text()
    delete_mp4_video()
    return text

def save_video_as_mp4(file: UploadFile):
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    file_path = VIDEO_DIR / FILE_NAME
    file.file.seek(0)

    with file_path.open("wb") as output_file:
        shutil.copyfileobj(file.file, output_file)


def transcribe_mp4_to_text() -> str:
    file_path = VIDEO_DIR / FILE_NAME
    if not file_path.is_absolute():
        file_path = file_path if file_path.parts[:2] == ("files", "video") else VIDEO_DIR / file_path
        file_path = PROJECT_ROOT / file_path if file_path.parts[:2] == ("files", "video") else file_path

    if file_path.suffix.lower() != ".mp4":
        raise ValueError("The video file must be an .mp4 file.")
    if not file_path.exists():
        raise FileNotFoundError(f"Video file not found: {file_path}")

    client = OpenAI()
    with file_path.open("rb") as video:
        return client.audio.transcriptions.create(model=WHISPER_MODEL, file=video, response_format="text")


def delete_mp4_video() -> bool:
    file_path = VIDEO_DIR / FILE_NAME
    if not file_path.exists(): return False
    file_path.unlink()
    return True

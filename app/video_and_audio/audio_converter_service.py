import shutil
from pathlib import Path
import time
from fastapi import UploadFile
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = PROJECT_ROOT / "files" / "audio"
FILE_NAME = "audio.mp4"
WHISPER_MODEL = "whisper-1"

def from_audio_to_text(file: UploadFile) -> str:
    save_audio_as_mp3(file)
    time.sleep(2)
    text: str = transcribe_mp3_to_text()
    delete_mp3_audio()
    return text

def save_audio_as_mp3(file: UploadFile):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    file_path = AUDIO_DIR / FILE_NAME
    file.file.seek(0)

    with file_path.open("wb") as output_file:
        shutil.copyfileobj(file.file, output_file)


def transcribe_mp3_to_text() -> str:
    file_path = AUDIO_DIR / FILE_NAME
    if not file_path.is_absolute():
        file_path = file_path if file_path.parts[:2] == ("files", "audio") else AUDIO_DIR / file_path
        file_path = PROJECT_ROOT / file_path if file_path.parts[:2] == ("files", "audio") else file_path

    if file_path.suffix.lower() != ".mp4":
        raise ValueError("The audio file must be an .mp3 file.")
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    client = OpenAI()
    with file_path.open("rb") as audio:
        return client.audio.transcriptions.create(model=WHISPER_MODEL, file=audio, response_format="text")


def delete_mp3_audio() -> bool:
    file_path = AUDIO_DIR / FILE_NAME
    if not file_path.exists(): return False
    file_path.unlink()
    return True
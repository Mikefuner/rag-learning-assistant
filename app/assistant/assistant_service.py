from typing import List
from rag import ingestion_service, generation_service
from chat_memory import chat_memory_service
from video_and_audio import audio_converter_service
from fastapi import UploadFile

def upload_files(files: List[UploadFile]):
    ingestion_service.process_files(files)

def query_request(query: str):
    chat_messages = chat_memory_service.get_messages()
    chat_memory_service.add_message("user", query)
    response = generation_service.generate_response(query, chat_messages)
    chat_memory_service.add_message("assistant", response)
    return response

def audio_request(audio_file: UploadFile):
    text_query: str = audio_converter_service.from_audio_to_text(audio_file)
    return query_request(text_query)
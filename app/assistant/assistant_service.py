from typing import List
from rag import ingestion_service, generation_service
from chat_memory import chat_memory_service
from fastapi import UploadFile

def upload_files(self, files: List[UploadFile]):
    ingestion_service.process_files(files)

def delete_collection(self, collection_name: str):
    return None

def user_query(self, query: str):
    chat_memory_service.add_message("user", query)
    chat_messages = chat_memory_service.get_messages()
    response = generation_service.generate_response(query, chat_messages)
    chat_memory_service.add_message("assistant", response)
    return response
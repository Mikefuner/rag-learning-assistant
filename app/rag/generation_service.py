from typing import Any

from langchain_core.messages import AIMessage
from . import vector_db_service
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o")

def generate_response(basic_query: str, chat_history: list[dict[str, str]]) -> str | list[str | Any]:
    conversation: str = get_conversation(chat_history)
    contextualized_query: str = contextualize_query(basic_query, conversation)
    context: list[str] = vector_db_service.retrieve_text_chunks(contextualized_query)

    prompt: str = f'''
        Context : {"\n".join(context)}
        
        Chat history : {conversation}
        
        Question : {basic_query}
        
        The response should be in the same language of the question.
    '''
    response: AIMessage = model.invoke(prompt)
    return response.content


def contextualize_query(basic_query: str, conversation: str) -> str:
    prompt: str = f'''
        Given a chat history and the latest user question 
        which might reference context in the chat history,
        formulate a standalone question which can be understood
        without the chat history. Do NOT answer the question,
        just reformulate it, in the same language of the question.
        
        Chat history : {conversation}
        
        Question : {basic_query}
    '''
    response: AIMessage = model.invoke(prompt)
    return response.content


def get_conversation(chat_history: list[dict[str, str]]) -> str:
    paragraphs: list[str] = []

    for dialog in chat_history:
        paragraphs.append(
            f"{dialog.get('role')}: {dialog.get('content')}"
        )

    return "\n".join(paragraphs)

from langchain_core.messages import AIMessage
from vector_database import vector_db_service
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o")

def generate_response(query: str):
    context: list[str] = vector_db_service.retrieve_text_chunks(query)
    prompt: str = f'''
        Context : {"\n".join(context)}
        
        Question : {query}
        
        The response should be in the same language of the question.
    '''
    response: AIMessage = model.invoke(prompt)
    return response.content
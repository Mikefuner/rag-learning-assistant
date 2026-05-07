from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
db_path = "/home/mikeonuf/PycharmProjects/rag-learning-assistant/db/chroma_db"

embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
vector_database = Chroma(collection_name="study_material", embedding_function=embedding_function, persist_directory=db_path)
model = ChatOpenAI(model="gpt-4o")

def generate_response(query: str):
    context: str = retrieve_user_query(query)
    prompt: str = f'''
        Context : {context}
        
        Question : {query}
        
        The response should be in the same language of the question.
    '''
    response: AIMessage = model.invoke(prompt)
    return response.content

def retrieve_user_query(query: str):
    documents: list[Document] = vector_database.similarity_search(query, k=10)
    context: str = '\n'.join([doc.page_content for doc in documents])
    return context
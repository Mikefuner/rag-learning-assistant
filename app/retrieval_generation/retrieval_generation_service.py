from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from ingestion.ingestion_service import get_vector_database
from dotenv import load_dotenv

load_dotenv()

vector_database = get_vector_database()
#model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_response(query: str):
    return None

def retrieve_user_query(query: str):
    results = vector_database.similarity_search(query, k=3)
    print(results)
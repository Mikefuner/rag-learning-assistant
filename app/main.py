import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from api.controller import router

load_dotenv()

server_host = os.getenv("SERVER_HOST")
server_port = int(os.getenv("EXPOSE_PORT"))
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=server_host, port=server_port)
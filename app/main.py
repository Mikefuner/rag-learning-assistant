import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from api.controller import router

load_dotenv()
expose_port = int(os.getenv("EXPOSE_PORT", "8000"))
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=expose_port)
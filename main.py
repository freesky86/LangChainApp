import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.endpoint.chat import router as chat_router


load_dotenv()
tags_metadata = [
    {
        "name": "chat",
        "description": "Endpoints related to chat interactions.",
    },
]

app = FastAPI(
    title="Chat API",
    description="API for handling chat interactions using GPT.",
    version="1.0.0", 
    openapi_tags=tags_metadata
)


app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
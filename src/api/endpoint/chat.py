from fastapi import APIRouter

from src.services.gpt_service import GPTService
from src.schemas.chat_request import ChatRequest
from src.schemas.chat_response import ChatResponse


router = APIRouter(tags=["chat"])
gpt_service = GPTService()


@router.post("/chat")
async def ask_question(chat_request: ChatRequest):
    message = chat_request.content
    response = gpt_service.ask(message)

    return ChatResponse(question=message, answer=response)
from fastapi import APIRouter

from src.services.gpt_service import GPTService
from src.schemas.chat_request import ChatRequest
from src.schemas.chat_response import ChatResponse
from src.agent.calculate_agent import CalculateAgent


router = APIRouter(tags=["chat"])
gpt_service = GPTService()
calculate_agent = CalculateAgent()


@router.post("/chat")
async def ask_question(chat_request: ChatRequest):
    message = chat_request.content
    response = gpt_service.ask(message)

    return ChatResponse(question=message, answer=response)


@router.post("/agent")
async def ask_agent(chat_request: ChatRequest):
    message = chat_request.content
    response = calculate_agent.ask_agent(message)

    return ChatResponse(question=message, answer=response)
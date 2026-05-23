from fastapi import FastAPI, APIRouter

from src.services.gpt_service import GPTService


router = APIRouter(tags=["chat"])
gpt_service = GPTService()

@router.post("/chat")
async def send_message(message: str):
    response = gpt_service.ask(message)
    return {"status": "Message sent", "message": message, "response": response}
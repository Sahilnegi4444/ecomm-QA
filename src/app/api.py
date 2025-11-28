from fastapi import APIRouter
from pydantic import BaseModel
from src.rag_pipeline.chatbot import Chatbot

# initialize chatbot here once → reuse memory across requests
chatbot = Chatbot(collection="product_collection")

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response, _ = chatbot.chat(request.query)
    return ChatResponse(response=response)

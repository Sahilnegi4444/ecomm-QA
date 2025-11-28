from fastapi import FastAPI
from src.app.api import router

app = FastAPI(
    title="Customer QA Chatbot API",
    description="Chatbot using Llama model + RAG",
    version="1.0.0"
)

# include our chat routes
app.include_router(router)
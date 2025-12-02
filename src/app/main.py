from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager  
from src.rag_pipeline.chatbot import Chatbot
from src.db.vector_db import VectorDB
from src.logger import logging

# Global collection and chatbot session storage
collection = None
chatbot_sessions = {}  # {session_id: Chatbot instance}


# Request/Response Models
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"
    k: int = 5


class ChatResponse(BaseModel):
    response: str
    products: list = []


# Initialize ChromaDB on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global collection
    
    # 🗄️ Load ChromaDB vector collection at startup
    print("🚀 Starting API — loading ChromaDB...")
    logging.info("Starting API — loading ChromaDB...")
    try:
        db_manager = VectorDB(persist_directory="./chroma_db")
        # try to get existing collection, may raise if not present
        try:
            collection = db_manager.client.get_collection("products")
        except Exception:
            # collection not found — leave as None and continue
            collection = None
            print("! Collection not found — continuing without collection")
            logging.info("! Collection not found")
        else:
            print("✓ Collection loaded")
            logging.info("✓ Collection loaded successfully")
    except Exception as e:
        # If DB init fails, log and continue so health endpoints still work
        collection = None
        print(f"! Failed to initialize VectorDB at startup: {e}")
        logging.info(f"! Failed to initialize VectorDB at startup: {e}")

    yield  # <-- App running here

    # 🔻 Optional shutdown cleanup here
    print("🛑 Shutting down API...")
    logging.info("Shut down API...")
    
# Create FastAPI app
app = FastAPI(
    title="Customer QA Chatbot API",
    description="Chatbot using Llama model + RAG",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with session-based chatbot instances"""
    global collection
    
    # Get or create a chatbot for this session
    if request.session_id not in chatbot_sessions:
        chatbot_sessions[request.session_id] = Chatbot(collection=collection)
    
    chatbot = chatbot_sessions[request.session_id]
    
    # Generate response using RAG pipeline
    response_text, results = chatbot.chat(request.query, k=request.k)
    
    # Return structured response
    return ChatResponse(
        response=response_text,
        products=chatbot.last_products
    )
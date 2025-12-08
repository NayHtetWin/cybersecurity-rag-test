import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.generation import get_rag_chain  # RAG logic
import logging
import time 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("rag_api")

# Initialize FastAPI App
app = FastAPI(
    title="Cybersecurity RAG API",
    description="A RAG system answering questions based on OWASP, Thailand Web Security Standard, and MITRE ATT&CK.",
    version="1.0"
)

# Define Request Model
class QueryRequest(BaseModel):
    query: str

# Define Response Model
class QueryResponse(BaseModel):
    answer: str

# Check if the vector database exists
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
if not os.path.exists(DB_PATH):
    raise RuntimeError(
        "❌ Vector database not found. Run 'python src/ingestion.py' first."
    )

# Load the Chain at Startup (Efficiency)
# Load it once to prevent re-initialize the DB on every request.
rag_chain = get_rag_chain()

@app.middleware("http")
async def log_latency(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} completed in {latency:.3f}s")
    return response

async def stream_rag(query):
    async for chunk in rag_chain.astream(query):
        yield chunk

@app.get("/")
def health_check():
    return {"status": "active", "message": "Cybersecurity RAG API is running"}

@app.post("/query", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Endpoint to ask a question to the RAG system.
    """
    try:
        print(f"📩 Received query: {request.query}")
        
        # Invoke the RAG chain
        response_text = rag_chain.invoke(request.query)

        return QueryResponse(answer=response_text)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))

# Streaming endpoint
@app.post("/query/stream")
async def ask_question_stream(request: QueryRequest):
    """
    Endpoint to ask a question with streaming response.
    """
    try:
        print(f"📩 Received streaming query: {request.query}")
        return StreamingResponse(
            stream_rag(request.query), 
            media_type="text/plain"
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")  
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
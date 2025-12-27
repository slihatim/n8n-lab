import chromadb
from chromadb.config import Settings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime

# Initialize FastAPI
app = FastAPI()

# Initialize ChromaDB (Persistent)
# This creates a folder "chroma_data" in your project directory
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="customer_memory")

# Data Models
class MemoryEntry(BaseModel):
    user_id: str
    conversation_summary: str

class QueryRequest(BaseModel):
    user_id: str
    query_text: str

@app.post("/add_memory")
def add_memory(entry: MemoryEntry):
    try:
        collection.add(
            documents=[entry.conversation_summary],
            metadatas=[{"user_id": entry.user_id, "timestamp": str(datetime.now())}],
            ids=[str(uuid.uuid4())]
        )
        return {"status": "success", "message": "Memory stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_memory")
def query_memory(request: QueryRequest):
    try:
        results = collection.query(
            query_texts=[request.query_text],
            n_results=3,
            # Filter results to only this specific user
            where={"user_id": request.user_id}
        )
        # Flatten the list of documents
        documents = [doc for sublist in results['documents'] for doc in sublist]
        return {"relevant_context": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
# knowledge_base_service/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Set up ChromaDB in-memory
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=".chromadb"))
collection = client.get_or_create_collection("knowledge_base")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class IngestRequest(BaseModel):
    documents: List[str]

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/ingest")
def ingest_docs(req: IngestRequest):
    for i, doc in enumerate(req.documents):
        embedding = embedding_model.encode(doc).tolist()
        collection.add(documents=[doc], embeddings=[embedding], ids=[f"doc_{i}"])
    return {"status": "success", "ingested": len(req.documents)}

@app.post("/query")
def search_kb(req: QueryRequest):
    query_embedding = embedding_model.encode(req.query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=req.top_k)
    
    return {
        "query": req.query,
        "results": results["documents"][0] if results["documents"] else []
    }

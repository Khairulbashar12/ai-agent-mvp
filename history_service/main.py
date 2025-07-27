# history_service/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from pymongo import MongoClient
import os

app = FastAPI()

# Connect to MongoDB (update URI if needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["ai_agent"]
collection = db["chat_history"]

class Message(BaseModel):
    role: str  # 'user' or 'bot'
    content: str

class HistoryRequest(BaseModel):
    chat_id: str
    messages: List[Message]

@app.post("/history")
def save_history(req: HistoryRequest):
    # Upsert (insert or update) chat history
    collection.update_one(
        {"chat_id": req.chat_id},
        {"$push": {"messages": {"$each": [msg.dict() for msg in req.messages]}}},
        upsert=True
    )
    return {"status": "saved", "chat_id": req.chat_id}

@app.get("/history/{chat_id}")
def get_history(chat_id: str):
    result = collection.find_one({"chat_id": chat_id}, {"_id": 0})
    if result:
        return result
    return {"chat_id": chat_id, "messages": []}

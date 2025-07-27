# chat_service/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# URLs of other services
KB_URL = "http://localhost:8001/query"
SEARCH_URL = "http://localhost:8002/search"
HISTORY_URL = "http://localhost:8003/history"

# Request model
class ChatRequest(BaseModel):
    chat_id: str
    message: str

# Helper to get KB answer
async def get_kb_answer(query: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(KB_URL, json={"query": query})
        return res.json().get("results", [])

# Helper to get web search fallback
async def get_web_answer(query: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(SEARCH_URL, params={"query": query})
        results = res.json().get("results", [])
        return "\n".join([r["title"] + ": " + r["body"] for r in results])

# Helper to generate response with OpenAI
def get_openai_response(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or use gpt-4 if available
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# Helper to store chat history
async def save_history(chat_id: str, user_msg: str, bot_msg: str):
    async with httpx.AsyncClient() as client:
        await client.post(HISTORY_URL, json={
            "chat_id": chat_id,
            "messages": [
                {"role": "user", "content": user_msg},
                {"role": "bot", "content": bot_msg}
            ]
        })

@app.post("/chat")
async def chat(req: ChatRequest):
    user_msg = req.message

    # Try knowledge base
    kb_results = await get_kb_answer(user_msg)

    if kb_results:
        context = "\n".join(kb_results)
        prompt = f"Answer using this context:\n{context}\n\nQuestion: {user_msg}"
    else:
        # Fallback to web
        web_context = await get_web_answer(user_msg)
        prompt = f"Answer using web info:\n{web_context}\n\nQuestion: {user_msg}"

    # Call OpenAI
    bot_msg = get_openai_response(prompt)

    # Save to history
    await save_history(req.chat_id, user_msg, bot_msg)

    return {"chat_id": req.chat_id, "response": bot_msg}

@app.get("/chat/{chat_id}")
async def get_chat_history(chat_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{HISTORY_URL}/{chat_id}")
        return res.json()

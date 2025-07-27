# 🧠 AI Agent MVP (Microservices-Based)

A Minimal Viable Product (MVP) of an AI Assistant built using Python microservices with FastAPI. It answers user queries using a knowledge base or fallback web search and stores chat history.

---

## 📦 Microservices

| Service          | Port | Description                                 |
|------------------|------|---------------------------------------------|
| `chat_service`   | 8000 | Main orchestrator. Handles chat logic.      |
| `kb_service`     | 8001 | Vector DB for semantic search via ChromaDB. |
| `search_service` | 8002 | Web search using DuckDuckGo.                |
| `history_service`| 8003 | MongoDB-based chat history.                 |

---

## ⚙️ Tech Stack

- **FastAPI** for backend APIs  
- **MongoDB** for chat history  
- **ChromaDB + SentenceTransformers** for semantic search  
- **DuckDuckGo Search** for fallback queries  
- **OpenAI API** for generating responses

---

## 🧪 API Endpoints

### 🔹 Chat Service (Port 8000)
- `POST /chat`  
- `GET /chat/{chat_id}`

### 🔹 Knowledge Base Service (Port 8001)
- `POST /ingest`  
- `POST /query`

### 🔹 Search Service (Port 8002)
- `GET /search?query=...`

### 🔹 History Service (Port 8003)
- `POST /history`  
- `GET /history/{chat_id}`

---

## 🧠 Sample Ingestion Data

For `POST /ingest`:

```json
{
  "documents": [
    "FastAPI is a fast Python web framework.",
    "ChromaDB is used for vector similarity search.",
    "OpenAI GPT models generate human-like text."
  ]
}

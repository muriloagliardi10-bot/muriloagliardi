import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from google import genai
from google.genai import types

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()

# --- 1. PRIMEIRO DEFINA AS CLASSES (MODELOS) ---
class ChatRequest(BaseModel):
    user_message: str
    current_page: str
    current_product: Optional[Dict[str, Any]] = None
    cart_items: Optional[List[Dict[str, Any]]] = []
    catalog: List[Dict[str, Any]]

class AdminChatRequest(BaseModel):
    user_message: str
    dashboard_data: Dict[str, Any]


# --- 2. DEPOIS DEFINA TODAS AS ROTAS DO SUAS IAs ---
@app.post("/api/chat")
async def process_ai_chat(data: ChatRequest):
    # ... código da rota do cliente ...
    pass

@app.post("/api/admin/chat")
async def process_admin_ai_chat(data: AdminChatRequest):
    # ... código da rota do admin ...
    pass


# --- 3. POR ÚLTIMO (LÁ NO FINALZÃO DO ARQUIVO) O UVICORN ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

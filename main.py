import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from google import genai

app = FastAPI()

# 1. Configuração do CORS (libera o Firebase para se comunicar com o Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DADOS ---

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    imagem: Optional[str] = "https://via.placeholder.com/300"

class ChatRequest(BaseModel):
    message: str

# Banco de dados de produtos inicial (em memória)
banco_produtos: List[dict] = [
    {
        "id": 1,
        "nome": "Camiseta Caceres Oversized",
        "preco": 120.00,
        "imagem": "https://via.placeholder.com/300"
    },
    {
        "id": 2,
        "nome": "Moletom Caceres Raw",
        "preco": 249.90,
        "imagem": "https://via.placeholder.com/300"
    }
]

# --- ROTAS DO CATÁLOGO DE PRODUTOS ---

# Rota GET: Chamada pelo index.html para carregar os produtos na tela
@app.get("/api/produtos")
def listar_produtos():
    return banco_produtos

# Rota POST: Chamada pelo admin.html para adicionar novos produtos
@app.post("/api/produtos")
def criar_produto(produto: Produto):
    novo_id = len(banco_produtos) + 1
    novo_prod = produto.model_dump() if hasattr(produto, "model_dump") else produto.dict()
    novo_prod["id"] = novo_id
    banco_produtos.append(novo_prod)
    return {"message": "Produto adicionado com sucesso!", "produto": novo_prod}

# Rota DELETE: Chamada pelo admin.html para excluir um produto pelo ID
@app.delete("/api/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    global banco_produtos
    banco_produtos = [p for p in banco_produtos if p.get("id") != produto_id]
    return {"message": "Produto removido com sucesso!"}


# --- ROTA DO CHAT DA IA (RAW AI) ---

@app.post("/api/chat")
def chat_ai(req: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no servidor.")
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt_sistema = f"""
        Você é o assistente virtual oficial da marca de streetwear CACERES.
        Responda às dúvidas dos clientes de forma concisa, direta e mantendo a identidade minimalista/urban da marca.
        Produtos disponíveis no momento: {banco_produtos}
        Pergunta do cliente: {req.message}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_sistema
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

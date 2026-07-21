from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

# 1. Configuração do CORS (libera o Firebase para acessar o Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para os Produtos
class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    imagem: Optional[str] = "https://via.placeholder.com/300"

# Banco de dados temporário em memória (para testes)
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

# Rota GET: O index.html chama essa rota para desenhar os produtos na tela
@app.get("/api/produtos")
def listar_produtos():
    return banco_produtos

# Rota POST: O admin.html chama essa rota para cadastrar novos produtos
@app.post("/api/produtos")
def criar_produto(produto: Produto):
    novo_id = len(banco_produtos) + 1
    novo_prod = produto.dict()
    novo_prod["id"] = novo_id
    banco_produtos.append(novo_prod)
    return {"message": "Produto adicionado com sucesso!", "produto": novo_prod}

# Rota DELETE: O admin.html chama essa rota para apagar um produto
@app.delete("/api/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    global banco_produtos
    banco_produtos = [p for p in banco_produtos if p.get("id") != produto_id]
    return {"message": "Produto removido com sucesso!"}


# --- SUA ROTA DO CHAT (RAW AI) CONTINUA AQUI ---
# @app.post("/api/chat")
# ... mantenha seu código da IA/Gemini aqui ...

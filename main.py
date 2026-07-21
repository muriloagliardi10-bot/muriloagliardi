import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from google import genai

app = FastAPI()

# Configuração de CORS - Libera o acesso do Firebase ao Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de Dados
class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    imagem: Optional[str] = "https://via.placeholder.com/300"

class ChatRequest(BaseModel):
    message: str

# Banco de dados temporário em memória
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

@app.get("/api/produtos")
def listar_produtos():
    """Retorna todos os produtos cadastrados"""
    return banco_produtos

@app.post("/api/produtos")
def criar_produto(produto: Produto):
    """Cadastra um novo produto vindo do admin"""
    novo_id = len(banco_produtos) + 1
    novo_prod = produto.model_dump() if hasattr(produto, "model_dump") else produto.dict()
    novo_prod["id"] = novo_id
    banco_produtos.append(novo_prod)
    return {"message": "Produto adicionado com sucesso!", "produto": novo_prod}

@app.delete("/api/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    """Remove um produto pelo ID"""
    global banco_produtos
    banco_produtos = [p for p in banco_produtos if p.get("id") != produto_id]
    return {"message": "Produto removido com sucesso!"}

# --- ROTA DO CHAT DA IA (RAW AI) ---

@app.post("/api/chat")
def chat_ai(req: ChatRequest):
    """Recebe a mensagem do cliente e responde via Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não encontrada no ambiente.")
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt_sistema = f"""
        Você é o assistente virtual da marca de streetwear CACERES.
        Responda às dúvidas dos clientes de forma concisa, direta e mantendo a identidade urbana/minimalista da marca.
        Catálogo atual de produtos: {banco_produtos}
        Pergunta do cliente: {req.message}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_sistema
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from app.despesas.routes import router as despesas_router # Importando o router de despesas
from app.usuario.routes import router as usuario_router # Importando o router de usuários

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter variáveis de ambiente
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
RESET_PASSWORD_URL = os.getenv("RESET_PASSWORD_URL")

# Criando a aplicação FastAPI
app = FastAPI()

# Configuração de CORS
origins = [
    "http://localhost:5173",  # Porta do Vite
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem (para fins de desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas criadas no routes.py
app.include_router(despesas_router)

# Inclui as rotas de usuário
app.include_router(usuario_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Controle Financeiro!"}

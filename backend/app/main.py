from fastapi import FastAPI
from app.despesas.routes import router as despesas_router # Importando o router de despesas
from app.usuario.routes import router as usuario_router # Importando o router de usuarios

app = FastAPI()

# Inclui as rotas criadas no routes.py
app.include_router(despesas_router)

# Inclui as rotas de usuário
app.include_router(usuario_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Controle Financeiro!"}


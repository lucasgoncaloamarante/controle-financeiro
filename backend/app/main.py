from fastapi import FastAPI
from app.despesas.routers import router as despesas_router # Importando o router de despesas

app = FastAPI()

# Inclui as rotas criadas no routers.py
app.include_router(despesas_router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Controle Financeiro!"}


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from app import models
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) # Cria as tabelas se não existirem

router = APIRouter()

# Dependência para criar sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar uma nova despesa
@router.post ("/despesas", response_model=schemas.Despesa)
def criar_despesa(despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    return crud.create_despesa(db=db, descricao=despesa.descricao, valor=despesa.valor, data=despesa.data, categoria=despesa.categoria)

# Endpoint para atualizar uma despesa
@router.put("/despesas/{despesa_id}", response_model=schemas.Despesa)
def atualizar_despesa(despesa_id: int, despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    return crud.update_despesa(db=db, despesa_id=despesa_id, descricao=despesa.descricao, valor=despesa.valor, data=despesa.data, categoria=despesa.categoria)

# Endpoint para deletar uma despesa
@router.delete("/despesas/{despesa_id}", response_model=schemas.Despesa)
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    return crud.delete_despesa(db=db, despesa_id=despesa_id)

    # Retorna o modelo Pydantic com os dados da despesa deletada
    return schemas.Despesa(
        id=despesa_deletada.id,
        descricao=despesa_deletada.descricao,
        valor=despesa_deletada.valor,
        data=despesa_deletada.data,
        categoria=despesa_deletada.categoria
    )

# Endpoint para listar uma despesa específica pelo ID
@router.get("/despesas/{despesa_id}", response_model=schemas.Despesa)
def listar_despesa_por_id(despesa_id: int, db: Session = Depends(get_db)):
    return crud.get_despesas_por_id(db=db, despesa_id=despesa_id)

# Endpoint para listar despesas
@router.get("/despesas", response_model=list[schemas.Despesa])
def listar_despesas(db: Session = Depends(get_db)):
    despesas = crud.get_despesas(db)
    return despesas

# Endpoint para listar despesas por categoria
@router.get("/despesas/categoria/{categoria}", response_model=list[schemas.Despesa])
def listar_despesas_por_categoria(categoria: str, db: Session = Depends(get_db)):
    despesas = crud.get_despesas_por_categoria(db, categoria)
    return despesas

# Endpoint para listar despesas por período (data inicial e final)
@router.get("/despesas/periodo", response_model=list[schemas.Despesa])
def listar_despesas_por_periodo(data_inicio: str, data_fim: str, db: Session = Depends(get_db)):
    despesas = crud.get_despesas_por_periodo(db, data_inicio, data_fim)
    return despesas

# Endpoint para relatório de gastos mensais
@router.get("/despesas/relatorio", response_model=dict)
def relatorio_mnensal(db: Session = Depends(get_db)):
    relatorio = crud.get_relatorio_mensal(db)
    return relatorio
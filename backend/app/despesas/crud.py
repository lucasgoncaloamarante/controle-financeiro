from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException

# Criar despesas
def create_despesa(db: Session, descricao: str, valor: float, data: str, categoria: str):
    db_despesa = models.Despesa(descricao=descricao, valor=valor, data=data, categoria=categoria)
    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa

# Select nas despesas
def get_despesas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Despesa).offset(skip).limit(limit).all()

# Select nas despesas pelo ID dela
def get_despesas_por_id(db: Session, despesa_id: int):
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if db_despesa is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return db_despesa  # Aqui retorna um objeto válido

# Update na despesa
def update_despesa(db: Session, despesa_id: int, descricao: str, valor: float, data: str, categoria: str):
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if db_despesa:
        db_despesa.descricao = descricao
        db_despesa.valor = valor
        db_despesa.data = data
        db_despesa.categoria = categoria
        db.commit()
        db.refresh(db_despesa)
    return db_despesa

# Delete na despesa
def delete_despesa(db: Session, despesa_id: int):
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if db_despesa is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    db.delete(db_despesa)
    db.commit()
    return db_despesa


# Select e filtro na despesa por categoria
def get_despesas_por_categoria(db: Session, categoria: str):
    return db.query(models.Despesa).filter(models.Despesa.categoria == categoria).all()
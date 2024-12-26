from pydantic import BaseModel
from datetime import date
from decimal import Decimal

#Esquema para criação de um novo gasto
class DespesaCreate(BaseModel):
    descricao: str
    valor: Decimal
    data: date
    categoria: str

#Esquema para leitura de um gasto (retorno da API)
class Despesa(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    data: date
    categoria: str

    class Config:
        from_attributes = True
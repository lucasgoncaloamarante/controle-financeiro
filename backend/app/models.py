from sqlalchemy import Column, Integer, String, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base
from .database import Base # Cria a base para os modelos

# Define a tabela de gastos
class Despesa(Base):
    __tablename__ = 'despesas'
    
    id = Column(Integer, primary_key=True, index=True)  # ID único para cada gasto
    descricao = Column(String, index=True)  # Descrição do gasto (Ex: Supermercado)
    valor = Column(DECIMAL(10, 2))  # Valor do gasto com precisão de 2 casas decimais
    data = Column(Date)  # Data do gasto
    categoria = Column(String, index=True)  # Categoria do gasto
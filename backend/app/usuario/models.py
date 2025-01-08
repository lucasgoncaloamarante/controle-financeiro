from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from app.database import Base # Cria a base para os modelos

Base = declarative_base()

# Tabela de Usuários
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False) # Armazena a senha com hash
    ativo = Column(Boolean, default=True) # Ativa/Desativa o usuário
    email_verificado = Column(Boolean, default=False)
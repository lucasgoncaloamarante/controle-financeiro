import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://lucas:lucas505@localhost:5432/controle_financeiro"

# Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
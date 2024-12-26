from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Despesa
from app.crud import create_despesa, get_despesas, update_despesa, delete_despesa

# Cria as tabelas no banco (caso não existam)
Base.metadata.create_all(bind=engine)

# Cria uma sessão de banco de dados
db: Session = SessionLocal()

# Teste de criação
nova_despesa = create_despesa(db, "Compra de livros", 120.50, "2024-12-26", "Educação")
print(f"Despesa criada: {nova_despesa.descricao}, Valor: {nova_despesa.valor}")

# Teste de leitura
despesas = get_despesas(db)
print("Lista de despesas:")
for despesa in despesas:
    print(f"{despesa.id} - {despesa.descricao} - {despesa.valor}")

# Teste de atualização
despesa_atualizada = update_despesa(db, nova_despesa.id, "Livros de Python", 130.00, "2024-12-26", "Educação")
print(f"Despesa atualizada: {despesa_atualizada.descricao}, Valor: {despesa_atualizada.valor}")

# Teste de deleção
delete_despesa(db, nova_despesa.id)
print(f"Despesa deletada com sucesso (ID: {nova_despesa.id})")

# Confirma se deletou
despesas_restantes = get_despesas(db)
print("Despesas restantes após deleção:")
for despesa in despesas_restantes:
    print(f"{despesa.id} - {despesa.descricao} - {despesa.valor}")

# Fecha a sessão
db.close()

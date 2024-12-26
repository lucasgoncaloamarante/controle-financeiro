from fastapi.testclient import TestClient
from app.main import app  # Substitua com o caminho correto para o seu app
import pytest

client = TestClient(app)

# Teste de criação de despesa
def test_create_despesa():
    response = client.post(
        "/despesas",
        json={
            "descricao": "Almoço",
            "valor": 50.0,
            "data": "2024-12-25",
            "categoria": "Alimentação",
        },
    )
    assert response.status_code == 200
    assert "id" in response.json()  # Verifica se o ID foi retornado

# Teste de leitura de todas as despesas
def test_get_despesas():
    response = client.get("/despesas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Verifica se a resposta é uma lista

# Teste de leitura de uma despesa por ID
def test_get_despesa_by_id():
    # Criar uma despesa para testar a leitura
    create_response = client.post(
        "/despesas",
        json={
            "descricao": "Almoço",
            "valor": 50.0,
            "data": "2024-12-25",
            "categoria": "Alimentação",
        },
    )
    despesa_id = create_response.json()["id"]

    # Teste de leitura da despesa
    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 200
    assert response.json()["id"] == despesa_id

# Teste de atualização de despesa
def test_update_despesa():
    # Criar uma despesa para testar a atualização
    create_response = client.post(
        "/despesas",
        json={
            "descricao": "Almoço",
            "valor": 50.0,
            "data": "2024-12-25",
            "categoria": "Alimentação",
        },
    )
    despesa_id = create_response.json()["id"]

    # Atualizar a despesa
    response = client.put(
        f"/despesas/{despesa_id}",
        json={
            "descricao": "Jantar",
            "valor": 70.0,
            "data": "2024-12-26",
            "categoria": "Alimentação",
        },
    )
    assert response.status_code == 200
    assert response.json()["descricao"] == "Jantar"  # Verifica se a descrição foi atualizada

# Teste de exclusão de despesa
def test_delete_despesa():
    # Criar uma despesa para testar a exclusão
    create_response = client.post(
        "/despesas",
        json={
            "descricao": "Almoço",
            "valor": 50.0,
            "data": "2024-12-25",
            "categoria": "Alimentação",
        },
    )
    despesa_id = create_response.json()["id"]

    # Excluir a despesa
    response = client.delete(f"/despesas/{despesa_id}")
    assert response.status_code == 200

    # Verificar se a despesa foi excluída
    response = client.get(f"/despesas/{despesa_id}")
    assert response.status_code == 404  # A despesa não deve ser mais encontrada

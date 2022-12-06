import pytest
from app.app import app
import ast

@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_route_cadastro_compra_status(client, mocker):
    mocker.patch('app.services.ORM.cadastro_compra', return_value={})
    response = client.post('/vendas', json = {
        "produtos": [
            {
                "id": 1,
                "nome": "Moranguinho do nordeste",
                "preco": 2,
                "quantidade": 1
            },
            {
                "id": 2,
                "nome": "Verdinha",
                "preco": 4.2,
                "quantidade": 3
            },
                    {
                "id": 10,
                "nome": "Juromeuga",
                "preco": 32,
                "quantidade": 4
            }
        ]
    })
    assert response.status_code == 200

def test_route_cadastro_compra_data(client, mocker):
    mocker.patch('app.services.ORM.cadastro_compra', return_value={})
    response = client.post('/vendas', json = {
        "produtos": [
            {
                "id": 1,
                "nome": "Moranguinho do nordeste",
                "preco": 2,
                "quantidade": 1
            },
            {
                "id": 2,
                "nome": "Verdinha",
                "preco": 4.2,
                "quantidade": 3
            },
                    {
                "id": 10,
                "nome": "Juromeuga",
                "preco": 32,
                "quantidade": 4
            }
        ]
    })
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response["200"] == 'Compra registrada com sucesso.'

def test_route_rank_vendidos_status(client, mocker):
    mocker.patch('app.services.ORM.relatorio_rank_vendidos', return_value={})
    response = client.get('/relatorio/rank_vendidos')
    
    assert response.status_code == 200

def test_route_rank_vendidos_data(client, mocker):

    mocker.patch('app.services.ORM.relatorio_rank_vendidos', return_value={
        "rank_vendidos": [
            {
                "id": 10,
                "nome": "Juromeuga",
                "qtd_produtos_vendidos": 23,
                "valor_total": 736.0
            },
            {
                "id": 2,
                "nome": "Senpaifruit",
                "qtd_produtos_vendidos": 20,
                "valor_total": 84.0
            }
        ]
    })
    response = client.get('/relatorio/rank_vendidos')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response["rank_vendidos"][0] == {
                "id": 10,
                "nome": "Juromeuga",
                "qtd_produtos_vendidos": 23,
                "valor_total": 736.0
            }

def test_route_total_vendas_status(client, mocker):
    mocker.patch('app.services.ORM.relatorio_total_vendas', return_value={
            "total_vendas": {
            "qtd_produtos_vendidos": 55,
            "qtd_vendas": 12,
            "valor_total": 844.0
        }
    })
    response = client.get('/relatorio/total_vendas')
    
    assert response.status_code == 200

def test_route_total_vendas_data(client, mocker):
    mocker.patch('app.services.ORM.relatorio_total_vendas', return_value={
            "total_vendas": {
            "qtd_produtos_vendidos": 55,
            "qtd_vendas": 12,
            "valor_total": 844.0
        }
    })
    response = client.get('/relatorio/total_vendas')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    
    assert decoded_response == {
            "total_vendas": {
            "qtd_produtos_vendidos": 55,
            "qtd_vendas": 12,
            "valor_total": 844.0
        }
    }

def test_route_relatorio_por_produto_status(client, mocker):
    mocker.patch('app.services.ORM.relatorio_por_produto', return_value={
            "vendas_por_produto": [
            {
                "id_produto": 1,
                "nome": "Moranguinho do nordeste",
                "quantidade_total": 12,
                "valor_total": 24.0
            },
            {
                "id_produto": 2,
                "nome": "Verdinha",
                "quantidade_total": 20,
                "valor_total": 84.0
            }
        ]
    })
    response = client.get('/relatorio/por_produto')
    
    assert response.status_code == 200

def test_route_relatorio_por_produto_data(client, mocker):
    mocker.patch('app.services.ORM.relatorio_por_produto', return_value={
            "vendas_por_produto": [
            {
                "id_produto": 1,
                "nome": "Moranguinho do nordeste",
                "quantidade_total": 12,
                "valor_total": 24.0
            },
            {
                "id_produto": 2,
                "nome": "Verdinha",
                "quantidade_total": 20,
                "valor_total": 84.0
            }
        ]
    })
    response = client.get('/relatorio/por_produto')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    
    assert decoded_response == {
            "vendas_por_produto": [
            {
                "id_produto": 1,
                "nome": "Moranguinho do nordeste",
                "quantidade_total": 12,
                "valor_total": 24.0
            },
            {
                "id_produto": 2,
                "nome": "Verdinha",
                "quantidade_total": 20,
                "valor_total": 84.0
            }
        ]
    }

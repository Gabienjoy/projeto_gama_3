import pytest
import ast
from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_cadastro_status_code(client, mocker):
    mocker.patch('services.database.cadastrar', return_value={})
    response = client.post("/cadastro", json={
        "_id": 1,
        "nome": "tomate",
        "preco": 3.50,
        "descricao": "é fruta, não é legume"
    })
    assert response.status_code == 201


def test_cadastro_response(client, mocker):
    mocker.patch('services.database.cadastrar', return_value=({
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    }, 200))
    response = client.post("/cadastro", json={
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    })
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {
        '_id': 1, 'descricao': 'é fruta, não é legume', 'nome': 'tomate', 'preco': 3.5}


def test_consulta_status_code(client, mocker):
    mocker.patch('services.database.consultar', return_value=({
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    }, 200))
    response = client.get("/consulta/Tomate")
    assert response.status_code == 200


def test_consulta_response(client, mocker):
    mocker.patch('services.database.consultar', return_value=({
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    }, 200))
    response = client.get("/consulta/Tomate")
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {
        '_id': 1, 'descricao': 'é fruta, não é legume', 'nome': 'tomate', 'preco': 3.5}


def test_atualizacao_status_code(client, mocker):
    mocker.patch('services.database.consultar', return_value=({
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    }, 200))
    mocker.patch('services.database.atualizar', return_value={})
    response = client.put("/atualizacao", json={
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    })
    assert response.status_code == 200


def test_atualizacao_erro(client, mocker):
    mocker.patch('services.database.consultar', return_value=({}, 404))
    response = client.put("/atualizacao", json={'nome': 'teste'})
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {'error': "Produto não encontrado!"}


def test_delecao_status_code(client, mocker):
    mocker.patch('services.database.consultar', return_value=({
        "_id": 1,
        "nome": "tomate",
        "preco": 3.5,
        "descricao": "é fruta, não é legume"
    }, 200))
    mocker.patch('services.database.deletar', return_value={})
    response = client.delete("/delecao/Tomate")
    assert response.status_code == 200


def test_delecao_erro(client, mocker):
    mocker.patch('services.database.consultar', return_value=({}, 404))
    mocker.patch('services.database.deletar', return_value={})
    response = client.delete("/delecao/teste")
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {'error': 'Produto não encontrado!'}

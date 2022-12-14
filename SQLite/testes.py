import pytest
from app import app
import ast


@pytest.fixture
def client():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_route_listagem_status(client, mocker):
    mocker.patch('orm.func_leitura', return_value=[
    [
        "Sal",
        1.4,
        2
    ],
    [
        "Açúcar",
        2.4,
        1
    ]
    ])
    response = client.get('/leitura')
    assert response.status_code == 200

def test_route_add_produto_status(client, mocker):
    mocker.patch('orm.insert_produto')
    response = client.post('/add_produto', json = {
      "nome": "teste",
      "preco": 3.2,
      "qtd": 4
    })
    assert response.status_code == 201


def test_route_delete_status(client, mocker):
    mocker.patch('orm.func_delete')
    response = client.delete('/delete/arroz')
    assert response.status_code == 200


def test_route_atualizacao_status(client, mocker):
    mocker.patch('orm.func_update', json = {"nome": 'pepino', "qtd": 1})
    response = client.put('/atualizacao/pepino')
    assert response.status_code == 200


def test_route_listagem_data(client, mocker):
    mocker.patch('orm.func_leitura', return_value=[
    [
        "Sal",
        1.4,
        2
    ],
    [
        "Açúcar",
        2.4,
        1
    ]
    ])
    response = client.get('/leitura')
    decoded_response = ast.literal_eval(response.data.decode('utf-8'))
    assert  decoded_response == [
        [
            "Sal",
            1.4,
            2
        ],
        [
            "Açúcar",
            2.4,
            1
        ]
    ]

def test_route_add_produto_error_data(client, mocker):
    mocker.patch('orm.insert_produto')
    response = client.post('/add_produto')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {"Erro": "Esperava receber um JSON"}


def test_route_delete_data(client, mocker):
    mocker.patch('orm.func_delete')
    response = client.delete('/delete/arroz')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {'message': 'Registro removido'}


def test_route_atualizacao_error(client, mocker):
    mocker.patch('orm.func_update', json = {"nome": 'pepino', "qtd": 1})
    response = client.put('/atualizacao/pepino')
    decoded_response = dict(ast.literal_eval(response.data.decode('utf-8')))
    assert decoded_response == {"Erro": "Produto não encontrado"}
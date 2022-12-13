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
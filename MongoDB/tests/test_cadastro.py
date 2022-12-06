import pytest
from flask import Flask, request
from app import app

@pytest.fixture()
def client():
    return app.test_client()


def test_cadastro_status_code(client):
    response = client.get("http://127.0.0.1:5000/cadastro")
    assert response.status_code == 200

from flask import Flask, request
from services import database

app = Flask(__name__)


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    if request.get_json(silent=True):
        produto = request.json
        database.cadastrar(produto)
        return produto, 201
    else:
        return {'error': 'Esperava receber um json no corpo da requisição'}, 400


@app.route('/atualizacao', methods=['PUT'])
def atualizar():
    request.get_json(silent=True)
    produto = request.json
    _, status = database.consultar(produto['nome'])
    if status == 200:
        database.atualizar(produto)
        return produto, 200
    else:
        return {'error': "Produto não encontrado!"}, 404


@app.route('/consulta/<nome>', methods=['GET'])
def consultar(nome):
    produto, _ = database.consultar(nome)
    if produto:
        return produto, 200
    else:
        return {'error': 'Produto não encontrado!'}, 404


@app.route('/delecao/<nome>', methods=['DELETE'])
def deletar(nome):
    produto, _ = database.consultar(nome)
    if produto:
        database.deletar(nome)
        return {'message': 'Produto deletado com sucesso!'}, 200
    else:
        return {'error': 'Produto não encontrado!'}, 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)

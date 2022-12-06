from flask import Flask, request
from pymongo import MongoClient


app = Flask(__name__)

conn = MongoClient(
    'mongodb+srv://gamamagalu.jl8mrli.mongodb.net/projeto_3',

    username='gabisilva',
    password='100113'
)
db = conn['projeto_3']


@app.route('/')
def home():
    return "Bem-vindo(a)!"


# Rota de cadastro
'''
{
"_id":1,
"nome": "Tomate",
"preco":5.00,
"descricao":"Tomate eh fruta"
}
'''


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    if request.get_json(silent=True):
        produto = request.json
        db.produtos.insert_one(produto)
        return produto, 201
    else:
        return {'erro': 'Esperava receber um json no corpo da requisição'}, 400


# Rota de alteração

@app.route('/atualizacao/', methods=['PUT'])
def atualizar():
    request.get_json(silent=True)
    produto = request.json
    _, status = consultar(produto['nome'])
    if status == 200:
        db.produtos.update_one(
            {'nome': produto['nome']},
            {'$set':
                {
                    'nome': produto['nome'],
                    'preco': produto['preco'],
                    'descricao': produto['descricao']
                }
             }
        )
        return produto, 200
    else:
        return {'erro': "Produto não encontrado!"}, 404


# Rota de consulta

@app.route('/consulta/<nome>', methods=['GET'])
def consultar(nome):
    produto = db.produtos.find_one({'nome': nome})
    if produto:
        return produto, 200
    else:
        return {'error': 'Produto não encontrado!'}, 404


# Rota de deleção

@app.route('/delecao/<nome>', methods=['DELETE'])
def deletar(nome):
    produto = db.produtos.find_one({'nome': nome})
    if produto:
        db.produtos.delete_one({'nome': nome})
        return {'message': 'Produto deletado com sucesso!'}, 200
    else:
        return {'error': 'Produto não encontrado!'}, 404


if __name__ == '__main__':
    app.run(debug=True)

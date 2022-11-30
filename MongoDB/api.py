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
    return "Olá, to funfando"


# Rota de cadastro
'''{"id":1,
"nome": "Tomate",
"preco":5.00,
"descricao":"Tomate eh fruta"}'''


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    if request.get_json(silent=True):
        produto = request.json
        db.produtos.insert_one(produto)
        return produto, 201
    else:
        return {'erro': 'Esperava receber um json no corpo da requisição'}, 400


# Rota de consulta

@app.route('/consultar/<nome>', methods=['GET'])
def consultar_nome(nome):
    produto = db.produtos.find_one({'nome': nome}, {'_id': False})
    if produto:
        return produto, 200
    else:
        return {'error': 'Produto não encontrado!'}, 404


if __name__ == '__main__':
    app.run(debug=True)

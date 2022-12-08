from pymongo import MongoClient

conn = MongoClient(
    'mongodb+srv://gamamagalu.jl8mrli.mongodb.net/projeto_3',

    username='gabisilva',
    password='100113'
)
db = conn['projeto_3']


def cadastrar(produto):
    db.produtos.insert_one(produto)


def atualizar(produto):
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


def consultar(nome):
    return db.produtos.find_one({'nome': nome}), 200


def deletar(nome):
    db.produtos.delete_one({'nome': nome})

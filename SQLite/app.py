from flask import Flask, request
import orm

app = Flask(__name__)


@app.route("/add_produto", methods=['POST'])
def add_produto():
    if request.get_json(silent=True):
        produtos = request.json
        orm.insert_produto(produtos)
        return produtos, 201
    else:
        return {"Erro": "Esperava receber um JSON"}, 400


@app.route("/leitura", methods=['GET'])
def leitura():
    resultado = orm.func_leitura()
    return resultado, 200


@app.route('/delecao/<nome>', methods=['DELETE'])
def delete_name(nome):
    orm.func_delete(nome)
    return {'message': 'Registro removido'}, 200


@app.route('/leitura/<nome>', methods=['GET'])
def leitura_nome(nome):
    resultado = orm.func_read(nome)
    return resultado, 200


@app.route('/atualizacao/<nome>', methods=['PUT'])
def atualiza(nome):
    try:
        resultado, status = leitura_nome(nome)
        if status == 200:
            if request.get_json(silent=True):
                produtos = request.json
                resp = orm.func_update(nome, produtos)
                return resp, 200
            else:
                return {"Erro": "Produto não encontrado"}
        else:
            return {"Erro": "Produto não encontrado"}
    except:
        return {"Erro": "Erro ao atualizar o produto"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)

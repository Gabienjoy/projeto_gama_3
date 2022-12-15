from flask import Flask, request
from app.services import ORM
from http import HTTPStatus

app = Flask(__name__)

ORM.initialise()


@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if request.method == 'POST':
        ORM.cadastro_compra(request.get_json())
        return {
            HTTPStatus.OK.value: 'Compra registrada com sucesso.'
        }
    elif request.method == 'GET':
        return ORM.consultar_vendas()


@app.route('/vendas/limpar', methods=['GET'])
def vendas_limpar():
    ORM.limpar_vendas()
    return {
        HTTPStatus.OK.value: 'Vendas limpadas com sucesso.'
    }


@app.route('/relatorio/por_produto', methods=['GET'])
def relatorio_por_produto():
    return ORM.relatorio_por_produto()


@app.route('/relatorio/total_vendas', methods=['GET'])
def relatorio_total_vendas():
    return ORM.relatorio_total_vendas()


@app.route('/relatorio/rank_vendidos', methods=['GET'])
def relatorio_rank_vendidos():
    return ORM.relatorio_rank_vendidos()


if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, request
from services import ORM
from http import HTTPStatus

app = Flask(__name__)

ORM.initialise()

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if request.method == 'POST':
        print(request.get_json())
        ORM.cadastro_compra(request.get_json())
        return {
            HTTPStatus.OK.value: 'Compra registrada com sucesso.'
        }

@app.route('/relatorio/por_produto', methods=['GET'])
def relatorio_por_produto():
    return ORM.relatorio_por_produto()


if __name__=="__main__":
    app.run(debug=True);
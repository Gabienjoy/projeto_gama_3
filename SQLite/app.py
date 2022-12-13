from flask import Flask, request
import sqlite3 as sql

app = Flask(__name__)
banco = 'banco.bd'
 
# Função
def abrir_conexao(banco):
    conexao = sql.connect(banco)
    cursor = conexao.cursor()
    return conexao, cursor

def fechar_conexao(conexao):
    conexao.commit()
    conexao.close()

# Comandos SQL
contagem = "SELECT COUNT(*) FROM produtos;"
select_todos = "SELECT * FROM produtos;"
select_nome = "SELECT * FROM produtos WHERE nome = ?;"
insert = "INSERT INTO produtos VALUES (:nome,:preco,:qtd);"
delete = "DELETE FROM produtos WHERE nome = ?;"
update = '''
UPDATE produtos SET
    qtd = :qtd
WHERE nome like :nome  
'''

@app.route("/add_produto", methods=['POST'])
def add_produto():
    if request.get_json(silent=True):
        produtos = request.json
        conexao, cursor = abrir_conexao(banco)
        cursor.execute(insert, produtos)
        fechar_conexao(conexao)
        return produtos , 201
    else:
        return {"Erro": "Esperava receber um JSON"} , 400

@app.route("/leitura")
def leitura():
    conexao, cursor = abrir_conexao(banco)
    cursor.execute(select_todos)
    resultado = cursor.fetchall()
    fechar_conexao(conexao)
    return resultado, 200

@app.route('/delete/<nome>', methods=['DELETE'])
def delete_name(nome):
    conexao, cursor = abrir_conexao(banco)
    resultado = cursor.execute(delete, [nome]).rowcount
    fechar_conexao(conexao)
    return {'message': 'Registro removido'}, 200

@app.route('/read/<nome>')
def read_name(nome):
    conexao, cursor = abrir_conexao(banco)
    resultado = cursor.execute(select_nome, [nome]).fetchall()
    fechar_conexao(conexao)
    return resultado, 200

@app.route('/atualizacao/<nome>', methods=['PUT'])
def atualiza(nome):

    resultado, status = read_name(nome)
    if status == 200: 
        if request.get_json(silent=True):
            produtos = request.json
            conexao, cursor = abrir_conexao(banco)
            # aluno['id'] = id
            resp = {"nome": nome, "qtd": produtos["qtd"]}
            cursor.execute(update, resp)
            fechar_conexao(conexao)
            return resp, 200
        else:
            return {"Erro": "Produto não encontrado "}
    else:
        return {"Erro": "Produto não encontrado"}

if __name__=="__main__":
    app.run(debug=True);
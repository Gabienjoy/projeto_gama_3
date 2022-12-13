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
    preco = :preco,
WHERE nome like :nome  
'''


@app.route("/")
def index():
    conexao, cursor = abrir_conexao(banco)
    resultado = cursor.execute(select_todos).fetchone()
    fechar_conexao(conexao)
    return {'registros': f'{resultado} alunos'}

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

@app.route('/delete/<nome>')
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
    return resultado

@app.route('/update/<nome>')
#?nome=teste&idade=0&filhos=1&estado=AC&altura=0.07&formacao=Ensino+Superior
def update_name(nome):
    consulta = read_name(nome)
    if consulta: # existe nome no banco de dados
        produtos=request.args.to_dict() #{chave: valor, chave:valor,...}
        if produtos: # se tem argumento
            conexao, cursor = abrir_conexao(banco)
            cursor.execute(update, produtos)
            fechar_conexao(conexao)
            return produtos
        else: # se não tem argumento
            return {'error': 'Produto não encontrado!'}
    else: # não existe nome no banco de dados
        return {'error': 'Produto não encontrado 1!'}

if __name__=="__main__":
    app.run(debug=True);
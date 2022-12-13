import sqlite3 as sql

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

def insert_produto(produtos):
    conexao, cursor = abrir_conexao(banco)
    cursor.execute(insert, produtos)
    fechar_conexao(conexao)

def func_leitura():
    conexao, cursor = abrir_conexao(banco)
    cursor.execute(select_todos)
    resultado = cursor.fetchall()
    fechar_conexao(conexao)
    return resultado

def func_delete(nome):
    conexao, cursor = abrir_conexao(banco)
    resultado = cursor.execute(delete, [nome]).rowcount
    fechar_conexao(conexao)

def func_read(nome):
    conexao, cursor = abrir_conexao(banco)
    resultado = cursor.execute(select_nome, [nome]).fetchall()
    fechar_conexao(conexao)
    return resultado

def func_update(nome, produtos):
    conexao, cursor = abrir_conexao(banco)
    resp = {"nome": nome, "qtd": produtos["qtd"]}
    cursor.execute(update, resp)
    fechar_conexao(conexao)
    return resp
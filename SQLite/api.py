import sqlite3 as sql

conexao = sql.connect("banco.bd")
cursor = conexao.cursor()

create_table = '''
CREATE TABLE produtos(
  nome     TEXT NOT NULL PRIMARY KEY,
  preco    REAL  NOT NULL,
  qtd   INTEGER  NOT NULL
);
'''
cursor.execute("DROP TABLE IF EXISTS produtos;")
cursor.execute(create_table)

insert_values = '''
INSERT INTO produtos VALUES
('Arroz',8.,4),
('Feijão',3.4,2),
('Óleo de soja',2.9,3),
('Sal',1.4,2),
('Açúcar',2.4,1),
('Café',5.1,6),
('Molho de tomate',2.6,8);

'''

cursor.execute(insert_values)

conexao.commit()

resultado = cursor.execute("SELECT COUNT(*) FROM produtos;").fetchone()
print(resultado)

conexao.close()
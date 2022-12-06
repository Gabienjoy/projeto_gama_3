
from sqlalchemy import create_engine, update, Column, Float, String, Integer, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# docker inspect <container_id>
engine = create_engine('mysql+mysqlconnector://root:root@172.17.0.2:3306/projeto', echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)

class Compras(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())

class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    preco = Column(Float)

class Transacoes(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer)
    valor_total = Column(Float)
    id_compra = Column(Integer, ForeignKey("compras.id"))
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    

def initialise() -> None:
    Base.metadata.create_all(engine)

def cadastro_compra(compra: dict) -> None:
    session = Session()
    nova_compra = Compras()
    session.add(nova_compra)
    for produto in compra["produtos"]:
        novo_produto = session.query(Produtos).filter(Produtos.id == produto["id"]).one_or_none()
        if not novo_produto:
            novo_produto = Produtos(
                id = produto["id"],
                nome = produto["nome"],
                preco =produto["preco"]
            )
            session.add(novo_produto)

        nova_transacao = Transacoes(
            quantidade = produto["quantidade"],
            valor_total = produto["quantidade"] * produto["preco"],
            id_compra = nova_compra.id,
            id_produto = novo_produto.id
        )
        session.add(nova_transacao)
    session.commit()
    session.close()
    return

def relatorio_por_produto() -> dict:
    session = Session()
    vendas = {
        "vendas_por_produto": []
    }
    for venda in session.query(Transacoes).join(Produtos).with_entities(
        Produtos.nome, 
        Transacoes.id_produto,  
        func.sum(Transacoes.quantidade).cast(Integer).label('quantidade_total'),
        func.sum(Transacoes.valor_total).label('valor_total')
    ).group_by(Transacoes.id_produto, Produtos.nome).all():
        vendas["vendas_por_produto"].append(dict(venda))
    return vendas

def relatorio_total_vendas() -> dict:
    session = Session()
    vendas = {
        "total_vendas": None
    }

    for venda in session.query(Transacoes).with_entities(
        func.sum(Transacoes.quantidade).cast(Integer).label('qtd_produtos_vendidos'),
        func.sum(Transacoes.valor_total).label('valor_total')
    ).all():
        vendas["total_vendas"] = dict(venda)

    vendas["total_vendas"]["qtd_vendas"] = session.query(Compras).count()

    return vendas

def relatorio_rank_vendidos() -> dict:
    session = Session()
    vendas = {
        "rank_vendidos": []
    }

    for venda in session.query(Transacoes).join(Produtos).with_entities(
        Produtos.id,
        Produtos.nome,
        func.sum(Transacoes.quantidade).cast(Integer).label('qtd_produtos_vendidos'),
        func.sum(Transacoes.valor_total).label('valor_total')
    ).group_by(Produtos.id, Produtos.nome).order_by(func.sum(Transacoes.quantidade).cast(Integer).desc()).all():
        vendas["rank_vendidos"].append(dict(venda))

    return vendas

def limpar_vendas():
    session = Session()
    session.query(Transacoes).delete()
    session.query(Compras).delete()
    session.commit()
    session.close()

def consultar_vendas():
    session = Session()
    compras = {
        "compras": []
    }
    for compra in session.query(Compras).all():
        compras["compras"].append({
            "id": compra.__dict__["id"],
            "items": [],
            "valor_total": 0
        })
    for transacao in session.query(Transacoes).all():
        for compra in compras["compras"]:
            if transacao.__dict__["id_compra"] == compra["id"]:
                compra["items"].append({
                    "id": transacao.__dict__["id_produto"],
                    "quantidade": transacao.__dict__["quantidade"]
                })
                compra["valor_total"] += transacao.__dict__["valor_total"]
    for produto in session.query(Produtos).all():
        for compra in compras["compras"]:
            for item in compra["items"]:
                if item["id"] == produto.__dict__["id"]:
                    item["nome"] = produto.__dict__["nome"]
                    item["preco"] = produto.__dict__["preco"]
    
    session.close()
    return compras
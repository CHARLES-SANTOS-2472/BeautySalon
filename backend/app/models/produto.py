from app.extensions import db

class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150))

    codigo_barras = db.Column(db.String(50))

    estoque = db.Column(db.Integer)

    preco_compra = db.Column(db.Numeric(10,2))

    preco_venda = db.Column(db.Numeric(10,2))

    ativo = db.Column(db.Boolean, default=True)
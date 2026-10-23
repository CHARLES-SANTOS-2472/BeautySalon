from app.extensions import db


class ItemVenda(db.Model):

    __tablename__ = "itens_venda"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    venda_id = db.Column(
        db.Integer,
        db.ForeignKey("vendas.id"),
        nullable=False
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False
    )

    preco_unitario = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    subtotal = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    produto = db.relationship(
        "Produto",
        backref="itens_venda"
    )
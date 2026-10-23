from app.extensions import db
from datetime import datetime


class Venda(db.Model):

    __tablename__ = "vendas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    funcionario_id = db.Column(
        db.Integer,
        db.ForeignKey("funcionarios.id"),
        nullable=False
    )

    data_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    total = db.Column(
        db.Numeric(10, 2),
        default=0,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Concluída",
        nullable=False
    )

    cliente = db.relationship(
        "Cliente",
        backref="vendas"
    )

    funcionario = db.relationship(
        "Funcionario",
        backref="vendas"
    )

    itens = db.relationship(
        "ItemVenda",
        backref="venda",
        lazy=True,
        cascade="all, delete-orphan"
    )
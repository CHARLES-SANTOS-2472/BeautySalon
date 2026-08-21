from app.extensions import db

class Funcionario(db.Model):

    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    telefone = db.Column(db.String(20))

    cargo = db.Column(db.String(60))

    agendamentos = db.relationship(
        "Agendamento",
        backref="funcionario",
        lazy=True
    )

    percentual_comissao = db.Column(db.Float)

    ativo = db.Column(db.Boolean, default=True)
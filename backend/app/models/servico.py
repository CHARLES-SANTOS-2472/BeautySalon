from app.extensions import db

class Servico(db.Model):

    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    descricao = db.Column(db.Text)

    duracao = db.Column(db.Integer)

    agendamentos = db.relationship(
        "Agendamento",
        backref="servico",
        lazy=True
    )

    valor = db.Column(db.Numeric(10,2))

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias_servico.id")
    )

    categoria = db.relationship("CategoriaServico")
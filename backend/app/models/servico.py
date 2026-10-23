from app.extensions import db

class Servico(db.Model):

    __tablename__ = "servicos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=False
    )

    duracao = db.Column(
        db.Integer,
        nullable=False
    )

    valor = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias_servico.id"),
        nullable=False
    )

    categoria = db.relationship(
        "CategoriaServico"
    )

    agendamentos = db.relationship(
        "Agendamento",
        backref="servico",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "duracao": self.duracao,
            "valor": float(self.valor) if self.valor is not None else None,
            "categoria_id": self.categoria_id,
            "categoria": (
                self.categoria.nome
                if self.categoria
                else None
            )
        }

    

    

    
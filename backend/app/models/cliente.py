from datetime import datetime

from app.extensions import db


class Cliente(db.Model):

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    cpf = db.Column(db.String(14), unique=True)

    telefone = db.Column(db.String(20))

    email = db.Column(db.String(120))

    data_nascimento = db.Column(db.Date)

    endereco = db.Column(db.String(250))

    observacoes = db.Column(db.Text)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    agendamentos = db.relationship(
        "Agendamento",
        backref="cliente",
        lazy=True
    )

    def to_dict(self):

        return {

            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "endereco": self.endereco,
            "observacoes": self.observacoes,
            "ativo": self.ativo

        }





"""from app.extensions import db
from datetime import datetime

class Cliente(db.Model):

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120), nullable=False)

    telefone = db.Column(db.String(20))

    cpf = db.Column(db.String(20), unique=True)

    email = db.Column(db.String(120))

    data_nascimento = db.Column(db.Date)

    endereco = db.Column(db.String(250))

    observacoes = db.Column(db.Text)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )"""
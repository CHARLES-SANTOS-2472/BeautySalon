from datetime import datetime
from app.extensions import db


class Agendamento(db.Model):

    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)

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

    servico_id = db.Column(
        db.Integer,
        db.ForeignKey("servicos.id"),
        nullable=False
    )

    data_hora = db.Column(
        db.DateTime,
        nullable=False
    )

    duracao = db.Column(
        db.Integer,
        nullable=False
    )

    observacoes = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Agendado"
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    """# ========================================================
    # RELACIONAMENTOS
    # ========================================================

    cliente = db.relationship(
        "Cliente",
        backref="agendamentos"
    )

    funcionario = db.relationship(
        "Funcionario",
        backref="agendamentos"
    )

    servico = db.relationship(
        "Servico",
        backref="agendamentos"
    )"""







    # ========================================================
    # TO_DICT
    # ========================================================

    def to_dict(self):

        return {

            "id": self.id,

            "cliente": self.cliente.nome
            if self.cliente else None,


            "funcionario": self.funcionario.nome
            if self.funcionario else None,


            "servico": self.servico.nome
            if self.servico else None,


            "data_hora":
                self.data_hora.strftime(
                    "%d/%m/%Y %H:%M"
                )
                if self.data_hora else None,


            "duracao": self.duracao,


            "status": self.status,


            "observacoes": self.observacoes

        }



   
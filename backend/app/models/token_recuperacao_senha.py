from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db


class TokenRecuperacaoSenha(db.Model):
    __tablename__ = "tokens_recuperacao_senha"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    codigo_hash = db.Column(
        db.String(255),
        nullable=False
    )

    expira_em = db.Column(
        db.DateTime,
        nullable=False
    )

    usado_em = db.Column(db.DateTime)

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def definir_codigo(self, codigo):
        self.codigo_hash = generate_password_hash(codigo)

    def verificar_codigo(self, codigo):
        return check_password_hash(
            self.codigo_hash,
            codigo
        )
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from app.models.usuario import Usuario


def autenticar(email, senha):

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario is None:
        return None

    if not usuario.verificar_senha(senha):
        return None

    access_token = create_access_token(

        identity=str(usuario.id),

        additional_claims={

            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil

        }

    )

    refresh_token = create_refresh_token(
        identity=str(usuario.id)
    )

    return access_token, refresh_token, usuario



"""from flask_jwt_extended import create_access_token

from app.models.usuario import Usuario


def autenticar(email, senha):

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario is None:
        return None

    if not usuario.verificar_senha(senha):
        return None

    token = create_access_token(

        identity=str(usuario.id),

        additional_claims={

            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil

        }

    )

    return token, usuario"""







"""
from flask_jwt_extended import create_access_token
from app.models.usuario import Usuario


def autenticar(email, senha):

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario is None:
        return None

    if not usuario.verificar_senha(senha):
        return None

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "perfil": usuario.perfil,
            "nome": usuario.nome
        }
    )

    return token, usuario
    """
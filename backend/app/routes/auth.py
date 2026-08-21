from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.auth.auth_service import autenticar

auth_bp = Blueprint("auth", __name__)


# ==========================================
# LOGIN
# ==========================================
@auth_bp.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON inválido."
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios."
        }), 400

    resultado = autenticar(email, senha)

    if resultado is None:

        return jsonify({
            "erro": "Usuário ou senha inválidos."
        }), 401

    access_token, refresh_token, usuario = resultado

    return jsonify({

        "access_token": access_token,

        "refresh_token": refresh_token,

        "usuario":{

            "id": usuario.id,

            "nome": usuario.nome,

            "email": usuario.email,

            "perfil": usuario.perfil

        }

    }),200


# ==========================================
# PERFIL DO USUÁRIO LOGADO
# ==========================================
@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():

    usuario_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({

        "usuario_id": usuario_id,

        "nome": claims["nome"],

        "perfil": claims["perfil"]

    })


# ==========================================
# REFRESH DO PERFIL DO USUÁRIO LOGADO
# ==========================================

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    usuario_id = get_jwt_identity()

    novo_token = create_access_token(
        identity=usuario_id
    )

    return jsonify({
        "access_token": novo_token
    })


# ==========================================
# ROTA DE LOGOU DO PERFIL DO USUÁRIO LOGADO
# ==========================================

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200







"""
from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.auth.auth_service import autenticar

auth_bp = Blueprint("auth", __name__)


# ==========================================
# LOGIN
# ==========================================
@auth_bp.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON inválido."
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios."
        }), 400

    resultado = autenticar(email, senha)

    if resultado is None:

        return jsonify({
            "erro": "Usuário ou senha inválidos."
        }), 401

    token, usuario = resultado

    return jsonify({

        "access_token": token,

        "usuario": {

            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil

        }

    }), 200


# ==========================================
# PERFIL DO USUÁRIO LOGADO
# ==========================================
@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():

    usuario_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({

        "usuario_id": usuario_id,

        "nome": claims["nome"],

        "perfil": claims["perfil"]

    })"""
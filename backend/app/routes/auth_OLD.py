from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])

def login():

    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios."
        }), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario is None:
        return jsonify({
            "erro": "Usuário não encontrado."
        }), 404

    if not usuario.verificar_senha(senha):
        return jsonify({
            "erro": "Senha inválida."
        }), 401

    token = create_access_token(
        identity=str(usuario.id),  # JWT moderno trabalha melhor com string
        additional_claims={
            "perfil": usuario.perfil,
            "nome": usuario.nome
        }
    )

    return jsonify({
        "access_token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }
    }), 200


"""Cria uma rota protegida"""

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt


@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():

    usuario_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({

        "usuario_id": usuario_id,

        "perfil": claims["perfil"],

        "nome": claims["nome"]

    })












"""@auth_bp.route("/login", methods=["POST"])

def login():

    dados = request.get_json()

    usuario = Usuario.query.filter_by(
        email=dados["email"]
    ).first()

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if not usuario.verificar_senha(dados["senha"]):
        return jsonify({"erro": "Senha inválida"}), 401

    token = create_access_token(
        identity=usuario.id,
        additional_claims={
            "perfil": usuario.perfil
        }
    )

    return jsonify({
        "token": token,
        "usuario": usuario.nome,
        "perfil": usuario.perfil
    })



TEMPORÁRIO  -  INÍCIO

@auth_bp.route("/login", methods=["GET"])
def login_get():
    return {
        "mensagem": "A rota de login está funcionando. Use POST para autenticar."
    }

TEMPORÁRIO  -  FIM



@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():

    usuario_id = get_jwt_identity()

    return jsonify({
        "usuario_id": usuario_id
    })"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.usuario import Usuario
from app.auth.decorators import perfil_requerido

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["POST"])
@jwt_required()
@perfil_requerido("Administrador")
def cadastrar_usuario():

    dados = request.get_json()


    usuario_existente = Usuario.query.filter_by(
        email=dados["email"]
    ).first()

    if usuario_existente:

        return jsonify({
            "erro": "Já existe um usuário com esse e-mail."
        }), 400

    usuario = Usuario(
        nome=dados["nome"],
        email=dados["email"],
        perfil=dados["perfil"]
    )

    usuario.definir_senha(dados["senha"])

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201


@usuarios_bp.route("/usuarios", methods=["GET"])
@jwt_required()
@perfil_requerido("Administrador")
def listar_usuarios():

    usuarios = Usuario.query.all()

    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "perfil": u.perfil
        }
        for u in usuarios
    ])


@usuarios_bp.route("/admin", methods=["GET"])
@jwt_required()
@perfil_requerido("Administrador")
def admin():

    return jsonify({
        "mensagem": "Área do administrador"
    })
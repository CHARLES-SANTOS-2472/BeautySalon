import secrets
import smtplib

from datetime import datetime, timedelta
from email.mime.text import MIMEText

from flask import Blueprint, request, jsonify, current_app

from app.extensions import db
from app.models.usuario import Usuario
from app.models.token_recuperacao_senha import TokenRecuperacaoSenha

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


# ==========================================
# ALTERAR SENHA
# ==========================================

@auth_bp.route("/alterar-senha", methods=["PUT"])
@jwt_required()
def alterar_senha():
    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON inválido."
        }), 400

    senha_atual = dados.get("senha_atual")
    nova_senha = dados.get("nova_senha")
    confirmar_nova_senha = dados.get("confirmar_nova_senha")

    if not senha_atual or not nova_senha or not confirmar_nova_senha:
        return jsonify({
            "erro": "Senha atual, nova senha e confirmação são obrigatórias."
        }), 400

    if nova_senha != confirmar_nova_senha:
        return jsonify({
            "erro": "A confirmação da nova senha não confere."
        }), 400

    if len(nova_senha) < 8:
        return jsonify({
            "erro": "A nova senha deve ter pelo menos 8 caracteres."
        }), 400

    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get(usuario_id)

    if usuario is None or not usuario.ativo:
        return jsonify({
            "erro": "Usuário não encontrado ou inativo."
        }), 404

    if not usuario.verificar_senha(senha_atual):
        return jsonify({
            "erro": "A senha atual está incorreta."
        }), 401

    if usuario.verificar_senha(nova_senha):
        return jsonify({
            "erro": "A nova senha deve ser diferente da senha atual."
        }), 400

    usuario.definir_senha(nova_senha)
    db.session.commit()

    return jsonify({
        "mensagem": "Senha alterada com sucesso."
    }), 200




def enviar_codigo_recuperacao(destinatario, codigo):
    mensagem = MIMEText(
        (
            "Olá!\n\n"
            "Seu código para redefinir a senha do Beauty Salon é:\n\n"
            f"{codigo}\n\n"
            "Ele é válido por 15 minutos e pode ser usado uma única vez.\n"
            "Se você não solicitou esta troca, ignore esta mensagem."
        ),
        "plain",
        "utf-8"
    )

    mensagem["Subject"] = "Redefinição de senha - Beauty Salon"
    mensagem["From"] = current_app.config["SMTP_FROM"]
    mensagem["To"] = destinatario

    with smtplib.SMTP(
        current_app.config["SMTP_HOST"],
        current_app.config["SMTP_PORT"],
        timeout=15
    ) as servidor:
        servidor.starttls()
        servidor.login(
            current_app.config["SMTP_USER"],
            current_app.config["SMTP_PASSWORD"]
        )
        servidor.send_message(mensagem)


@auth_bp.route("/esqueci-senha", methods=["POST"])
def solicitar_redefinicao_senha():
    dados = request.get_json()

    if not dados or not dados.get("email"):
        return jsonify({
            "erro": "O e-mail é obrigatório."
        }), 400

    email = dados["email"].strip().lower()

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    resposta = {
        "mensagem": (
            "Se o e-mail estiver cadastrado, "
            "você receberá um código de recuperação."
        )
    }


    if usuario is None or not usuario.ativo:
        return jsonify({
            "erro": "E-mail não cadastrado."
        }), 404

    """if usuario is None or not usuario.ativo:
        return jsonify(resposta), 200"""

    TokenRecuperacaoSenha.query.filter_by(
        usuario_id=usuario.id
    ).delete()

    codigo = f"{secrets.randbelow(1_000_000):06d}"

    token = TokenRecuperacaoSenha(
        usuario_id=usuario.id,
        expira_em=datetime.utcnow() + timedelta(minutes=15)
    )

    token.definir_codigo(codigo)

    db.session.add(token)

    try:
        enviar_codigo_recuperacao(usuario.email, codigo)
        db.session.commit()

    except Exception:
        db.session.rollback()

        current_app.logger.exception(
            "Erro ao enviar código de recuperação de senha."
        )

        return jsonify({
            "erro": "Não foi possível enviar o código. Tente novamente."
        }), 500

    return jsonify(resposta), 200


@auth_bp.route("/redefinir-senha", methods=["POST"])
def redefinir_senha():
    dados = request.get_json()

    campos = [
        "email",
        "codigo",
        "nova_senha",
        "confirmar_nova_senha"
    ]

    if not dados or any(not dados.get(campo) for campo in campos):
        return jsonify({
            "erro": "Todos os campos são obrigatórios."
        }), 400

    if dados["nova_senha"] != dados["confirmar_nova_senha"]:
        return jsonify({
            "erro": "A confirmação da nova senha não confere."
        }), 400

    if len(dados["nova_senha"]) < 8:
        return jsonify({
            "erro": "A nova senha deve ter pelo menos 8 caracteres."
        }), 400

    email = dados["email"].strip().lower()

    usuario = Usuario.query.filter_by(
        email=email
    ).first()

    if usuario is None or not usuario.ativo:
        return jsonify({
            "erro": "Código ou e-mail inválido."
        }), 400

    token = TokenRecuperacaoSenha.query.filter_by(
        usuario_id=usuario.id,
        usado_em=None
    ).order_by(
        TokenRecuperacaoSenha.criado_em.desc()
    ).first()

    if (
        token is None
        or token.expira_em < datetime.utcnow()
        or not token.verificar_codigo(dados["codigo"])
    ):
        return jsonify({
            "erro": "Código inválido ou expirado."
        }), 400

    usuario.definir_senha(dados["nova_senha"])
    token.usado_em = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "mensagem": (
            "Senha redefinida com sucesso. "
            "Agora você já pode entrar."
        )
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
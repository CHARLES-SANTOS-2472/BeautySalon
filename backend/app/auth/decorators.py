from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def perfil_requerido(*perfis):
    """
    Exemplo:
    @perfil_requerido("Administrador")
    @perfil_requerido("Administrador", "Gerente")
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Verifica se existe um JWT válido
            verify_jwt_in_request()

            # Recupera os dados gravados no token
            claims = get_jwt()

            perfil_usuario = claims.get("perfil")

            # Verifica se o perfil possui permissão
            if perfil_usuario not in perfis:
                return jsonify({
                    "erro": "Acesso negado.",
                    "perfil": perfil_usuario
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator



"""from app.auth.decorators import perfil_requerido

@auth_bp.route("/admin")
@perfil_requerido("Administrador")
def painel_admin():

    return {
        "mensagem":"Bem-vindo Administrador"
    }
"""


"""@usuarios_bp.route("/usuarios", methods=["GET"])
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
    ])"""




"""from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def perfil_requerido(*perfis):

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            perfil = claims.get("perfil")

            if perfil not in perfis:
                return jsonify({
                    "erro": "Você não possui permissão."
                }), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper"""




from flask import Blueprint, request, jsonify
from datetime import datetime

from app.extensions import db
from app.models.cliente import Cliente

from flask_jwt_extended import jwt_required
from app.auth.decorators import perfil_requerido

clientes_bp = Blueprint("clientes", __name__)


# ==========================================
# LISTAR CLIENTES
# ==========================================
@clientes_bp.route("/clientes", methods=["GET"])
@jwt_required()
def listar_clientes():

    clientes = Cliente.query.filter_by(ativo=True).all()

    return jsonify([cliente.to_dict() for cliente in clientes])


# ==========================================
# CADASTRAR CLIENTE
# ==========================================
@clientes_bp.route("/clientes", methods=["POST"])
@jwt_required()
@perfil_requerido("Administrador", "Gerente", "Funcionário")
def cadastrar_cliente():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "JSON inválido."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "erro": "O nome é obrigatório."
        }), 400

    # Verifica CPF existente
    cpf = dados.get("cpf")

    if cpf:
        cliente_existente = Cliente.query.filter_by(
            cpf=cpf
        ).first()

        if cliente_existente:
            if cliente_existente.ativo:
                return jsonify({
                    "erro": "CPF já cadastrado."
                }), 400

            cliente_existente.ativo = True

            db.session.commit()

            return jsonify({
                "mensagem": "Cliente reativado com sucesso.",
                "cliente": cliente_existente.to_dict()
            }), 200


    if not dados.get("email"):

        existe = Cliente.query.filter_by(
            email=dados["email"]
        ).first()

        if existe:
            return jsonify({
                "erro":"E-mail já cadastrado."
            }),400

    data_nascimento = None

    if dados.get("data_nascimento"):

        data_nascimento = datetime.strptime(
            dados["data_nascimento"],
            "%Y-%m-%d"
        ).date()

    cliente = Cliente(

        nome=dados["nome"],

        cpf=dados.get("cpf"),

        telefone=dados.get("telefone"),

        email=dados.get("email"),

        data_nascimento=data_nascimento,

        endereco=dados.get("endereco"),

        observacoes=dados.get("observacoes")

    )

    db.session.add(cliente)
    db.session.commit()

    return jsonify({

        "mensagem": "Cliente cadastrado com sucesso.",

        "cliente": cliente.to_dict()

    }), 201


# ==========================================
# BUSCAR CLIENTE POR ID
# ==========================================
@clientes_bp.route("/clientes/<int:id>", methods=["GET"])
@jwt_required()
def buscar_cliente(id):

    cliente = Cliente.query.get(id)

    if cliente is None or not cliente.ativo:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    return jsonify(cliente.to_dict())


# ==========================================
# ATUALIZAR CLIENTE
# ==========================================
@clientes_bp.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
@perfil_requerido("Administrador", "Gerente")
def atualizar_cliente(id):

    cliente = Cliente.query.get(id)

    if cliente is None or not cliente.ativo:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    dados = request.get_json()

    if "nome" in dados:
        cliente.nome = dados["nome"]

    if "telefone" in dados:
        cliente.telefone = dados["telefone"]

    if "email" in dados:
        cliente.email = dados["email"]

    if "cpf" in dados:
        cliente.cpf = dados["cpf"]

    if "endereco" in dados:
        cliente.endereco = dados["endereco"]

    if "observacoes" in dados:
        cliente.observacoes = dados["observacoes"]

    if "data_nascimento" in dados:

        cliente.data_nascimento = datetime.strptime(
            dados["data_nascimento"],
            "%Y-%m-%d"
        ).date()

    db.session.commit()

    return jsonify({

        "mensagem": "Cliente atualizado com sucesso.",

        "cliente": cliente.to_dict()

    })


# ==========================================
# DESATIVAR CLIENTE
# ==========================================
@clientes_bp.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
@perfil_requerido("Administrador")
def excluir_cliente(id):

    cliente = Cliente.query.get(id)

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    cliente.ativo = False

    db.session.commit()

    return jsonify({
        "mensagem": "Cliente desativado com sucesso."
    })





# ==========================================
# LISTAR CLIENTES INATIVOS
# ==========================================
@clientes_bp.route("/clientes/inativos", methods=["GET"])
@jwt_required()
@perfil_requerido("Administrador", "Gerente")
def listar_clientes_inativos():

    clientes = Cliente.query.filter_by(
        ativo=False
    ).all()

    return jsonify([
        cliente.to_dict()
        for cliente in clientes
    ]), 200


# ==========================================
# REATIVAR CLIENTE
# ==========================================
@clientes_bp.route(
    "/clientes/<int:id>/reativar",
    methods=["PUT"]
)
@jwt_required()
@perfil_requerido("Administrador", "Gerente")
def reativar_cliente(id):

    cliente = Cliente.query.get(id)

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404

    if cliente.ativo:
        return jsonify({
            "erro": "Cliente já está ativo."
        }), 400

    cliente.ativo = True

    db.session.commit()

    return jsonify({
        "mensagem": "Cliente reativado com sucesso.",
        "cliente": cliente.to_dict()
    }), 200





"""# ==========================================
# AGENDAR CLIENTE
# ==========================================
agendamentos = db.relationship(
    "Agendamento",
    backref="cliente",
    lazy=True
)
"""




"""from flask import Blueprint, jsonify

clientes_bp = Blueprint(
    "clientes",
    __name__
)

@clientes_bp.route("/clientes", methods=["GET"])
def listar_clientes():

    return jsonify({
        "mensagem": "Módulo Clientes funcionando!"
    })"""
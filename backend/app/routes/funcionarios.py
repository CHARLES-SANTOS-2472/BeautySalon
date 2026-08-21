from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.funcionario import Funcionario


funcionarios_bp = Blueprint(
    "funcionarios",
    __name__
)


# ========================================================
# CADASTRAR FUNCIONÁRIO
# ========================================================

@funcionarios_bp.route(
    "/funcionarios",
    methods=["POST"]
)
@jwt_required()
def cadastrar_funcionario():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Nenhum dado foi enviado."
        }), 400

    nome = dados.get("nome")

    if not nome:
        return jsonify({
            "erro": "O nome do funcionário é obrigatório."
        }), 400

    funcionario = Funcionario(

        nome=nome,

        telefone=dados.get(
            "telefone"
        ),

        cargo=dados.get(
            "cargo"
        ),

        percentual_comissao=dados.get(
            "percentual_comissao"
        ),

        ativo=dados.get(
            "ativo",
            True
        )
    )

    db.session.add(funcionario)
    db.session.commit()

    return jsonify({

        "mensagem":
        "Funcionário cadastrado com sucesso!",

        "funcionario": {

            "id": funcionario.id,

            "nome": funcionario.nome,

            "telefone": funcionario.telefone,

            "cargo": funcionario.cargo,

            "percentual_comissao":
                funcionario.percentual_comissao,

            "ativo": funcionario.ativo
        }

    }), 201


# ========================================================
# LISTAR FUNCIONÁRIOS
# ========================================================

@funcionarios_bp.route(
    "/funcionarios",
    methods=["GET"]
)
@jwt_required()
def listar_funcionarios():

    funcionarios = Funcionario.query.all()

    return jsonify([

        {
            "id": f.id,

            "nome": f.nome,

            "telefone": f.telefone,

            "cargo": f.cargo,

            "percentual_comissao":
                f.percentual_comissao,

            "ativo": f.ativo
        }

        for f in funcionarios

    ]), 200


# ========================================================
# BUSCAR FUNCIONÁRIO
# ========================================================

@funcionarios_bp.route(
    "/funcionarios/<int:id>",
    methods=["GET"]
)
@jwt_required()
def buscar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    return jsonify({

        "id": funcionario.id,

        "nome": funcionario.nome,

        "telefone": funcionario.telefone,

        "cargo": funcionario.cargo,

        "percentual_comissao":
            funcionario.percentual_comissao,

        "ativo": funcionario.ativo

    }), 200


# ========================================================
# ATUALIZAR FUNCIONÁRIO
# ========================================================

@funcionarios_bp.route(
    "/funcionarios/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def atualizar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Nenhum dado foi enviado."
        }), 400

    if "nome" in dados:

        if not dados["nome"]:
            return jsonify({
                "erro":
                "O nome do funcionário não pode ser vazio."
            }), 400

        funcionario.nome = dados["nome"]

    if "telefone" in dados:

        funcionario.telefone = dados["telefone"]

    if "cargo" in dados:

        funcionario.cargo = dados["cargo"]

    if "percentual_comissao" in dados:

        funcionario.percentual_comissao = (
            dados["percentual_comissao"]
        )

    if "ativo" in dados:

        funcionario.ativo = dados["ativo"]

    db.session.commit()

    return jsonify({

        "mensagem":
        "Funcionário atualizado com sucesso!"

    }), 200


# ========================================================
# EXCLUIR FUNCIONÁRIO
# ========================================================

@funcionarios_bp.route(
    "/funcionarios/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def excluir_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    db.session.delete(funcionario)

    db.session.commit()

    return jsonify({

        "mensagem":
        "Funcionário removido com sucesso!"

    }), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.servico import Servico
from app.models.categoria_servico import CategoriaServico

from app.auth.decorators import perfil_requerido


servicos_bp = Blueprint(
    "servicos",
    __name__
)


# ========================================================
# LISTAR SERVIÇOS
# ========================================================

@servicos_bp.route(
    "/servicos",
    methods=["GET"]
)
@jwt_required()
def listar_servicos():

    servicos = Servico.query.all()

    return jsonify([
        servico.to_dict()
        for servico in servicos
    ]), 200


# ========================================================
# BUSCAR SERVIÇO POR ID
# ========================================================

@servicos_bp.route(
    "/servicos/<int:id>",
    methods=["GET"]
)
@jwt_required()
def buscar_servico(id):

    servico = Servico.query.get(id)

    if servico is None:

        return jsonify({
            "erro": "Serviço não encontrado."
        }), 404

    return jsonify(
        servico.to_dict()
    ), 200


# ========================================================
# CADASTRAR SERVIÇO
# ========================================================

@servicos_bp.route(
    "/servicos",
    methods=["POST"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def cadastrar_servico():

    dados = request.get_json()

    if not dados:

        return jsonify({
            "erro": "JSON inválido."
        }), 400


    # ----------------------------------------------------
    # VALIDAR NOME
    # ----------------------------------------------------

    if not dados.get("nome"):

        return jsonify({
            "erro": "O nome do serviço é obrigatório."
        }), 400


    # ----------------------------------------------------
    # VALIDAR DURAÇÃO
    # ----------------------------------------------------

    if "duracao" not in dados:

        return jsonify({
            "erro": "A duração é obrigatória."
        }), 400


    if (
        not isinstance(
            dados["duracao"],
            int
        )
        or dados["duracao"] <= 0
    ):

        return jsonify({
            "erro":
            "A duração deve ser um número inteiro maior que zero."
        }), 400


    # ----------------------------------------------------
    # VALIDAR VALOR
    # ----------------------------------------------------

    if "valor" not in dados:

        return jsonify({
            "erro": "O valor do serviço é obrigatório."
        }), 400


    try:

        valor = float(
            dados["valor"]
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "erro": "Valor inválido."
        }), 400


    if valor < 0:

        return jsonify({
            "erro":
            "O valor não pode ser negativo."
        }), 400


    # ----------------------------------------------------
    # VALIDAR CATEGORIA
    # ----------------------------------------------------

    if not dados.get("categoria_id"):

        return jsonify({
            "erro":
            "A categoria do serviço é obrigatória."
        }), 400


    categoria = CategoriaServico.query.get(
        dados["categoria_id"]
    )


    if categoria is None:

        return jsonify({
            "erro":
            "Categoria de serviço não encontrada."
        }), 404


    # ----------------------------------------------------
    # CRIAR SERVIÇO
    # ----------------------------------------------------

    servico = Servico(

        nome=dados["nome"],

        descricao=dados.get(
            "descricao"
        ),

        duracao=dados["duracao"],

        valor=valor,

        categoria_id=dados[
            "categoria_id"
        ]
    )


    db.session.add(
        servico
    )

    db.session.commit()


    return jsonify({

        "mensagem":
        "Serviço cadastrado com sucesso.",

        "servico":
        servico.to_dict()

    }), 201


# ========================================================
# ATUALIZAR SERVIÇO
# ========================================================

@servicos_bp.route(
    "/servicos/<int:id>",
    methods=["PUT"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def atualizar_servico(id):

    servico = Servico.query.get(id)


    if servico is None:

        return jsonify({
            "erro":
            "Serviço não encontrado."
        }), 404


    dados = request.get_json()


    if not dados:

        return jsonify({
            "erro":
            "JSON inválido."
        }), 400


    # ----------------------------------------------------
    # NOME
    # ----------------------------------------------------

    if "nome" in dados:

        if not dados["nome"]:

            return jsonify({
                "erro":
                "O nome não pode ser vazio."
            }), 400

        servico.nome = dados["nome"]


    # ----------------------------------------------------
    # DESCRIÇÃO
    # ----------------------------------------------------

    if "descricao" in dados:

        servico.descricao = dados[
            "descricao"
        ]


    # ----------------------------------------------------
    # DURAÇÃO
    # ----------------------------------------------------

    if "duracao" in dados:

        if (
            not isinstance(
                dados["duracao"],
                int
            )
            or dados["duracao"] <= 0
        ):

            return jsonify({
                "erro":
                "A duração deve ser maior que zero."
            }), 400

        servico.duracao = dados[
            "duracao"
        ]


    # ----------------------------------------------------
    # VALOR
    # ----------------------------------------------------

    if "valor" in dados:

        try:

            valor = float(
                dados["valor"]
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "erro":
                "Valor inválido."
            }), 400


        if valor < 0:

            return jsonify({
                "erro":
                "O valor não pode ser negativo."
            }), 400


        servico.valor = valor


    # ----------------------------------------------------
    # CATEGORIA
    # ----------------------------------------------------

    if "categoria_id" in dados:

        categoria = CategoriaServico.query.get(
            dados["categoria_id"]
        )


        if categoria is None:

            return jsonify({
                "erro":
                "Categoria de serviço não encontrada."
            }), 404


        servico.categoria_id = categoria.id


    # ----------------------------------------------------
    # SALVAR
    # ----------------------------------------------------

    db.session.commit()


    return jsonify({

        "mensagem":
        "Serviço atualizado com sucesso.",

        "servico":
        servico.to_dict()

    }), 200


# ========================================================
# EXCLUIR SERVIÇO
# ========================================================

@servicos_bp.route(
    "/servicos/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def excluir_servico(id):

    servico = Servico.query.get(id)


    if servico is None:

        return jsonify({
            "erro":
            "Serviço não encontrado."
        }), 404


    db.session.delete(
        servico
    )

    db.session.commit()


    return jsonify({

        "mensagem":
        "Serviço removido com sucesso."

    }), 200
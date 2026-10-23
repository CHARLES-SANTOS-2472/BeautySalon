from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.produto import Produto

from app.auth.decorators import perfil_requerido


produtos_bp = Blueprint(
    "produtos",
    __name__
)


# ========================================================
# CADASTRAR PRODUTO
# ========================================================

@produtos_bp.route(
    "/produtos",
    methods=["POST"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def cadastrar_produto():

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
            "erro": "O nome do produto é obrigatório."
        }), 400


    # ----------------------------------------------------
    # VALIDAR ESTOQUE
    # ----------------------------------------------------

    if "estoque" not in dados:

        return jsonify({
            "erro": "O estoque é obrigatório."
        }), 400


    estoque = dados["estoque"]

    if (
        not isinstance(estoque, int)
        or estoque < 0
    ):

        return jsonify({
            "erro":
            "O estoque deve ser um número inteiro maior ou igual a zero."
        }), 400


    # ----------------------------------------------------
    # VALIDAR PREÇO DE COMPRA
    # ----------------------------------------------------

    if "preco_compra" not in dados:

        return jsonify({
            "erro": "O preço de compra é obrigatório."
        }), 400


    try:

        preco_compra = float(
            dados["preco_compra"]
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "erro": "Preço de compra inválido."
        }), 400


    if preco_compra < 0:

        return jsonify({
            "erro":
            "O preço de compra não pode ser negativo."
        }), 400


    # ----------------------------------------------------
    # VALIDAR PREÇO DE VENDA
    # ----------------------------------------------------

    if "preco_venda" not in dados:

        return jsonify({
            "erro": "O preço de venda é obrigatório."
        }), 400


    try:

        preco_venda = float(
            dados["preco_venda"]
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "erro": "Preço de venda inválido."
        }), 400


    if preco_venda < 0:

        return jsonify({
            "erro":
            "O preço de venda não pode ser negativo."
        }), 400


    # ----------------------------------------------------
    # CRIAR PRODUTO
    # ----------------------------------------------------

    produto = Produto(

        nome=dados["nome"],

        codigo_barras=dados.get(
            "codigo_barras"
        ),

        estoque=estoque,

        preco_compra=preco_compra,

        preco_venda=preco_venda,

        ativo=True
    )


    db.session.add(produto)

    db.session.commit()

    return jsonify({

        "mensagem":
        "Produto cadastrado com sucesso.",

        "produto": {

            "id": produto.id,

            "nome": produto.nome,

            "codigo_barras":
            produto.codigo_barras,

            "estoque":
            produto.estoque,

            "preco_compra":
            float(produto.preco_compra),

            "preco_venda":
            float(produto.preco_venda),

            "ativo":
            produto.ativo
        }

    }), 201





# ========================================================
# LISTAR PRODUTOS
# ========================================================

@produtos_bp.route(
    "/produtos",
    methods=["GET"]
)
@jwt_required()
def listar_produtos():

    produtos = Produto.query.filter_by(
        ativo=True
    ).all()

    return jsonify([
        {
            "id": produto.id,
            "nome": produto.nome,
            "codigo_barras": produto.codigo_barras,
            "estoque": produto.estoque,
            "preco_compra": float(produto.preco_compra),
            "preco_venda": float(produto.preco_venda),
            "ativo": produto.ativo
        }
        for produto in produtos
    ]), 200



# ========================================================
# BUSCAR PRODUTO POR ID
# ========================================================

@produtos_bp.route(
    "/produtos/<int:id>",
    methods=["GET"]
)
@jwt_required()
def buscar_produto(id):

    produto = Produto.query.get(id)

    if produto is None or not produto.ativo:

        return jsonify({
            "erro": "Produto não encontrado."
        }), 404

    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "codigo_barras": produto.codigo_barras,
        "estoque": produto.estoque,
        "preco_compra": float(produto.preco_compra),
        "preco_venda": float(produto.preco_venda),
        "ativo": produto.ativo
    }), 200




# ========================================================
# ATUALIZAR PRODUTO
# ========================================================

@produtos_bp.route(
    "/produtos/<int:id>",
    methods=["PUT"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def atualizar_produto(id):

    produto = Produto.query.get(id)

    if produto is None or not produto.ativo:

        return jsonify({
            "erro": "Produto não encontrado."
        }), 404

    dados = request.get_json()

    if not dados:

        return jsonify({
            "erro": "JSON inválido."
        }), 400


    # ----------------------------------------------------
    # NOME
    # ----------------------------------------------------

    if "nome" in dados:

        if not dados["nome"]:

            return jsonify({
                "erro": "O nome não pode ser vazio."
            }), 400

        produto.nome = dados["nome"]


    # ----------------------------------------------------
    # CÓDIGO DE BARRAS
    # ----------------------------------------------------

    if "codigo_barras" in dados:

        produto.codigo_barras = dados[
            "codigo_barras"
        ]


    # ----------------------------------------------------
    # ESTOQUE
    # ----------------------------------------------------

    if "estoque" in dados:

        estoque = dados["estoque"]

        if (
            not isinstance(estoque, int)
            or estoque < 0
        ):

            return jsonify({
                "erro":
                "O estoque deve ser um número inteiro maior ou igual a zero."
            }), 400

        produto.estoque = estoque


    # ----------------------------------------------------
    # PREÇO DE COMPRA
    # ----------------------------------------------------

    if "preco_compra" in dados:

        try:

            preco_compra = float(
                dados["preco_compra"]
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "erro":
                "Preço de compra inválido."
            }), 400

        if preco_compra < 0:

            return jsonify({
                "erro":
                "O preço de compra não pode ser negativo."
            }), 400

        produto.preco_compra = preco_compra


    # ----------------------------------------------------
    # PREÇO DE VENDA
    # ----------------------------------------------------

    if "preco_venda" in dados:

        try:

            preco_venda = float(
                dados["preco_venda"]
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "erro":
                "Preço de venda inválido."
            }), 400

        if preco_venda < 0:

            return jsonify({
                "erro":
                "O preço de venda não pode ser negativo."
            }), 400

        produto.preco_venda = preco_venda


    db.session.commit()


    return jsonify({

        "mensagem":
        "Produto atualizado com sucesso.",

        "produto": {

            "id": produto.id,

            "nome": produto.nome,

            "codigo_barras":
            produto.codigo_barras,

            "estoque":
            produto.estoque,

            "preco_compra":
            float(produto.preco_compra),

            "preco_venda":
            float(produto.preco_venda),

            "ativo":
            produto.ativo
        }

    }), 200



# ========================================================
# DESATIVAR PRODUTO
# ========================================================

@produtos_bp.route(
    "/produtos/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
@perfil_requerido(
    "Administrador",
    "Gerente"
)
def excluir_produto(id):

    produto = Produto.query.get(id)

    if produto is None:

        return jsonify({
            "erro": "Produto não encontrado."
        }), 404

    if not produto.ativo:

        return jsonify({
            "erro": "Produto já está desativado."
        }), 400

    produto.ativo = False

    db.session.commit()

    return jsonify({

        "mensagem":
        "Produto desativado com sucesso.",

        "produto": {

            "id": produto.id,

            "nome": produto.nome,

            "ativo": produto.ativo
        }

    }), 200




    
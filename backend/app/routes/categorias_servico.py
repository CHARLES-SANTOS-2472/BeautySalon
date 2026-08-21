from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.categoria_servico import CategoriaServico


categorias_servico_bp = Blueprint(
    "categorias_servico",
    __name__
)


# ========================================================
# CADASTRAR CATEGORIA
# ========================================================

@categorias_servico_bp.route(
    "/categorias-servico",
    methods=["POST"]
)
@jwt_required()
def cadastrar_categoria():

    dados = request.get_json()

    if not dados or not dados.get("nome"):
        return jsonify({
            "erro": "O nome da categoria é obrigatório."
        }), 400

    categoria = CategoriaServico(
        nome=dados["nome"]
    )

    db.session.add(categoria)
    db.session.commit()

    return jsonify({
        "mensagem": "Categoria cadastrada com sucesso!",
        "categoria": {
            "id": categoria.id,
            "nome": categoria.nome
        }
    }), 201


# ========================================================
# LISTAR CATEGORIAS
# ========================================================

@categorias_servico_bp.route(
    "/categorias-servico",
    methods=["GET"]
)
@jwt_required()
def listar_categorias():

    categorias = CategoriaServico.query.all()

    return jsonify([
        {
            "id": categoria.id,
            "nome": categoria.nome
        }
        for categoria in categorias
    ])


# ========================================================
# BUSCAR CATEGORIA
# ========================================================

@categorias_servico_bp.route(
    "/categorias-servico/<int:id>",
    methods=["GET"]
)
@jwt_required()
def buscar_categoria(id):

    categoria = CategoriaServico.query.get_or_404(id)

    return jsonify({
        "id": categoria.id,
        "nome": categoria.nome
    })


# ========================================================
# ATUALIZAR CATEGORIA
# ========================================================

@categorias_servico_bp.route(
    "/categorias-servico/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def atualizar_categoria(id):

    categoria = CategoriaServico.query.get_or_404(id)

    dados = request.get_json()

    if not dados or not dados.get("nome"):
        return jsonify({
            "erro": "O nome da categoria é obrigatório."
        }), 400

    categoria.nome = dados["nome"]

    db.session.commit()

    return jsonify({
        "mensagem": "Categoria atualizada com sucesso!",
        "categoria": {
            "id": categoria.id,
            "nome": categoria.nome
        }
    })


# ========================================================
# EXCLUIR CATEGORIA
# ========================================================

@categorias_servico_bp.route(
    "/categorias-servico/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def excluir_categoria(id):

    categoria = CategoriaServico.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({
        "mensagem": "Categoria removida com sucesso."
    })
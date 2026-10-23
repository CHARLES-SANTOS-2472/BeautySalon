from datetime import datetime, timedelta

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app.extensions import db
from app.models.agendamento import Agendamento
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.produto import Produto
from app.models.servico import Servico
from app.models.venda import Venda
from app.models.item_venda import ItemVenda


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def obter_dashboard():
    inicio_hoje = datetime.combine(
        datetime.today().date(),
        datetime.min.time()
    )
    fim_hoje = inicio_hoje + timedelta(days=1)

    agendamentos_hoje = Agendamento.query.filter(
        Agendamento.data_hora >= inicio_hoje,
        Agendamento.data_hora < fim_hoje
    ).count()

    limite_estoque_baixo = 5

    produtos_estoque_baixo = Produto.query.filter(
        Produto.estoque <= limite_estoque_baixo
    ).count()

    faturamento = db.session.query(
        func.coalesce(func.sum(Venda.total), 0)
    ).filter(
        Venda.status == "Concluída"
    ).scalar()

    return jsonify({
        "clientes": Cliente.query.count(),
        "funcionarios": Funcionario.query.count(),
        "servicos": Servico.query.count(),
        "produtos": Produto.query.count(),
        "produtos_estoque_baixo": produtos_estoque_baixo,
        "agendamentos": Agendamento.query.count(),
        "agendamentos_hoje": agendamentos_hoje,
        "vendas": Venda.query.count(),
        "faturamento": float(faturamento),
    }), 200



# ========================================================
# SERVIÇOS MAIS REALIZADOS
# ========================================================

@dashboard_bp.route("/dashboard/servicos-mais-realizados", methods=["GET"])
@jwt_required()
def servicos_mais_realizados():
    resultados = db.session.query(
        Servico.id.label("servico_id"),
        Servico.nome.label("servico"),
        func.count(Agendamento.id).label("quantidade")
    ).join(
        Agendamento,
        Agendamento.servico_id == Servico.id
    ).filter(
        Agendamento.status == "Finalizado"
    ).group_by(
        Servico.id,
        Servico.nome
    ).order_by(
        func.count(Agendamento.id).desc()
    ).all()

    return jsonify({
        "servicos_mais_realizados": [
            {
                "servico_id": item.servico_id,
                "servico": item.servico,
                "quantidade": item.quantidade
            }
            for item in resultados
        ]
    }), 200



# ========================================================
# PRODUTOS MAIS VENDIDOS
# ========================================================

@dashboard_bp.route("/dashboard/produtos-mais-vendidos", methods=["GET"])
@jwt_required()
def produtos_mais_vendidos():
    resultados = db.session.query(
        Produto.id.label("produto_id"),
        Produto.nome.label("produto"),
        func.sum(ItemVenda.quantidade).label("quantidade_vendida")
    ).join(
        ItemVenda,
        ItemVenda.produto_id == Produto.id
    ).join(
        Venda,
        ItemVenda.venda_id == Venda.id
    ).filter(
        Venda.status == "Concluída"
    ).group_by(
        Produto.id,
        Produto.nome
    ).order_by(
        func.sum(ItemVenda.quantidade).desc()
    ).all()

    return jsonify({
        "produtos_mais_vendidos": [
            {
                "produto_id": item.produto_id,
                "produto": item.produto,
                "quantidade_vendida": item.quantidade_vendida
            }
            for item in resultados
        ]
    }), 200



# ========================================================
# DASHBOARD COMPLETO
# ========================================================

@dashboard_bp.route("/dashboard/completo", methods=["GET"])
@jwt_required()
def dashboard_completo():
    inicio_hoje = datetime.combine(
        datetime.today().date(),
        datetime.min.time()
    )
    fim_hoje = inicio_hoje + timedelta(days=1)

    agendamentos_hoje = Agendamento.query.filter(
        Agendamento.data_hora >= inicio_hoje,
        Agendamento.data_hora < fim_hoje
    ).count()

    produtos_estoque_baixo = Produto.query.filter(
        Produto.estoque <= 5
    ).count()

    faturamento = db.session.query(
        func.coalesce(func.sum(Venda.total), 0)
    ).filter(
        Venda.status == "Concluída"
    ).scalar()

    servicos = db.session.query(
        Servico.id.label("servico_id"),
        Servico.nome.label("servico"),
        func.count(Agendamento.id).label("quantidade")
    ).join(
        Agendamento,
        Agendamento.servico_id == Servico.id
    ).filter(
        Agendamento.status == "Finalizado"
    ).group_by(
        Servico.id,
        Servico.nome
    ).order_by(
        func.count(Agendamento.id).desc()
    ).all()

    produtos = db.session.query(
        Produto.id.label("produto_id"),
        Produto.nome.label("produto"),
        func.sum(ItemVenda.quantidade).label("quantidade_vendida")
    ).join(
        ItemVenda,
        ItemVenda.produto_id == Produto.id
    ).join(
        Venda,
        ItemVenda.venda_id == Venda.id
    ).filter(
        Venda.status == "Concluída"
    ).group_by(
        Produto.id,
        Produto.nome
    ).order_by(
        func.sum(ItemVenda.quantidade).desc()
    ).all()

    return jsonify({
        "indicadores_gerais": {
            "clientes": Cliente.query.count(),
            "funcionarios": Funcionario.query.count(),
            "servicos": Servico.query.count(),
            "produtos": Produto.query.count(),
            "vendas": Venda.query.count(),
            "faturamento_total": float(faturamento)
        },
        "agendamentos": {
            "total": Agendamento.query.count(),
            "hoje": agendamentos_hoje
        },
        "estoque": {
            "produtos_estoque_baixo": produtos_estoque_baixo
        },
        "servicos_mais_realizados": [
            {
                "servico_id": item.servico_id,
                "servico": item.servico,
                "quantidade": item.quantidade
            }
            for item in servicos
        ],
        "produtos_mais_vendidos": [
            {
                "produto_id": item.produto_id,
                "produto": item.produto,
                "quantidade_vendida": item.quantidade_vendida
            }
            for item in produtos
        ]
    }), 200
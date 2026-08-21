from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.agendamento import Agendamento

from datetime import datetime, timedelta

agendamentos_bp = Blueprint("agendamentos", __name__)


# ========================================================
# CADASTRAR AGENDAMENTO
# ========================================================

@agendamentos_bp.route("/agendamentos", methods=["POST"])
@jwt_required()
def cadastrar_agendamento():

    dados = request.get_json()


    try:

        data_inicio = datetime.fromisoformat(
            dados["data_hora"]
        )

    except ValueError:

        return jsonify({
            "erro": "Data inválida. Use formato AAAA-MM-DDTHH:MM"
        }),400


    duracao = dados["duracao"]


    fim_novo = data_inicio + timedelta(
        minutes=duracao
    )


    conflitos = Agendamento.query.filter(
        Agendamento.funcionario_id == dados["funcionario_id"],
        Agendamento.data_hora < fim_novo
    ).all()


    for item in conflitos:

        fim_existente = (
            item.data_hora +
            timedelta(minutes=item.duracao)
        )


        if data_inicio < fim_existente:

            return jsonify({

                "erro":
                "Funcionário já possui atendimento nesse horário."

            }),400



    agendamento = Agendamento(

        cliente_id=dados["cliente_id"],

        funcionario_id=dados["funcionario_id"],

        servico_id=dados["servico_id"],

        data_hora=data_inicio,

        duracao=duracao,

        observacoes=dados.get(
            "observacoes",
            ""
        ),

        status="Agendado"

    )


    db.session.add(agendamento)

    db.session.commit()


    return jsonify({

        "mensagem":
        "Agendamento criado com sucesso!"

    }),201


# ========================================================
# LISTAR AGENDAMENTOS
# ========================================================

@agendamentos_bp.route("/agendamentos", methods=["GET"])
@jwt_required()
def listar_agendamentos():

    agendamentos = Agendamento.query.all()

    for a in agendamentos:
        print("AGENDAMENTO:", a.id)
        print("cliente_id:", a.cliente_id)
        print("cliente:", a.cliente)

        print("funcionario_id:", a.funcionario_id)
        print("funcionario:", a.funcionario)

        print("servico_id:", a.servico_id)
        print("servico:", a.servico)

    return jsonify([a.to_dict() for a in agendamentos])


# ========================================================
# BUSCAR AGENDAMENTO
# ========================================================

@agendamentos_bp.route("/agendamentos/<int:id>", methods=["GET"])
@jwt_required()
def buscar_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    return jsonify(
        agendamento.to_dict()
    )


# ========================================================
# ATUALIZAR AGENDAMENTO
# ========================================================

@agendamentos_bp.route("/agendamentos/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    dados = request.get_json()

    # ----------------------------------------------------
    # CLIENTE
    # ----------------------------------------------------

    if "cliente_id" in dados:
        agendamento.cliente_id = dados["cliente_id"]


    # ----------------------------------------------------
    # FUNCIONÁRIO
    # ----------------------------------------------------

    if "funcionario_id" in dados:
        agendamento.funcionario_id = dados["funcionario_id"]


    # ----------------------------------------------------
    # SERVIÇO
    # ----------------------------------------------------

    if "servico_id" in dados:
        agendamento.servico_id = dados["servico_id"]


    # ----------------------------------------------------
    # DATA E HORA
    # ----------------------------------------------------

    if "data_hora" in dados:

        try:

            nova_data_hora = datetime.fromisoformat(
                dados["data_hora"]
            )

        except (ValueError, TypeError):

            return jsonify({
                "erro": "Data inválida. Use formato AAAA-MM-DDTHH:MM"
            }), 400

    else:

        nova_data_hora = agendamento.data_hora


    # ----------------------------------------------------
    # DURAÇÃO
    # ----------------------------------------------------

    if "duracao" in dados:

        nova_duracao = dados["duracao"]

    else:

        nova_duracao = agendamento.duracao


    # ----------------------------------------------------
    # VALIDAR DURAÇÃO
    # ----------------------------------------------------

    if not isinstance(nova_duracao, int) or nova_duracao <= 0:

        return jsonify({
            "erro": "A duração deve ser um número inteiro maior que zero."
        }), 400


    # ----------------------------------------------------
    # VERIFICAR CONFLITO DE HORÁRIO
    # ----------------------------------------------------

    fim_novo = nova_data_hora + timedelta(
        minutes=nova_duracao
    )


    conflitos = Agendamento.query.filter(
        Agendamento.funcionario_id == agendamento.funcionario_id,
        Agendamento.id != agendamento.id,
        Agendamento.data_hora < fim_novo
    ).all()


    for item in conflitos:

        fim_existente = (
            item.data_hora +
            timedelta(minutes=item.duracao)
        )


        if nova_data_hora < fim_existente:

            return jsonify({

                "erro":
                "Funcionário já possui atendimento nesse horário."

            }), 400


    # ----------------------------------------------------
    # APLICAR ALTERAÇÕES
    # ----------------------------------------------------

    agendamento.data_hora = nova_data_hora

    agendamento.duracao = nova_duracao


    if "status" in dados:

        agendamento.status = dados["status"]


    if "observacoes" in dados:

        agendamento.observacoes = dados["observacoes"]


    # ----------------------------------------------------
    # SALVAR
    # ----------------------------------------------------

    db.session.commit()


    return jsonify({

        "mensagem":
        "Agendamento atualizado com sucesso!"

    }), 200


# ========================================================
# EXCLUIR AGENDAMENTO
# ========================================================

@agendamentos_bp.route("/agendamentos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    db.session.delete(agendamento)

    db.session.commit()

    return jsonify({
        "mensagem": "Agendamento removido."
    })


# ========================================================
# ALTERAR STATUS DO AGENDAMENTO
# ========================================================

@agendamentos_bp.route(
    "/agendamentos/<int:id>/status",
    methods=["PUT"]
)
@jwt_required()
def alterar_status(id):

    agendamento = Agendamento.query.get_or_404(id)

    dados = request.get_json()

    novo_status = dados.get("status")


    status_permitidos = [
        "Agendado",
        "Confirmado",
        "Em atendimento",
        "Finalizado",
        "Cancelado"
    ]


    if novo_status not in status_permitidos:

        return jsonify({
            "erro": "Status inválido",
            "status_permitidos": status_permitidos
        }), 400


    agendamento.status = novo_status

    db.session.commit()


    return jsonify({
        "mensagem": "Status atualizado com sucesso!",
        "status": agendamento.status
    })






"""# ========================================================
# ALTERAR STATUS DO AGENDAMENTO
# ========================================================

@agendamentos_bp.route(
    "/agendamentos/<int:id>/status",
    methods=["PUT"]
)
@jwt_required()
def alterar_status(id):

    agendamento = Agendamento.query.get_or_404(id)

    dados = request.get_json()

    novo_status = dados.get("status")


    status_permitidos = [
        "Agendado",
        "Confirmado",
        "Em atendimento",
        "Finalizado",
        "Cancelado"
    ]


    if novo_status not in status_permitidos:

        return jsonify({
            "erro": "Status inválido",
            "permitidos": status_permitidos
        }), 400


    agendamento.status = novo_status

    db.session.commit()


    return jsonify({
        "mensagem": "Status atualizado com sucesso!",
        "status": agendamento.status
    })"""






"""# ========================================================
# TO_DICT
# ========================================================
def to_dict(self):
    return {
        "id": self.id,
        "cliente_id": self.cliente_id,
        "funcionario_id": self.funcionario_id,
        "servico_id": self.servico_id,
        "data_hora": self.data_hora.isoformat() if self.data_hora else None,
        "status": self.status,
        "observacoes": self.observacoes
    }"""

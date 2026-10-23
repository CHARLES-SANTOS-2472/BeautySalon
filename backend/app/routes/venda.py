from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario

from decimal import Decimal
from datetime import datetime, timedelta


vendas_bp = Blueprint("vendas", __name__)


# ========================================================
# CADASTRAR VENDA
# ========================================================

@vendas_bp.route("/vendas", methods=["POST"])
@jwt_required()
def cadastrar_venda():

    dados = request.get_json()

    # ----------------------------------------------------
    # VALIDAR JSON
    # ----------------------------------------------------

    if not dados:

        return jsonify({
            "erro": "JSON inválido."
        }), 400


    # ----------------------------------------------------
    # VALIDAR CLIENTE
    # ----------------------------------------------------

    cliente_id = dados.get("cliente_id")

    if not cliente_id:

        return jsonify({
            "erro": "O cliente é obrigatório."
        }), 400


    cliente = Cliente.query.get(cliente_id)

    if cliente is None:

        return jsonify({
            "erro": "Cliente não encontrado."
        }), 404


    # ----------------------------------------------------
    # VALIDAR FUNCIONÁRIO
    # ----------------------------------------------------

    funcionario_id = dados.get("funcionario_id")

    if not funcionario_id:

        return jsonify({
            "erro": "O funcionário é obrigatório."
        }), 400


    funcionario = Funcionario.query.get(funcionario_id)

    if funcionario is None:

        return jsonify({
            "erro": "Funcionário não encontrado."
        }), 404


    # ----------------------------------------------------
    # VALIDAR ITENS
    # ----------------------------------------------------

    itens = dados.get("itens")

    if not itens or not isinstance(itens, list):

        return jsonify({
            "erro": "A venda deve possuir pelo menos um item."
        }), 400


    try:

        total = Decimal("0.00")

        itens_processados = []


        # =================================================
        # PROCESSAR CADA ITEM
        # =================================================

        for item in itens:

            produto_id = item.get("produto_id")
            quantidade = item.get("quantidade")


            # ---------------------------------------------
            # PRODUTO
            # ---------------------------------------------

            if not produto_id:

                return jsonify({
                    "erro": "O produto é obrigatório."
                }), 400


            produto = Produto.query.get(produto_id)


            if produto is None:

                return jsonify({
                    "erro": f"Produto {produto_id} não encontrado."
                }), 404


            # ---------------------------------------------
            # PRODUTO ATIVO
            # ---------------------------------------------

            if not produto.ativo:

                return jsonify({
                    "erro":
                    f"O produto '{produto.nome}' está inativo."
                }), 400


            # ---------------------------------------------
            # QUANTIDADE
            # ---------------------------------------------

            if not isinstance(quantidade, int) or quantidade <= 0:

                return jsonify({
                    "erro":
                    "A quantidade deve ser um número inteiro maior que zero."
                }), 400


            # ---------------------------------------------
            # ESTOQUE
            # ---------------------------------------------

            if produto.estoque is None:

                return jsonify({
                    "erro":
                    f"O produto '{produto.nome}' não possui estoque definido."
                }), 400


            if produto.estoque < quantidade:

                return jsonify({
                    "erro":
                    f"Estoque insuficiente para o produto '{produto.nome}'.",
                    "estoque_disponivel": produto.estoque,
                    "quantidade_solicitada": quantidade
                }), 400


            # ---------------------------------------------
            # PREÇO
            # ---------------------------------------------

            preco_unitario = Decimal(
                str(produto.preco_venda)
            )


            subtotal = preco_unitario * quantidade


            # ---------------------------------------------
            # SOMAR AO TOTAL
            # ---------------------------------------------

            total += subtotal


            # ---------------------------------------------
            # BAIXAR ESTOQUE
            # ---------------------------------------------

            produto.estoque -= quantidade


            # ---------------------------------------------
            # GUARDAR ITEM
            # ---------------------------------------------

            itens_processados.append({

                "produto": produto,

                "quantidade": quantidade,

                "preco_unitario": preco_unitario,

                "subtotal": subtotal

            })


        # =================================================
        # CRIAR VENDA
        # =================================================

        venda = Venda(

            cliente_id=cliente_id,

            funcionario_id=funcionario_id,

            total=total,

            status="Concluída"

        )


        db.session.add(venda)

        db.session.flush()


        # =================================================
        # CRIAR ITENS
        # =================================================

        for item in itens_processados:

            item_venda = ItemVenda(

                venda_id=venda.id,

                produto_id=item["produto"].id,

                quantidade=item["quantidade"],

                preco_unitario=item["preco_unitario"],

                subtotal=item["subtotal"]

            )

            db.session.add(item_venda)


        # =================================================
        # SALVAR
        # =================================================

        db.session.commit()


        # =================================================
        # RESPOSTA
        # =================================================

        return jsonify({

            "mensagem":
            "Venda registrada com sucesso.",

            "venda": {

                "id": venda.id,

                "cliente_id": venda.cliente_id,

                "funcionario_id": venda.funcionario_id,

                "total": float(venda.total),

                "status": venda.status

            }

        }), 201


    except SQLAlchemyError:

        db.session.rollback()

        return jsonify({

            "erro":
            "Erro ao registrar venda."

        }), 500


# ========================================================
# LISTAR VENDAS
# ========================================================

@vendas_bp.route("/vendas", methods=["GET"])
@jwt_required()
def listar_vendas():

    # ====================================================
    # FILTROS
    # ====================================================

    status = request.args.get("status")
    cliente_id = request.args.get("cliente_id", type=int)
    funcionario_id = request.args.get("funcionario_id")

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")
    
    
    """status = request.args.get("status")
    cliente_id = request.args.get("cliente_id", type=int)
    funcionario_id = request.args.get("funcionario_id", type=int)"""

    consulta = Venda.query

    # ----------------------------------------------------
    # FILTRO POR STATUS
    # ----------------------------------------------------

    if status:

        status_validos = [
            "Concluída",
            "Cancelada"
        ]

        if status not in status_validos:

            return jsonify({
                "erro": "Status inválido.",
                "status_validos": status_validos
            }), 400

        consulta = consulta.filter(
            Venda.status == status
        )

    # ----------------------------------------------------
    # FILTRO POR CLIENTE
    # ----------------------------------------------------

    if cliente_id is not None:

        consulta = consulta.filter(
            Venda.cliente_id == cliente_id
        )

    # ----------------------------------------------------
    # FILTRO POR FUNCIONÁRIO
    # ----------------------------------------------------

    if funcionario_id is not None:

        consulta = consulta.filter(
            Venda.funcionario_id == funcionario_id
        )


    # ----------------------------------------------------
    # FILTRO POR DATA INICIAL
    # ----------------------------------------------------

    if data_inicio:

        try:
            data_inicio_obj = datetime.strptime(
                data_inicio,
                "%Y-%m-%d"
            )

        except ValueError:
            return jsonify({
                "erro": "Data inicial inválida. Use o formato YYYY-MM-DD."
            }), 400
    
    
    # ----------------------------------------------------
    # FILTRO POR DATA FINAL
    # ----------------------------------------------------

    if data_fim:

        try:
            data_fim_obj = datetime.strptime(
                data_fim,
                "%Y-%m-%d"
            )

        except ValueError:
            return jsonify({
                "erro": "Data final inválida. Use o formato YYYY-MM-DD."
            }), 400
    
    
    if data_inicio and data_fim:

        if data_inicio_obj >= data_fim_obj:
            return jsonify({
                "erro": "A data inicial não pode ser maior ou igual à data final."
            }), 400


    if data_inicio:
        consulta = consulta.filter(
            Venda.data_hora >= data_inicio_obj
        )

    if data_fim:
        data_fim_obj = data_fim_obj + timedelta(days=1)

        consulta = consulta.filter(
            Venda.data_hora < data_fim_obj
    )
    

    # ====================================================
    # BUSCAR VENDAS
    # ====================================================

    vendas = consulta.order_by(
        Venda.id.desc()
    ).all()

    resultado = []

    # ====================================================
    # MONTAR RESPOSTA
    # ====================================================

    for venda in vendas:

        itens = []

        for item in venda.itens:

            itens.append({

                "id": item.id,

                "produto_id":
                item.produto_id,

                "quantidade":
                item.quantidade,

                "preco_unitario":
                float(item.preco_unitario),

                "subtotal":
                float(item.subtotal)

            })

        resultado.append({

            "id":
            venda.id,

            "cliente_id":
            venda.cliente_id,

            "funcionario_id":
            venda.funcionario_id,

            "data_hora":
            venda.data_hora.isoformat(),

            "total":
            float(venda.total),

            "status":
            venda.status,

            "itens":
            itens

        })

    return jsonify(resultado), 200



# ========================================================
# RESUMO DE VENDAS
# ========================================================

@vendas_bp.route("/vendas/resumo", methods=["GET"])
@jwt_required()
def resumo_vendas():

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    consulta = Venda.query

    # ----------------------------------------------------
    # FILTRO POR DATA INICIAL
    # ----------------------------------------------------

    if data_inicio:

        try:
            data_inicio_obj = datetime.strptime(
                data_inicio,
                "%Y-%m-%d"
            )

        except ValueError:

            return jsonify({
                "erro":
                "Data inicial inválida. Use o formato YYYY-MM-DD."
            }), 400

        consulta = consulta.filter(
            Venda.data_hora >= data_inicio_obj
        )

    # ----------------------------------------------------
    # FILTRO POR DATA FINAL
    # ----------------------------------------------------

    if data_fim:

        try:
            data_fim_obj = datetime.strptime(
                data_fim,
                "%Y-%m-%d"
            )

        except ValueError:

            return jsonify({
                "erro":
                "Data final inválida. Use o formato YYYY-MM-DD."
            }), 400

        # Incluir todo o dia informado
        data_fim_obj = data_fim_obj + timedelta(days=1)

        consulta = consulta.filter(
            Venda.data_hora < data_fim_obj
        )

    # ----------------------------------------------------
    # BUSCAR VENDAS
    # ----------------------------------------------------

    vendas = consulta.all()

    # ----------------------------------------------------
    # CALCULAR RESUMO
    # ----------------------------------------------------

    total_vendas = len(vendas)

    vendas_concluidas = sum(
        1
        for venda in vendas
        if venda.status == "Concluída"
    )

    vendas_canceladas = sum(
        1
        for venda in vendas
        if venda.status == "Cancelada"
    )

    valor_total_vendas = sum(
        (
            Decimal(str(venda.total))
            for venda in vendas
        ),
        Decimal("0.00")
    )

    # ----------------------------------------------------
    # RETORNO
    # ----------------------------------------------------

    return jsonify({

        "total_vendas":
        total_vendas,

        "vendas_concluidas":
        vendas_concluidas,

        "vendas_canceladas":
        vendas_canceladas,

        "valor_total_vendas":
        float(valor_total_vendas)

    }), 200



# ========================================================
# RELATÓRIO DE VENDAS
# ========================================================

@vendas_bp.route("/vendas/relatorio", methods=["GET"])
@jwt_required()
def relatorio_vendas():
    """Retorna um relatório financeiro das vendas filtradas por período."""

    # ====================================================
    # FILTROS
    # ====================================================

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    consulta = Venda.query

    # ====================================================
    # VALIDAR DATA INICIAL
    # ====================================================

    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(
                data_inicio,
                "%Y-%m-%d",
            )

        except ValueError:
            return jsonify({
                "erro": (
                    "Data inicial inválida. "
                    "Use o formato YYYY-MM-DD."
                )
            }), 400

    # ====================================================
    # VALIDAR DATA FINAL
    # ====================================================

    if data_fim:
        try:
            data_fim_obj = datetime.strptime(
                data_fim,
                "%Y-%m-%d",
            )

        except ValueError:
            return jsonify({
                "erro": (
                    "Data final inválida. "
                    "Use o formato YYYY-MM-DD."
                )
            }), 400

    # ====================================================
    # VALIDAR INTERVALO
    # ====================================================

    if data_inicio and data_fim:
        if data_inicio_obj > data_fim_obj:
            return jsonify({
                "erro": (
                    "A data inicial não pode ser maior "
                    "que a data final."
                )
            }), 400

    # ====================================================
    # APLICAR DATA INICIAL
    # ====================================================

    if data_inicio:
        consulta = consulta.filter(
            Venda.data_hora >= data_inicio_obj
        )

    # ====================================================
    # APLICAR DATA FINAL
    # ====================================================

    if data_fim:
        data_fim_obj += timedelta(days=1)

        consulta = consulta.filter(
            Venda.data_hora < data_fim_obj
        )

    # ====================================================
    # BUSCAR VENDAS
    # ====================================================

    vendas = consulta.all()

    # ====================================================
    # CONTADORES
    # ====================================================

    total_vendas = len(vendas)

    vendas_concluidas = sum(
        venda.status == "Concluída"
        for venda in vendas
    )

    vendas_canceladas = sum(
        venda.status == "Cancelada"
        for venda in vendas
    )

    # ====================================================
    # VALORES FINANCEIROS
    # ====================================================

    faturamento_bruto = sum(
        (
            Decimal(str(venda.total))
            for venda in vendas
            if venda.status == "Concluída"
        ),
        Decimal("0.00"),
    )

    valor_cancelado = sum(
        (
            Decimal(str(venda.total))
            for venda in vendas
            if venda.status == "Cancelada"
        ),
        Decimal("0.00"),
    )

    # Vendas canceladas não geram faturamento.
    faturamento_liquido = faturamento_bruto

    # ====================================================
    # RETORNO
    # ====================================================

    return jsonify({
        "total_vendas": total_vendas,
        "vendas_concluidas": vendas_concluidas,
        "vendas_canceladas": vendas_canceladas,
        "faturamento_bruto": float(faturamento_bruto),
        "valor_cancelado": float(valor_cancelado),
        "faturamento_liquido": float(faturamento_liquido),
    }), 200







# ========================================================
# RELATÓRIO DE VENDAS POR PRODUTO
# ========================================================

@vendas_bp.route("/vendas/relatorio/produtos", methods=["GET"])
@jwt_required()
def relatorio_vendas_por_produto():

    # ====================================================
    # FILTROS DE DATA
    # ====================================================

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    consulta = Venda.query.filter(
        Venda.status == "Concluída"
    )

    # ====================================================
    # VALIDAR DATA INICIAL
    # ====================================================

    if data_inicio:

        try:
            data_inicio_obj = datetime.strptime(
                data_inicio,
                "%Y-%m-%d"
            )

        except ValueError:

            return jsonify({
                "erro":
                "Data inicial inválida. "
                "Use o formato YYYY-MM-DD."
            }), 400

    # ====================================================
    # VALIDAR DATA FINAL
    # ====================================================

    if data_fim:

        try:
            data_fim_obj = datetime.strptime(
                data_fim,
                "%Y-%m-%d"
            )

        except ValueError:

            return jsonify({
                "erro":
                "Data final inválida. "
                "Use o formato YYYY-MM-DD."
            }), 400

    # ====================================================
    # VALIDAR INTERVALO
    # ====================================================

    if data_inicio and data_fim:

        if data_inicio_obj > data_fim_obj:

            return jsonify({
                "erro":
                "A data inicial não pode ser maior "
                "que a data final."
            }), 400

    # ====================================================
    # APLICAR DATA INICIAL
    # ====================================================

    if data_inicio:

        consulta = consulta.filter(
            Venda.data_hora >= data_inicio_obj
        )

    # ====================================================
    # APLICAR DATA FINAL
    # ====================================================

    if data_fim:

        data_fim_obj += timedelta(days=1)

        consulta = consulta.filter(
            Venda.data_hora < data_fim_obj
        )

    # ====================================================
    # BUSCAR VENDAS CONCLUÍDAS
    # ====================================================

    vendas = consulta.all()

    # ====================================================
    # AGRUPAR PRODUTOS
    # ====================================================

    produtos = {}

    for venda in vendas:

        for item in venda.itens:

            produto_id = item.produto_id

            if produto_id not in produtos:

                produtos[produto_id] = {
                    "produto_id": produto_id,
                    "produto": (
                        item.produto.nome
                        if item.produto
                        else "Produto não encontrado"
                    ),
                    "quantidade_vendida": 0,
                    "faturamento": Decimal("0.00")
                }

            produtos[produto_id]["quantidade_vendida"] += (
                item.quantidade
            )

            produtos[produto_id]["faturamento"] += Decimal(
                str(item.subtotal)
            )

    # ====================================================
    # MONTAR RESULTADO
    # ====================================================

    resultado = []

    for produto in produtos.values():

        resultado.append({

            "produto_id":
            produto["produto_id"],

            "produto":
            produto["produto"],

            "quantidade_vendida":
            produto["quantidade_vendida"],

            "faturamento":
            float(produto["faturamento"])

        })

    # ====================================================
    # ORDENAR POR QUANTIDADE VENDIDA
    # ====================================================

    resultado.sort(
        key=lambda x: x["quantidade_vendida"],
        reverse=True
    )

    # ====================================================
    # RETORNO
    # ====================================================

    return jsonify(resultado), 200






















# ========================================================
# CONSULTAR VENDA POR ID
# ========================================================

@vendas_bp.route("/vendas/<int:id>", methods=["GET"])
@jwt_required()
def consultar_venda(id):

    venda = Venda.query.get(id)

    if venda is None:
        return jsonify({
            "erro": "Venda não encontrada."
        }), 404

    itens = []

    for item in venda.itens:

        itens.append({
            "id": item.id,
            "produto_id": item.produto_id,
            "quantidade": item.quantidade,
            "preco_unitario": float(
                item.preco_unitario
            ),
            "subtotal": float(
                item.subtotal
            )
        })

    return jsonify({

        "id": venda.id,

        "cliente_id": venda.cliente_id,

        "funcionario_id": venda.funcionario_id,

        "data_hora": venda.data_hora.isoformat(),

        "total": float(venda.total),

        "status": venda.status,

        "itens": itens

    }), 200



# ========================================================
# CANCELAR VENDA
# ========================================================

@vendas_bp.route("/vendas/<int:id>/cancelar", methods=["PUT"])
@jwt_required()
def cancelar_venda(id):

    venda = Venda.query.get(id)

    # ----------------------------------------------------
    # VALIDAR VENDA
    # ----------------------------------------------------

    if venda is None:
        return jsonify({
            "erro": "Venda não encontrada."
        }), 404

    # ----------------------------------------------------
    # VERIFICAR SE JÁ ESTÁ CANCELADA
    # ----------------------------------------------------

    if venda.status == "Cancelada":
        return jsonify({
            "erro": "Esta venda já está cancelada."
        }), 400

    try:

        # =================================================
        # DEVOLVER PRODUTOS AO ESTOQUE
        # =================================================

        for item in venda.itens:

            produto = Produto.query.get(item.produto_id)

            if produto is not None:

                if produto.estoque is None:
                    produto.estoque = 0

                produto.estoque += item.quantidade

        # =================================================
        # ALTERAR STATUS
        # =================================================

        venda.status = "Cancelada"

        # =================================================
        # SALVAR
        # =================================================

        db.session.commit()

        # =================================================
        # RESPOSTA
        # =================================================

        return jsonify({

            "mensagem":
            "Venda cancelada com sucesso.",

            "venda": {

                "id": venda.id,

                "cliente_id":
                venda.cliente_id,

                "funcionario_id":
                venda.funcionario_id,

                "data_hora":
                venda.data_hora.isoformat(),

                "total":
                float(venda.total),

                "status":
                venda.status

            }

        }), 200

    except SQLAlchemyError:

        db.session.rollback()

        return jsonify({

            "erro":
            "Erro ao cancelar venda."

        }), 500
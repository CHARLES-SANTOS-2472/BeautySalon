"""Criar tabelas de vendas e itens de venda

Revision ID: accdbf4b8c14
Revises: 81bd1161e167
Create Date: 2026-09-01 14:19:23.103119

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision = "accdbf4b8c14"
down_revision = "81bd1161e167"
branch_labels = None
depends_on = None


def upgrade():

    # ====================================================
    # TABELA DE VENDAS
    # ====================================================

    op.create_table(
        "vendas",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "cliente_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "funcionario_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "data_hora",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "total",
            sa.Numeric(
                precision=10,
                scale=2
            ),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(
                length=30
            ),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"]
        ),

        sa.ForeignKeyConstraint(
            ["funcionario_id"],
            ["funcionarios.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


    # ====================================================
    # TABELA DE ITENS DA VENDA
    # ====================================================

    op.create_table(
        "itens_venda",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "venda_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "produto_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "quantidade",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "preco_unitario",
            sa.Numeric(
                precision=10,
                scale=2
            ),
            nullable=False
        ),

        sa.Column(
            "subtotal",
            sa.Numeric(
                precision=10,
                scale=2
            ),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["produto_id"],
            ["produtos.id"]
        ),

        sa.ForeignKeyConstraint(
            ["venda_id"],
            ["vendas.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )


def downgrade():

    op.drop_table(
        "itens_venda"
    )

    op.drop_table(
        "vendas"
    )
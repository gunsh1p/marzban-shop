"""Create tables

Revision ID: 36159a9e6985
Revises: 
Create Date: 2023-11-19 23:51:25.030165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36159a9e6985'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crypto_payments',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('lang', sa.String(length=64), nullable=True),
    sa.Column('payment_uuid', sa.String(length=64), nullable=True),
    sa.Column('order_id', sa.String(length=64), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.Column('callback', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('vpnusers',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('vpn_id', sa.String(length=64), nullable=True),
    sa.Column('test', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('yookassa_payments',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('lang', sa.String(length=64), nullable=True),
    sa.Column('payment_id', sa.String(length=64), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=True),
    sa.Column('callback', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('yookassa_payments')
    op.drop_table('vpnusers')
    op.drop_table('crypto_payments')
    # ### end Alembic commands ###

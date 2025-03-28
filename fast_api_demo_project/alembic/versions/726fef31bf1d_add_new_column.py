"""Add new column

Revision ID: 726fef31bf1d
Revises: cc84d8cd2e88
Create Date: 2025-02-03 13:55:41.048233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '726fef31bf1d'
down_revision: Union[str, None] = 'cc84d8cd2e88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('flash_sale_price', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('flash_sale_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'flash_sale_active')
    op.drop_column('products', 'flash_sale_price')
    # ### end Alembic commands ###

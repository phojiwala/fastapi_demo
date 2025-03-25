"""first migrations

Revision ID: 193ffe4e273f
Revises: 0ac160570127
Create Date: 2025-01-31 15:38:18.523971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '193ffe4e273f'
down_revision: Union[str, None] = '0ac160570127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

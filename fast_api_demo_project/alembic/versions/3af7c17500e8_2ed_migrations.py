"""2ed migrations

Revision ID: 3af7c17500e8
Revises: 193ffe4e273f
Create Date: 2025-01-31 16:48:49.258222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3af7c17500e8'
down_revision: Union[str, None] = '193ffe4e273f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

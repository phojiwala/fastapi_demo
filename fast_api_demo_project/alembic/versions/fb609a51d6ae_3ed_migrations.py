"""3ed migrations

Revision ID: fb609a51d6ae
Revises: 3af7c17500e8
Create Date: 2025-01-31 16:53:17.421444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb609a51d6ae'
down_revision: Union[str, None] = '3af7c17500e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

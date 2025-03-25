"""4ed migrations

Revision ID: cc84d8cd2e88
Revises: fb609a51d6ae
Create Date: 2025-02-03 13:00:47.467875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc84d8cd2e88'
down_revision: Union[str, None] = 'fb609a51d6ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

"""create account table

Revision ID: 43b193dc9a13
Revises: edfde9b8a874
Create Date: 2025-10-20 15:24:09.076920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43b193dc9a13'
down_revision: Union[str, Sequence[str], None] = 'edfde9b8a874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

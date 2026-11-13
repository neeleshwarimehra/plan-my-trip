"""add updated_at to trips

Revision ID: 9ecfd040c6f9
Revises: 46178e206468
Create Date: 2026-11-14 01:39:44.381036
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9ecfd040c6f9"
down_revision: Union[str, Sequence[str], None] = "46178e206468"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "trips",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("trips", "updated_at")

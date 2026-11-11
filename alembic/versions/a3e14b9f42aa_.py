"""empty message

Revision ID: a3e14b9f42aa
Revises: 
Create Date: 2026-11-05 15:47:56.503844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3e14b9f42aa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tasks",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("title", sa.String(200), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column("completed", sa.Boolean(), nullable=False),)


def downgrade() -> None:
    op.drop_table("tasks")

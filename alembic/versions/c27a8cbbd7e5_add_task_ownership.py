"""add task ownership

Revision ID: c27a8cbbd7e5
Revises: aea5f6aa8bbc
Create Date: 2026-11-08 17:50:03.484876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c27a8cbbd7e5'
down_revision: Union[str, Sequence[str], None] = 'aea5f6aa8bbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key("fk_tasks_user_id_users", 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint("fk_tasks_user_id_users", 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')

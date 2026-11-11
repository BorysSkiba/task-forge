"""add projects

Revision ID: b0277975b276
Revises: c27a8cbbd7e5
Create Date: 2026-11-10 15:57:42.820186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0277975b276'
down_revision: Union[str, Sequence[str], None] = 'c27a8cbbd7e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], 'fk_projects_user_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('tasks', sa.Column('project_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_tasks_project_id_projects', 'tasks', 'projects', ['project_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_tasks_project_id_projects', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'project_id')
    op.drop_table('projects')

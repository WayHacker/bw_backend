"""Edit tasks table/ add work scope and object id

Revision ID: dce66889c188
Revises: 1fe5558f7c8d
Create Date: 2024-07-08 22:15:34.243964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dce66889c188'
down_revision: Union[str, None] = '1fe5558f7c8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('work_scope', sa.Integer(), nullable=False))
    op.add_column('task', sa.Column('done_scope', sa.Integer(), nullable=False))
    op.add_column('task', sa.Column('object_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'task', 'object', ['object_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'object_id')
    op.drop_column('task', 'done_scope')
    op.drop_column('task', 'work_scope')
    # ### end Alembic commands ###

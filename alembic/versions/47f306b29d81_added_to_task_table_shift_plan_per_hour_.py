"""added to task table shift, plan_per_hour, plan_scope_hours

Revision ID: 47f306b29d81
Revises: 3f9410f97e4a
Create Date: 2024-07-22 22:09:35.911212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47f306b29d81'
down_revision: Union[str, None] = '3f9410f97e4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('plan_per_hour', sa.Integer(), nullable=False))
    op.add_column('task', sa.Column('shift', sa.Integer(), nullable=False))
    op.add_column('task', sa.Column('plan_scope_hours', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'plan_scope_hours')
    op.drop_column('task', 'shift')
    op.drop_column('task', 'plan_per_hour')
    # ### end Alembic commands ###

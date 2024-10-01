"""Add in progres to task table

Revision ID: a7a6d2833476
Revises: 0201e0f28da6
Create Date: 2024-10-02 01:17:24.523194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7a6d2833476'
down_revision: Union[str, None] = '0201e0f28da6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('in_progres', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'in_progres')
    # ### end Alembic commands ###

"""Add role to user table

Revision ID: 0201e0f28da6
Revises: 896756a4419d
Create Date: 2024-10-02 00:40:38.101721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0201e0f28da6'
down_revision: Union[str, None] = '896756a4419d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    # ### end Alembic commands ###

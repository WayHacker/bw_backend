"""Added material table

Revision ID: 273271c023b3
Revises: e8286202e52b
Create Date: 2024-06-17 22:07:17.104892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '273271c023b3'
down_revision: Union[str, None] = 'e8286202e52b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material',
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('reciept', sa.LargeBinary(), nullable=False),
    sa.Column('supply', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('material')
    # ### end Alembic commands ###

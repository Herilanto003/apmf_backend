"""empty message

Revision ID: cb74bcb00a6d
Revises: 231a11599b3d
Create Date: 2023-10-10 11:57:39.964638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb74bcb00a6d'
down_revision: Union[str, None] = '231a11599b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('marchandises', 'caractere',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('marchandises', 'conditionnement',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('marchandises', 'conditionnement',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('marchandises', 'caractere',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###

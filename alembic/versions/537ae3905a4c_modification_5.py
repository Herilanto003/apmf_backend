"""modification 5

Revision ID: 537ae3905a4c
Revises: 3be51a3038cc
Create Date: 2023-10-09 21:13:58.467199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '537ae3905a4c'
down_revision: Union[str, None] = '3be51a3038cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accostage', sa.Column('date_enreg', sa.Date(), nullable=False))
    op.add_column('accostage', sa.Column('date_heure_arrive', sa.DateTime(), nullable=False))
    op.add_column('accostage', sa.Column('date_heure_depart', sa.DateTime(), nullable=False))
    op.drop_column('accostage', 'date_accoste')
    op.drop_column('navires', 'date_heure_depart')
    op.drop_column('navires', 'date_heure_arrive')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('navires', sa.Column('date_heure_arrive', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('navires', sa.Column('date_heure_depart', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('accostage', sa.Column('date_accoste', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('accostage', 'date_heure_depart')
    op.drop_column('accostage', 'date_heure_arrive')
    op.drop_column('accostage', 'date_enreg')
    # ### end Alembic commands ###

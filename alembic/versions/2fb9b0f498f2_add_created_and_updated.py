"""add created and updated

Revision ID: 2fb9b0f498f2
Revises: dd35c2c299df
Create Date: 2023-10-08 05:25:34.092028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fb9b0f498f2'
down_revision: Union[str, None] = 'dd35c2c299df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accostage', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('accostage', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('actionaire', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('actionaire', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('continents', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('continents', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('marchandises', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('marchandises', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('navires', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('navires', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('operation', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('operation', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('pays', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('pays', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('ports', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('ports', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('responsable_navire', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('responsable_navire', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('responsable_navire', 'updated_at')
    op.drop_column('responsable_navire', 'created_at')
    op.drop_column('ports', 'updated_at')
    op.drop_column('ports', 'created_at')
    op.drop_column('pays', 'updated_at')
    op.drop_column('pays', 'created_at')
    op.drop_column('operation', 'updated_at')
    op.drop_column('operation', 'created_at')
    op.drop_column('navires', 'updated_at')
    op.drop_column('navires', 'created_at')
    op.drop_column('marchandises', 'updated_at')
    op.drop_column('marchandises', 'created_at')
    op.drop_column('continents', 'updated_at')
    op.drop_column('continents', 'created_at')
    op.drop_column('actionaire', 'updated_at')
    op.drop_column('actionaire', 'created_at')
    op.drop_column('accostage', 'updated_at')
    op.drop_column('accostage', 'created_at')
    # ### end Alembic commands ###

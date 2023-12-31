"""last change

Revision ID: 4141118504e4
Revises: d908d9f086bf
Create Date: 2023-10-28 10:05:31.123008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4141118504e4'
down_revision: Union[str, None] = 'd908d9f086bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actionaire', sa.Column('tel_act', sa.String(), nullable=True))
    op.add_column('actionaire', sa.Column('email_act', sa.String(), nullable=True))
    op.drop_column('actionaire', 'adresse_email_act')
    op.drop_column('actionaire', 'cin_act')
    op.drop_column('actionaire', 'localisation_ent_act')
    op.drop_column('actionaire', 'nom_ent_act')
    op.drop_column('actionaire', 'prenoms_act')
    op.drop_column('actionaire', 'contact_act')
    op.drop_column('actionaire', 'email_ent_act')
    op.add_column('responsable_navire', sa.Column('tel_resp', sa.String(), nullable=False))
    op.add_column('responsable_navire', sa.Column('email_resp', sa.String(), nullable=False))
    op.drop_column('responsable_navire', 'contact_resp')
    op.drop_column('responsable_navire', 'nom_ent_resp')
    op.drop_column('responsable_navire', 'adresse_email_resp')
    op.drop_column('responsable_navire', 'email_ent_resp')
    op.drop_column('responsable_navire', 'adresse')
    op.drop_column('responsable_navire', 'prenoms_resp')
    op.drop_column('responsable_navire', 'cin_resp')
    op.drop_column('responsable_navire', 'localisation_ent_resp')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('responsable_navire', sa.Column('localisation_ent_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('cin_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('prenoms_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('adresse', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('email_ent_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('adresse_email_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('nom_ent_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('responsable_navire', sa.Column('contact_resp', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('responsable_navire', 'email_resp')
    op.drop_column('responsable_navire', 'tel_resp')
    op.add_column('actionaire', sa.Column('email_ent_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('contact_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('prenoms_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('nom_ent_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('localisation_ent_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('cin_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('actionaire', sa.Column('adresse_email_act', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('actionaire', 'email_act')
    op.drop_column('actionaire', 'tel_act')
    # ### end Alembic commands ###

"""insert_user

Revision ID: f553ec83a9ad
Revises: 19a6ff2d1aa5
Create Date: 2023-11-07 20:42:51.804984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.orm as orm
from config.connexion_db import get_db
from config.models import Utilisateur
from config.auth.utilis import get_password_hash


# revision identifiers, used by Alembic.
revision: str = 'f553ec83a9ad'
down_revision: Union[str, None] = '19a6ff2d1aa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    db = orm.Session(bind=connection)
    admin = Utilisateur(
        nom = 'admin',
        prenoms = 'admin',
        role = 'ADMIN',
        email = 'admin@apmf.mg',
        password = get_password_hash('admin'),
        code_activation = 'admin',
        status_compte = True
    )
    db.add(admin)
    db.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

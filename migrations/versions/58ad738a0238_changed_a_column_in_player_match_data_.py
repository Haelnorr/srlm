"""changed a column in player_match_data to match slap api

Revision ID: 58ad738a0238
Revises: 85cc919b2356
Create Date: 2024-04-03 11:32:03.222696

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '58ad738a0238'
down_revision = '85cc919b2356'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('possession_time_sec', sa.Integer(), nullable=True))
        batch_op.drop_column('possession_time')

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player_match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('possession_time', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('possession_time_sec')

    # ### end Alembic commands ###


def upgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


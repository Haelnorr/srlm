"""added num_players to matchtype

Revision ID: 11f045f72507
Revises: 58ad738a0238
Create Date: 2024-04-04 21:10:16.034642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f045f72507'
down_revision = '58ad738a0238'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matchtype', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num_players', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matchtype', schema=None) as batch_op:
        batch_op.drop_column('num_players')

    # ### end Alembic commands ###


def upgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


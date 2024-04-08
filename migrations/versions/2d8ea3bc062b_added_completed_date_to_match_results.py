"""added completed_date to match_results

Revision ID: 2d8ea3bc062b
Revises: eacbca084e9a
Create Date: 2024-04-01 00:21:05.182242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d8ea3bc062b'
down_revision = 'eacbca084e9a'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_result', schema=None) as batch_op:
        batch_op.drop_column('completed_date')

    # ### end Alembic commands ###


def upgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


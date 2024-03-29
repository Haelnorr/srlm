"""added links from league.server_region to server_region table

Revision ID: b9ccb8cf35b8
Revises: 4eacde8fd444
Create Date: 2024-03-29 12:00:28.380087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ccb8cf35b8'
down_revision = '4eacde8fd444'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('league', schema=None) as batch_op:
        batch_op.add_column(sa.Column('server_region_value', sa.String(length=32), nullable=True))
        batch_op.create_foreign_key(None, 'server_region', ['server_region_value'], ['value'])

    with op.batch_alter_table('server_region', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utc_offset', sa.String(length=7), nullable=True))

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('server_region', schema=None) as batch_op:
        batch_op.drop_column('utc_offset')

    with op.batch_alter_table('league', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('server_region_value')

    # ### end Alembic commands ###


def upgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_api_access():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

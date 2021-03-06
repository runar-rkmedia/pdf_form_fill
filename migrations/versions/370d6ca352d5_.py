"""empty message

Revision ID: 370d6ca352d5
Revises: 2368ae874fda
Create Date: 2017-08-10 20:04:45.383542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '370d6ca352d5'
down_revision = '2368ae874fda'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'room_item_modifications', ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'room_item_modifications', type_='unique')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


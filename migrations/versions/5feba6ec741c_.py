"""empty message

Revision ID: 5feba6ec741c
Revises: 0d00fa813645
Create Date: 2017-09-03 12:07:43.107797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5feba6ec741c'
down_revision = '0d00fa813645'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vk_users', sa.Column('last_modified_customer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'vk_users', 'customer', ['last_modified_customer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vk_users', type_='foreignkey')
    op.drop_column('vk_users', 'last_modified_customer_id')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


"""empty message

Revision ID: 0f7006aa4743
Revises: c16ed716af74
Create Date: 2017-10-10 19:42:56.278429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f7006aa4743'
down_revision = 'c16ed716af74'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_data', sa.Column('mobile', sa.String(length=20), nullable=True))
    op.add_column('customer_data', sa.Column('phone', sa.String(length=20), nullable=True))
    op.drop_column('customer_data', 'contact_phone')
    op.drop_column('customer_data', 'contact_mobile')
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer_data', sa.Column('contact_mobile', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('customer_data', sa.Column('contact_phone', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.drop_column('customer_data', 'phone')
    op.drop_column('customer_data', 'mobile')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


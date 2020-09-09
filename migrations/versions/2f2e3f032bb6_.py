"""empty message

Revision ID: 2f2e3f032bb6
Revises: a5bf6f438b26
Create Date: 2017-10-16 08:18:08.976047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2f2e3f032bb6'
down_revision = 'a5bf6f438b26'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_type', sa.Column('inside', sa.Boolean(), nullable=True))
    op.add_column('product_type', sa.Column('isMat', sa.Boolean(), nullable=True))
    op.add_column('product_type', sa.Column('outside', sa.Boolean(), nullable=True))
    op.drop_column('product_type', 'catagory')
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_type', sa.Column('catagory', postgresql.ENUM('cable_inside', 'cable_outside', 'mat_inside', 'mat_outside', 'single_inside', 'single_outside', name='productcatagory'), autoincrement=False, nullable=True))
    op.drop_column('product_type', 'outside')
    op.drop_column('product_type', 'isMat')
    op.drop_column('product_type', 'inside')
    # ### end Alembic commands ###

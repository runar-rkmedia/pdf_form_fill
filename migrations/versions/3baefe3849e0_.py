"""empty message

Revision ID: 3baefe3849e0
Revises: ceffe0cedd90
Create Date: 2017-08-31 19:31:20.263882

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3baefe3849e0'
down_revision = 'ceffe0cedd90'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('archived', sa.Boolean(), nullable=True))
    op.add_column('company', sa.Column('archived', sa.Boolean(), nullable=True))
    op.add_column('customer', sa.Column('archived', sa.Boolean(), nullable=True))
    op.drop_constraint('room_room_type_info_id_fkey', 'room', type_='foreignkey')
    op.drop_column('room', 'room_type_info_id')
    op.add_column('room_item', sa.Column('archived', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room_item', 'archived')
    op.add_column('room', sa.Column('room_type_info_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('room_room_type_info_id_fkey', 'room', 'room_type_info', ['room_type_info_id'], ['id'])
    op.drop_column('customer', 'archived')
    op.drop_column('company', 'archived')
    op.drop_column('address', 'archived')
    # ### end Alembic commands ###


def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

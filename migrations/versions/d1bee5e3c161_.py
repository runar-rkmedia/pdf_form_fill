"""empty message

Revision ID: d1bee5e3c161
Revises: 51553242fff0
Create Date: 2017-08-10 17:56:07.256769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1bee5e3c161'
down_revision = '51553242fff0'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_():
    op.rename_table('filled_form_modified', 'room_item')
    op.execute('ALTER SEQUENCE filled_form_modified_id_seq RENAME TO room_item_id_seq')
    op.execute('ALTER INDEX filled_form_modified_pkey RENAME TO room_item_pkey')

def downgrade_():
    op.rename_table('room_item', 'filled_form_modified')
    op.execute('ALTER SEQUENCE room_item_id_seq RENAME TO filled_form_modified_id_seq')
    op.execute('ALTER INDEX room_item_pkey RENAME TO filled_form_modified_pkey')



def upgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_products():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

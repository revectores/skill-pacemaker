"""empty message

Revision ID: eec6fc81c554
Revises: 13c2aed05d88
Create Date: 2020-03-10 22:19:00.784932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec6fc81c554'
down_revision = '13c2aed05d88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('node_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_record_node_id'), 'record', ['node_id'], unique=False)
    op.create_foreign_key(None, 'record', 'node', ['node_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'record', type_='foreignkey')
    op.drop_index(op.f('ix_record_node_id'), table_name='record')
    op.drop_column('record', 'node_id')
    # ### end Alembic commands ###

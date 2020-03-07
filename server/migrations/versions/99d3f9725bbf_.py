"""empty message

Revision ID: 99d3f9725bbf
Revises: e4ffd34a5d40
Create Date: 2020-03-07 12:24:27.163436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d3f9725bbf'
down_revision = 'e4ffd34a5d40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('avatar_name', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('avatar_name', 'user', ['avatar_name'], unique=True)
    # ### end Alembic commands ###

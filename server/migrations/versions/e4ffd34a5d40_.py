"""empty message

Revision ID: e4ffd34a5d40
Revises: 0ce544e0d3fd
Create Date: 2020-03-07 11:54:12.379838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4ffd34a5d40'
down_revision = '0ce544e0d3fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('auth', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('avatar_name', sa.String(length=255), nullable=True),
    sa.Column('io', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('avatar_name')
    )
    op.create_index(op.f('ix_user_auth'), 'user', ['auth'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_auth'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
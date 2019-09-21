"""fifth Migration

Revision ID: 42fc9ed256ff
Revises: 5dada5862dcc
Create Date: 2019-09-21 12:33:03.486393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42fc9ed256ff'
down_revision = '5dada5862dcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'votes', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.drop_column('votes', 'user_id')
    # ### end Alembic commands ###

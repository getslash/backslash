"""empty message

Revision ID: 1cf822ad388
Revises: 2aeb533be9a
Create Date: 2015-08-11 23:18:18.325373

"""

# revision identifiers, used by Alembic.
revision = '1cf822ad388'
down_revision = '2aeb533be9a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('deleted', sa.Boolean(), server_default='false', nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'deleted')
    ### end Alembic commands ###
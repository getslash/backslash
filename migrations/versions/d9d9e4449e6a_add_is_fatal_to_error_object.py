"""Add is_fatal to error object

Revision ID: d9d9e4449e6a
Revises: dafc141fefb9
Create Date: 2019-05-29 10:35:48.698561

"""

# revision identifiers, used by Alembic.
revision = 'd9d9e4449e6a'
down_revision = 'dafc141fefb9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('error', sa.Column('is_fatal', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('error', 'is_fatal')
    # ### end Alembic commands ###

"""Add subject indexing

Revision ID: e265d0623907
Revises: f8abde08cbc6
Create Date: 2016-04-07 16:43:33.390866

"""

# revision identifiers, used by Alembic.
revision = 'e265d0623907'
down_revision = 'f8abde08cbc6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_session_subject_session_id', 'session_subject', ['session_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_session_subject_session_id', table_name='session_subject')
    ### end Alembic commands ###

"""empty message

Revision ID: 41f8ccc363a0
Revises: 36b001176e75
Create Date: 2015-05-06 15:02:15.761004

"""

# revision identifiers, used by Alembic.
revision = '41f8ccc363a0'
down_revision = '36b001176e75'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('test', sa.Column('edited_status', sa.String(length=256), nullable=True))
    op.create_index(op.f('ix_test_edited_status'), 'test', ['edited_status'], unique=False)
    op.add_column('session', sa.Column('edited_status', sa.String(length=256), nullable=True))
    op.create_index(op.f('ix_session_edited_status'), 'session', ['edited_status'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_test_edited_status'), table_name='test')
    op.drop_column('test', 'edited_status')
    op.drop_index(op.f('ix_session_edited_status'), table_name='session')
    op.drop_column('session', 'edited_status')

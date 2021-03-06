"""labels

Revision ID: 9306b5950ba7
Revises: c9b38de7bf68
Create Date: 2016-11-22 11:40:25.221046

"""

# revision identifiers, used by Alembic.
revision = '9306b5950ba7'
down_revision = 'c9b38de7bf68'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_label_name'), 'label', ['name'], unique=True)
    op.create_table('session_label',
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('label_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['label_id'], ['label.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ondelete='CASCADE')
    )
    op.create_index('ix_session_label_session_id', 'session_label', ['session_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_session_label_session_id', table_name='session_label')
    op.drop_table('session_label')
    op.drop_index(op.f('ix_label_name'), table_name='label')
    op.drop_table('label')
    ### end Alembic commands ###

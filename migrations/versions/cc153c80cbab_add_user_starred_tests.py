"""add_user_starred_tests

Revision ID: cc153c80cbab
Revises: faf0174f2569
Create Date: 2018-04-16 12:36:21.537710

"""

# revision identifiers, used by Alembic.
revision = 'cc153c80cbab'
down_revision = 'faf0174f2569'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_starred_tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('test_id', sa.Integer(), nullable=True),
    sa.Column('star_creation_time', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['test.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_starred_tests_user_id_test_id', 'user_starred_tests', ['user_id', 'test_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_starred_tests_user_id_test_id', table_name='user_starred_tests')
    op.drop_table('user_starred_tests')
    # ### end Alembic commands ###
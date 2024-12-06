"""empty message

Revision ID: 0ce368a896a3
Revises: 72e8dd479f25
Create Date: 2024-12-06 10:30:40.818222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ce368a896a3'
down_revision = '72e8dd479f25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    # ### end Alembic commands ###

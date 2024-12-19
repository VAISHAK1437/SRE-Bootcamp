"""Initial migration

Revision ID: 2432a4ef923d
Revises: 
Create Date: 2024-12-19 13:11:13.192099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2432a4ef923d'
down_revision = None
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
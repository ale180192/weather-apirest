"""init3

Revision ID: 819f0ade7a63
Revises: 8844132516e2
Create Date: 2022-08-02 22:39:55.475177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '819f0ade7a63'
down_revision = '8844132516e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('lon', sa.String(), nullable=True))
    op.drop_column('cities', 'log')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('log', sa.VARCHAR(), nullable=True))
    op.drop_column('cities', 'lon')
    # ### end Alembic commands ###
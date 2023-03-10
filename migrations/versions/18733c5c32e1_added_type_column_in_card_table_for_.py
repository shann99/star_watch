"""added type column in card table for show, movie, etc.

Revision ID: 18733c5c32e1
Revises: 63ee43ef8ecd
Create Date: 2023-03-03 17:35:28.559179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18733c5c32e1'
down_revision = '63ee43ef8ecd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
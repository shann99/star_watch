"""added release_information column

Revision ID: 5983bb4dfef4
Revises: 38d935d15ef1
Create Date: 2023-03-31 17:31:44.466835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5983bb4dfef4'
down_revision = '38d935d15ef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('release_information', sa.String(length=10000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('release_information')

    # ### end Alembic commands ###

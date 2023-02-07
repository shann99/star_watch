"""Initial migration.

Revision ID: ff4dafa4610f
Revises: c4eed9e917e9
Create Date: 2023-02-06 15:56:00.914812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff4dafa4610f'
down_revision = 'c4eed9e917e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('mode',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('mode',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###

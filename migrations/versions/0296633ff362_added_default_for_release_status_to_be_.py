"""added default for release_status to be released

Revision ID: 0296633ff362
Revises: c6361d5b9171
Create Date: 2023-03-30 17:49:14.928214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0296633ff362'
down_revision = 'c6361d5b9171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_card')
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('release_status',
               existing_type=sa.VARCHAR(length=10000),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('release_status',
               existing_type=sa.VARCHAR(length=10000),
               nullable=True)

    op.create_table('_alembic_tmp_card',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('image', sa.VARCHAR(length=10000000), server_default=sa.text("'/background.jpg'"), nullable=False),
    sa.Column('current_ep', sa.INTEGER(), nullable=False),
    sa.Column('total_eps', sa.VARCHAR(length=1000), server_default=sa.text("'0'"), nullable=False),
    sa.Column('description', sa.VARCHAR(length=10000), nullable=True),
    sa.Column('rating', sa.INTEGER(), nullable=True),
    sa.Column('date_added', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('status', sa.VARCHAR(length=1000), server_default=sa.text("'Planning'"), nullable=False),
    sa.Column('fav', sa.BOOLEAN(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('date_edited', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('language', sa.VARCHAR(length=1000), server_default=sa.text("'Unknown'"), nullable=False),
    sa.Column('media_type', sa.VARCHAR(length=1000), server_default=sa.text("'Unknown'"), nullable=False),
    sa.Column('release_status', sa.VARCHAR(length=10000), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

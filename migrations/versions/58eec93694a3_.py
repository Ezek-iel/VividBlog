"""empty message

Revision ID: 58eec93694a3
Revises: 3b3e6bb9ad98
Create Date: 2024-04-21 20:15:27.376152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58eec93694a3'
down_revision = '3b3e6bb9ad98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ingredients', sa.Text(), nullable=False))
        batch_op.drop_column('recipesInvolved')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_address', sa.String(length=70), nullable=False))
        batch_op.drop_column('emailaddress')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('emailaddress', sa.VARCHAR(length=70), nullable=False))
        batch_op.drop_column('email_address')

    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipesInvolved', sa.TEXT(), nullable=False))
        batch_op.drop_column('ingredients')

    # ### end Alembic commands ###

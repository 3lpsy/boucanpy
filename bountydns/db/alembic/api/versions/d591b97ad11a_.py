"""empty message

Revision ID: d591b97ad11a
Revises: 04c1c884cf2e
Create Date: 2019-05-18 00:42:35.275010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd591b97ad11a'
down_revision = '04c1c884cf2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('api_tokens', 'dns_server_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('dns_requests', 'dns_server_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dns_requests', 'dns_server_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('api_tokens', 'dns_server_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
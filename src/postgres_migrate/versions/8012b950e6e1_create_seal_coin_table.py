"""create seal_coin table

Revision ID: 8012b950e6e1
Revises: 
Create Date: 2021-06-27 02:13:14.735932

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8012b950e6e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "SealCoin",
        sa.Column("audience", sa.String, primary_key=True),
        sa.Column("coin", sa.Integer)
    )


def downgrade():
    op.drop_table('SealCoin')
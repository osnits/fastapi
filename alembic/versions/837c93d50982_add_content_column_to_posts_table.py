"""add content column to posts table

Revision ID: 837c93d50982
Revises: a6bf7c4d4f69
Create Date: 2025-07-14 17:14:43.853648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '837c93d50982'
down_revision = 'a6bf7c4d4f69'
branch_labels = None
depends_on = None 


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass

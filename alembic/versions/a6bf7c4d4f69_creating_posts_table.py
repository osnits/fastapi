"""creating posts table

Revision ID: a6bf7c4d4f69
Revises: 
Create Date: 2025-07-14 16:30:03.835518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6bf7c4d4f69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    #how to undo the creating of table that we coded above in the upgrade()
    op.drop_table("posts")

    pass

"""add foreign key to posts table

Revision ID: a209281411c1
Revises: 59f21c20b226
Create Date: 2025-07-14 17:31:57.073018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a209281411c1'
down_revision = '59f21c20b226'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", 
                          referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass

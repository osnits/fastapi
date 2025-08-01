"""add user table

Revision ID: 59f21c20b226
Revises: 837c93d50982
Create Date: 2025-07-14 17:21:28.429437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f21c20b226'
down_revision = '837c93d50982'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False), 
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email") 
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass

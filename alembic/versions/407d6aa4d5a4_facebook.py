"""facebook

Revision ID: 407d6aa4d5a4
Revises: 
Create Date: 2023-10-10 16:36:13.617518

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "407d6aa4d5a4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facebook_post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("page_name", sa.String(), nullable=False),
        sa.Column("post_id", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id"),
    )
    op.create_table(
        "facebook_comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("comment_id", sa.String(), nullable=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["post_id"], ["facebook_post.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "post_id"),
        sa.UniqueConstraint("content"),
    )


def downgrade() -> None:
    op.drop_table("facebook_comment")
    op.drop_table("facebook_post")

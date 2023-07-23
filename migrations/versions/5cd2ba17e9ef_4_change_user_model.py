"""4_change_user_model

Revision ID: 5cd2ba17e9ef
Revises: c11b8cbe7510
Create Date: 2023-07-22 13:22:48.748865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5cd2ba17e9ef"
down_revision = "c11b8cbe7510"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "hashed_password", existing_type=sa.VARCHAR(length=1024), nullable=True
    )
    op.drop_index("ix_user_email", table_name="user")
    op.drop_column("user", "is_superuser")
    op.drop_column("user", "is_verified")
    op.drop_column("user", "is_active")
    op.drop_column("user", "email")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("email", sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user",
        sa.Column("is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user",
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=False)
    op.alter_column(
        "user", "hashed_password", existing_type=sa.VARCHAR(length=1024), nullable=False
    )
    # ### end Alembic commands ###

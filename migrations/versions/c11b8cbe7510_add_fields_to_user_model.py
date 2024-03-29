"""Add fields to User model

Revision ID: c11b8cbe7510
Revises: 0fbb92e18986
Create Date: 2023-07-19 00:13:11.127401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c11b8cbe7510"
down_revision = "0fbb92e18986"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("first_name", sa.String(length=30), nullable=False))
    op.add_column("user", sa.Column("last_name", sa.String(length=50), nullable=False))
    op.add_column(
        "user", sa.Column("phone_number", sa.String(length=11), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "phone_number")
    op.drop_column("user", "last_name")
    op.drop_column("user", "first_name")
    # ### end Alembic commands ###

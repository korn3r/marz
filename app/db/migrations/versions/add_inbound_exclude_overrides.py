"""add inbound exclude overrides

Revision ID: inbound_exclude_overrides
Revises: 2b231de97dc3
Create Date: 2026-08-11
"""

from alembic import op
import sqlalchemy as sa


revision = "inbound_exclude_overrides"
down_revision = "2b231de97dc3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "inbound_exclude_overrides",
        sa.Column(
            "proxy_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "inbound_tag",
            sa.String(length=256),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "proxy_id",
            "inbound_tag",
        ),
    )


def downgrade():
    op.drop_table("inbound_exclude_overrides")

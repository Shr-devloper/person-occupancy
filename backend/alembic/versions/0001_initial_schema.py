"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-17
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    role_enum = sa.Enum("admin", "manager", "viewer", name="userrole")
    camera_status_enum = sa.Enum("online", "offline", "maintenance", name="camerastatus")
    occupancy_state_enum = sa.Enum("occupied", "empty", name="occupancystate")

    role_enum.create(op.get_bind(), checkfirst=True)
    camera_status_enum.create(op.get_bind(), checkfirst=True)
    occupancy_state_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role", role_enum, nullable=False, server_default="viewer"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "cameras",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("camera_name", sa.String(length=120), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("ip_address", sa.String(length=255), nullable=True),
        sa.Column("stream_url", sa.String(length=512), nullable=True),
        sa.Column("status", camera_status_enum, nullable=False, server_default="offline"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "seats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("seat_name", sa.String(length=120), nullable=False),
        sa.Column("camera_id", sa.Integer(), sa.ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False),
        sa.Column("region_x1", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("region_y1", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("region_x2", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("region_y2", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("current_state", occupancy_state_enum, nullable=False, server_default="empty"),
        sa.Column("last_state_change", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "occupancy_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("seat_id", sa.Integer(), sa.ForeignKey("seats.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("duration", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="info"),
        sa.Column("seat_id", sa.Integer(), sa.ForeignKey("seats.id", ondelete="SET NULL"), nullable=True),
        sa.Column("camera_id", sa.Integer(), sa.ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "device_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False, unique=True),
        sa.Column("platform", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("device_tokens")
    op.drop_table("notifications")
    op.drop_table("occupancy_logs")
    op.drop_table("seats")
    op.drop_table("cameras")
    op.drop_table("users")
    sa.Enum(name="occupancystate").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="camerastatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)

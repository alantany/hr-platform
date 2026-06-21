"""enhancement modules"""

from alembic import op
import sqlalchemy as sa

revision = "0003_enhancement_modules"
down_revision = "0002_support_modules"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "system_configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("value", sa.Text(), nullable=False, server_default=""),
        sa.Column("description", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "email_configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("host", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("port", sa.Integer(), nullable=False, server_default="25"),
        sa.Column("sender", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("username", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("password", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("use_tls", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "ai_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_type", sa.String(length=64), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("output_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="完成"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("ai_tasks")
    op.drop_table("email_configs")
    op.drop_table("system_configs")

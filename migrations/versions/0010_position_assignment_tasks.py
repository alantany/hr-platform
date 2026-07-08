"""add position assignment confirmation tasks"""

from alembic import op
import sqlalchemy as sa


revision = "0010_position_tasks"
down_revision = "4c437f655beb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "position_assignment_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.Column("assignee_user_id", sa.Integer(), nullable=False),
        sa.Column("assigned_by_user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("response_note", sa.Text(), nullable=False, server_default=""),
        sa.Column("responded_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("position_id", "assignee_user_id", name="uq_position_assignment_task"),
    )
    op.create_index("ix_position_assignment_tasks_position_id", "position_assignment_tasks", ["position_id"])
    op.create_index("ix_position_assignment_tasks_assignee_user_id", "position_assignment_tasks", ["assignee_user_id"])
    op.create_index("ix_position_assignment_tasks_assigned_by_user_id", "position_assignment_tasks", ["assigned_by_user_id"])
    op.create_index("ix_position_assignment_tasks_status", "position_assignment_tasks", ["status"])


def downgrade() -> None:
    op.drop_index("ix_position_assignment_tasks_status", table_name="position_assignment_tasks")
    op.drop_index("ix_position_assignment_tasks_assigned_by_user_id", table_name="position_assignment_tasks")
    op.drop_index("ix_position_assignment_tasks_assignee_user_id", table_name="position_assignment_tasks")
    op.drop_index("ix_position_assignment_tasks_position_id", table_name="position_assignment_tasks")
    op.drop_table("position_assignment_tasks")

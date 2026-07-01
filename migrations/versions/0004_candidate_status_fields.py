"""add delivery_status and warranty_status to candidates"""

from alembic import op
import sqlalchemy as sa

revision = "0004_candidate_status_fields"
down_revision = "99731a6b4d23"
branch_labels = None
depends_on = None


def upgrade():
    # 1. 新增 delivery_status 字段（冗余推荐流程状态）
    op.add_column(
        "candidates",
        sa.Column(
            "delivery_status",
            sa.String(length=32),
            nullable=False,
            server_default="未推荐",
        ),
    )
    # 2. 新增 candidate_warranty_status 字段（冗余质保状态）
    op.add_column(
        "candidates",
        sa.Column(
            "candidate_warranty_status",
            sa.String(length=32),
            nullable=False,
            server_default="",
        ),
    )


def downgrade():
    op.drop_column("candidates", "delivery_status")
    op.drop_column("candidates", "candidate_warranty_status")

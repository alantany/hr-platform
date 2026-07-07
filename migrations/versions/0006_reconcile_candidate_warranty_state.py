"""reconcile candidate warranty state from employment records

Revision ID: 0006_warranty_state
Revises: 0005_candidate_state
"""

from datetime import datetime, timedelta, timezone

from alembic import op
import sqlalchemy as sa


revision = "0006_warranty_state"
down_revision = "0005_candidate_state"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    candidates = sa.Table("candidates", metadata, autoload_with=bind)
    employment_records = sa.Table("employment_records", metadata, autoload_with=bind)
    warranty_rules = sa.Table("warranty_rules", metadata, autoload_with=bind)

    months = bind.execute(
        sa.select(warranty_rules.c.months).where(warranty_rules.c.scope == "入职质保期").limit(1)
    ).scalar_one_or_none()
    warranty_days = max(int(months or 2), 0) * 30
    now = datetime.now(timezone.utc)

    candidate_ids = bind.execute(sa.select(candidates.c.id)).scalars().all()
    for candidate_id in candidate_ids:
        record = bind.execute(
            sa.select(employment_records.c.status, employment_records.c.onboard_date)
            .where(employment_records.c.candidate_id == candidate_id)
            .order_by(employment_records.c.created_at.desc(), employment_records.c.id.desc())
            .limit(1)
        ).first()
        status = ""
        if record and record.status == "已入职" and record.onboard_date:
            onboard = record.onboard_date
            if onboard.tzinfo is None:
                onboard = onboard.replace(tzinfo=timezone.utc)
            status = "质保到期" if now > onboard + timedelta(days=warranty_days) else "质保中"
        bind.execute(
            candidates.update()
            .where(candidates.c.id == candidate_id)
            .values(candidate_warranty_status=status)
        )


def downgrade() -> None:
    # 数据修复不可逆；字段结构未变化。
    pass

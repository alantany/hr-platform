"""normalize recommendation and employment statuses

Revision ID: 0007_status_cleanup
Revises: 0006_warranty_state
"""

from datetime import datetime, timedelta, timezone

from alembic import op
import sqlalchemy as sa


revision = "0007_status_cleanup"
down_revision = "0006_warranty_state"
branch_labels = None
depends_on = None


ACTIVE_STATUS_MAP = {
    "已推荐": "已推荐",
    "客户已收": "已推荐",
    "客户未收": "已推荐",
    "安排面试": "面试中",
    "面试中": "面试中",
    "拒绝": "未录用",
    "淘汰": "未录用",
    "未录用": "未录用",
    "已入职": "已入职",
}


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    candidates = sa.Table("candidates", metadata, autoload_with=bind)
    recommendations = sa.Table("recommendations", metadata, autoload_with=bind)
    employment_records = sa.Table("employment_records", metadata, autoload_with=bind)
    followups = sa.Table("candidate_follow_up_records", metadata, autoload_with=bind)
    warranty_rules = sa.Table("warranty_rules", metadata, autoload_with=bind)

    bind.execute(
        warranty_rules.update()
        .where(warranty_rules.c.scope == "入职质保期")
        .values(months=6)
    )

    bind.execute(recommendations.update().where(recommendations.c.status == "待推荐").values(status="已推荐"))
    bind.execute(followups.update().where(followups.c.status == "已录用").values(status="已入职"))

    old_hired = bind.execute(
        sa.select(recommendations.c.id, recommendations.c.candidate_id).where(recommendations.c.status == "已录用")
    ).all()
    for recommendation_id, candidate_id in old_hired:
        employment = bind.execute(
            sa.select(employment_records.c.status)
            .where(employment_records.c.candidate_id == candidate_id)
            .order_by(employment_records.c.created_at.desc(), employment_records.c.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        normalized = "已入职" if employment == "已入职" else "面试中"
        bind.execute(recommendations.update().where(recommendations.c.id == recommendation_id).values(status=normalized))

    candidate_ids = bind.execute(sa.select(candidates.c.id)).scalars().all()
    for candidate_id in candidate_ids:
        employment = bind.execute(
            sa.select(employment_records.c.status)
            .where(employment_records.c.candidate_id == candidate_id)
            .order_by(employment_records.c.created_at.desc(), employment_records.c.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        if employment == "已入职":
            values = {"locked": True, "status": "锁定", "delivery_status": "已入职"}
        else:
            recommendation = bind.execute(
                sa.select(recommendations.c.status)
                .where(recommendations.c.candidate_id == candidate_id)
                .order_by(recommendations.c.created_at.desc(), recommendations.c.id.desc())
                .limit(1)
            ).scalar_one_or_none()
            values = (
                {"locked": True, "status": "锁定", "delivery_status": ACTIVE_STATUS_MAP.get(recommendation, "已推荐")}
                if recommendation
                else {"locked": False, "status": "未锁定", "delivery_status": "未推荐", "owner_user_id": None}
            )
        employment_row = bind.execute(
            sa.select(employment_records.c.status, employment_records.c.onboard_date)
            .where(employment_records.c.candidate_id == candidate_id)
            .order_by(employment_records.c.created_at.desc(), employment_records.c.id.desc())
            .limit(1)
        ).first()
        warranty_status = ""
        if employment_row and employment_row.status == "已入职" and employment_row.onboard_date:
            onboard = employment_row.onboard_date
            if onboard.tzinfo is None:
                onboard = onboard.replace(tzinfo=timezone.utc)
            warranty_status = "质保到期" if datetime.now(timezone.utc) > onboard + timedelta(days=180) else "质保中"
        values["candidate_warranty_status"] = warranty_status
        bind.execute(candidates.update().where(candidates.c.id == candidate_id).values(**values))


def downgrade() -> None:
    # 状态归一化不可逆；字段结构未变化。
    pass

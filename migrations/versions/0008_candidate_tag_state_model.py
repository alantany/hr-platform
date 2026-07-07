"""finalize candidate three-dimension status tags

Revision ID: 0008_tag_state_model
Revises: 0007_status_cleanup
"""

from datetime import datetime, timedelta, timezone

from alembic import op
import sqlalchemy as sa


revision = "0008_tag_state_model"
down_revision = "0007_status_cleanup"
branch_labels = None
depends_on = None


FLOW_MAP = {
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
    employments = sa.Table("employment_records", metadata, autoload_with=bind)
    warranty_rules = sa.Table("warranty_rules", metadata, autoload_with=bind)
    tags = sa.Table("tag_dictionaries", metadata, autoload_with=bind)

    bind.execute(warranty_rules.update().where(warranty_rules.c.scope == "入职质保期").values(months=6))
    now = datetime.now(timezone.utc)

    for candidate_id in bind.execute(sa.select(candidates.c.id)).scalars().all():
        employment = bind.execute(
            sa.select(employments.c.status, employments.c.onboard_date)
            .where(employments.c.candidate_id == candidate_id)
            .order_by(employments.c.created_at.desc(), employments.c.id.desc())
            .limit(1)
        ).first()
        recommendation = bind.execute(
            sa.select(recommendations.c.status)
            .where(recommendations.c.candidate_id == candidate_id)
            .order_by(recommendations.c.created_at.desc(), recommendations.c.id.desc())
            .limit(1)
        ).scalar_one_or_none()

        if employment and employment.status == "已入职":
            flow_status = "已入职"
        elif recommendation:
            flow_status = FLOW_MAP.get(recommendation, "已推荐")
        else:
            flow_status = "未推荐"

        warranty_status = ""
        if employment and employment.status == "已入职" and employment.onboard_date:
            onboard = employment.onboard_date
            if onboard.tzinfo is None:
                onboard = onboard.replace(tzinfo=timezone.utc)
            warranty_status = "质保到期" if now > onboard + timedelta(days=180) else "质保中"

        bind.execute(
            candidates.update().where(candidates.c.id == candidate_id).values(
                locked=bool(recommendation),
                status="锁定" if recommendation else "未锁定",
                delivery_status=flow_status if recommendation else "未推荐",
                candidate_warranty_status=warranty_status,
                **({} if recommendation else {"owner_user_id": None}),
            )
        )

    tag_defaults = [
        ("status", "锁定状态", "primary-soft", 80),
        ("delivery_status", "流程状态", "subtle-outline", 90),
        ("candidate_warranty_status", "质保状态", "muted", 100),
    ]
    for field_key, field_label, style_key, sort_order in tag_defaults:
        exists = bind.execute(
            sa.select(tags.c.id).where(tags.c.object_type == "candidate", tags.c.field_key == field_key).limit(1)
        ).scalar_one_or_none()
        if exists is None:
            bind.execute(tags.insert().values(
                category="候选人",
                name=field_label,
                color=style_key,
                object_type="candidate",
                field_key=field_key,
                field_label=field_label,
                style_key=style_key,
                sort_order=sort_order,
                enabled=True,
                created_at=now,
                updated_at=now,
            ))


def downgrade() -> None:
    # 状态与用户标签配置均不做破坏性回滚。
    pass

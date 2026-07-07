"""remove legacy auto-created employment records

Revision ID: 0009_remove_auto_entry
Revises: 0008_tag_state_model
"""

from alembic import op
import sqlalchemy as sa


revision = "0009_remove_auto_entry"
down_revision = "0008_tag_state_model"
branch_labels = None
depends_on = None


LEGACY_AUTO_NOTE = "通过系统推荐流程自动流转入职"


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    candidates = sa.Table("candidates", metadata, autoload_with=bind)
    recommendations = sa.Table("recommendations", metadata, autoload_with=bind)
    employments = sa.Table("employment_records", metadata, autoload_with=bind)

    candidate_ids = bind.execute(
        sa.select(employments.c.candidate_id).where(employments.c.note == LEGACY_AUTO_NOTE)
    ).scalars().all()
    if not candidate_ids:
        return

    bind.execute(employments.delete().where(employments.c.note == LEGACY_AUTO_NOTE))
    bind.execute(
        recommendations.update()
        .where(recommendations.c.candidate_id.in_(candidate_ids), recommendations.c.status == "已入职")
        .values(status="面试中")
    )

    for candidate_id in set(candidate_ids):
        remaining_manual_entry = bind.execute(
            sa.select(employments.c.id)
            .where(employments.c.candidate_id == candidate_id, employments.c.status == "已入职")
            .limit(1)
        ).scalar_one_or_none()
        if remaining_manual_entry:
            continue
        recommendation = bind.execute(
            sa.select(recommendations.c.status)
            .where(recommendations.c.candidate_id == candidate_id)
            .order_by(recommendations.c.created_at.desc(), recommendations.c.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        flow_status = "面试中" if recommendation in {"安排面试", "面试中"} else "已推荐"
        bind.execute(
            candidates.update().where(candidates.c.id == candidate_id).values(
                locked=bool(recommendation),
                status="锁定" if recommendation else "未锁定",
                delivery_status=flow_status if recommendation else "未推荐",
                candidate_warranty_status="",
                **({} if recommendation else {"owner_user_id": None}),
            )
        )


def downgrade() -> None:
    # 被清理的是旧代码伪造记录，不恢复。
    pass

"""reconcile candidate lock and recommendation summary state

Revision ID: 0005_candidate_state
Revises: 0004_candidate_status_fields
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_candidate_state"
down_revision = "0004_candidate_status_fields"
branch_labels = None
depends_on = None


STATUS_MAP = {
    "待推荐": "已推荐",
    "已推荐": "已推荐",
    "客户已收": "已推荐",
    "客户未收": "已推荐",
    "安排面试": "面试中",
    "面试中": "面试中",
    "已录用": "已录用",
}


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()
    candidates = sa.Table("candidates", metadata, autoload_with=bind)
    recommendations = sa.Table("recommendations", metadata, autoload_with=bind)

    candidate_ids = bind.execute(sa.select(candidates.c.id)).scalars().all()
    for candidate_id in candidate_ids:
        recommendation = bind.execute(
            sa.select(recommendations.c.status)
            .where(
                recommendations.c.candidate_id == candidate_id,
                recommendations.c.status.in_(tuple(STATUS_MAP)),
            )
            .order_by(recommendations.c.created_at.desc(), recommendations.c.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        values = (
            {"locked": True, "status": "锁定", "delivery_status": STATUS_MAP[recommendation]}
            if recommendation
            else {"locked": False, "status": "未锁定", "delivery_status": "未推荐", "owner_user_id": None}
        )
        bind.execute(candidates.update().where(candidates.c.id == candidate_id).values(**values))


def downgrade() -> None:
    # 数据修复不可逆；旧版本字段仍保留，无需结构回滚。
    pass

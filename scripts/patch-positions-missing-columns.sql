-- 安全补全 positions 表缺失字段（可重复执行，不会删数据）
-- 用法见 windows/04-patch-positions-columns.bat 或下方 psql 命令

BEGIN;

ALTER TABLE positions ADD COLUMN IF NOT EXISTS owner_user_id INTEGER;
ALTER TABLE positions ADD COLUMN IF NOT EXISTS age_requirement TEXT NOT NULL DEFAULT '';
ALTER TABLE positions ADD COLUMN IF NOT EXISTS education_requirement TEXT NOT NULL DEFAULT '';
ALTER TABLE positions ADD COLUMN IF NOT EXISTS experience_requirement TEXT NOT NULL DEFAULT '';
ALTER TABLE positions ADD COLUMN IF NOT EXISTS requirement_tags JSON;
ALTER TABLE positions ADD COLUMN IF NOT EXISTS target_resume_count INTEGER NOT NULL DEFAULT 10;
ALTER TABLE positions ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '';

COMMIT;

-- 验证
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'positions'
  AND column_name IN (
    'owner_user_id',
    'age_requirement',
    'education_requirement',
    'experience_requirement',
    'requirement_tags',
    'target_resume_count',
    'description'
  )
ORDER BY column_name;

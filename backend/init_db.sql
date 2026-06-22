-- 创建 schema
CREATE SCHEMA IF NOT EXISTS recruit;

-- 幂等创建数据库角色/用户
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user_delivery') THEN
        CREATE ROLE user_delivery WITH LOGIN PASSWORD 'delivery_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user_recruit') THEN
        CREATE ROLE user_recruit WITH LOGIN PASSWORD 'recruit_pass';
    END IF;
END
$$;

-- 授予数据库级的创建权限（允许创建 Schema）
GRANT CREATE ON DATABASE hr_platform TO user_delivery;
GRANT CREATE ON DATABASE hr_platform TO user_recruit;

-- 授予 Schema 的 USAGE 权限，使得用户可以访问 Schema 内的对象
GRANT USAGE ON SCHEMA public TO user_delivery;
GRANT USAGE ON SCHEMA recruit TO user_delivery;

GRANT USAGE ON SCHEMA public TO user_recruit;
GRANT USAGE ON SCHEMA recruit TO user_recruit;

-- 针对未来新创建保持默认权限配置
-- user_delivery 默认对 public schema 下所有表拥有全部权限，对 recruit schema 下所有表拥有只读权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO user_delivery;
ALTER DEFAULT PRIVILEGES IN SCHEMA recruit GRANT SELECT ON TABLES TO user_delivery;

-- user_recruit 默认对 recruit schema 下所有表拥有全部权限，对 public schema 下所有表拥有只读权限
ALTER DEFAULT PRIVILEGES IN SCHEMA recruit GRANT ALL PRIVILEGES ON TABLES TO user_recruit;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO user_recruit;

-- 针对未来新创建的序列，配置默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO user_delivery;
ALTER DEFAULT PRIVILEGES IN SCHEMA recruit GRANT USAGE, SELECT ON SEQUENCES TO user_recruit;

-- 同时授权当前已存在的表（以防有表被提前建立）
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_delivery;
GRANT SELECT ON ALL TABLES IN SCHEMA recruit TO user_delivery;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA recruit TO user_recruit;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO user_recruit;

-- 同时授权当前已存在的序列
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO user_delivery;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA recruit TO user_recruit;

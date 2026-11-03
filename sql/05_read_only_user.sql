-- TRUSTLENS: READ-ONLY DATABASE USER
-- Password must be configured separately and securely.
--
-- Run this script as the database/schema owner that creates future tables.
-- Existing tables are covered by the GRANT statements below.
-- Default privileges apply only to future tables created by the role
-- specified in ALTER DEFAULT PRIVILEGES (the current role here).

CREATE ROLE trustlens_reader LOGIN;

GRANT CONNECT ON DATABASE trustlens TO trustlens_reader;
GRANT USAGE ON SCHEMA raw TO trustlens_reader;
GRANT USAGE ON SCHEMA analytics TO trustlens_reader;

GRANT SELECT ON ALL TABLES IN SCHEMA raw TO trustlens_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO trustlens_reader;

ALTER DEFAULT PRIVILEGES IN SCHEMA raw
GRANT SELECT ON TABLES TO trustlens_reader;

ALTER DEFAULT PRIVILEGES IN SCHEMA analytics
GRANT SELECT ON TABLES TO trustlens_reader;

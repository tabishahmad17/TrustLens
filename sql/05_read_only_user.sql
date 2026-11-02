-- TRUSTLENS: READ-ONLY DATABASE USER
-- Password must be configured separately and securely.

CREATE ROLE trustlens_reader LOGIN;

GRANT CONNECT ON DATABASE trustlens TO trustlens_reader;
GRANT USAGE ON SCHEMA raw TO trustlens_reader;
GRANT USAGE ON SCHEMA analytics TO trustlens_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA raw TO trustlens_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO trustlens_reader;

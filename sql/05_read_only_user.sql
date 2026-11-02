
-- ==========================================
-- TRUSTLENS: READ-ONLY DATABASE USER
-- ==========================================

-- 1. Create a dedicated read-only user
EATE ROLE trustlens_reader
LOGIN  
PASSWORD 'TATASKY@a123';



-- 2. Allow connection to TrustLens database
GRANT CONNECT ON DATABASE trustlens
TO trustlens_reader;


-- 3. Allow access to approved schemas
GRANT USAGE ON SCHEMA raw
TO trustlens_reader;

GRANT USAGE ON SCHEMA analytics
TO trustlens_reader;


-- 4. Allow SELECT on existing raw tables
GRANT SELECT ON ALL TABLES IN SCHEMA raw
TO trustlens_reader;


-- 5. Allow SELECT on existing analytics views
GRANT SELECT ON ALL TABLES IN SCHEMA analytics
TO trustlens_reader;

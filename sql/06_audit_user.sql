
-- ==========================================
-- TRUSTLENS: AUDIT DATABASE USER
-- ==========================================
-- 1. Create restricted audit 
CREATE ROLE trustlens_auditor
LOGIN
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
PASSWORD 'Ramish@123';



-- 2. Allow connection to TrustLens
GRANT CONNECT ON DATABASE trustlens
TO trustlens_auditor;


-- 3. Allow access to the audit schema
GRANT USAGE ON SCHEMA ops
TO trustlens_auditor;


-- 4. Allow inserting audit records only
GRANT INSERT ON TABLE ops.audit_log
TO trustlens_auditor;


-- 5. Allow generating the BIGSERIAL ID
GRANT USAGE ON SEQUENCE ops.audit_log_id_seq
TO trustlens_auditor;

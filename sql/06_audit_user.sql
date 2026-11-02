-- TRUSTLENS: AUDIT DATABASE USER
-- Password must be configured separately and securely.

CREATE ROLE trustlens_auditor
LOGIN
NOSUPERUSER
NOCREATEDB
NOCREATEROLE;

GRANT CONNECT ON DATABASE trustlens TO trustlens_auditor;
GRANT USAGE ON SCHEMA ops TO trustlens_auditor;
GRANT INSERT ON TABLE ops.audit_log TO trustlens_auditor;
GRANT USAGE ON SEQUENCE ops.audit_log_id_seq TO trustlens_auditor;

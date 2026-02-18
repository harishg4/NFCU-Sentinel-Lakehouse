-- DAT-10: Databricks-native storage + RBAC template
-- Replace placeholders wrapped in <> before execution.

-- Storage credential for object storage IAM role/service principal.
CREATE STORAGE CREDENTIAL IF NOT EXISTS nfcu_storage_credential
WITH <CLOUD_PROVIDER_AUTH_CLAUSE>
COMMENT 'Storage credential for NFCU Sentinel Lakehouse';

-- External locations by environment.
CREATE EXTERNAL LOCATION IF NOT EXISTS nfcu_dev_ext
URL '<DEV_STORAGE_URL>'
WITH (STORAGE CREDENTIAL nfcu_storage_credential);

CREATE EXTERNAL LOCATION IF NOT EXISTS nfcu_qa_ext
URL '<QA_STORAGE_URL>'
WITH (STORAGE CREDENTIAL nfcu_storage_credential);

CREATE EXTERNAL LOCATION IF NOT EXISTS nfcu_prod_ext
URL '<PROD_STORAGE_URL>'
WITH (STORAGE CREDENTIAL nfcu_storage_credential);

-- Volumes for managed paths.
CREATE VOLUME IF NOT EXISTS nfcu_dev.ops.raw_volume;
CREATE VOLUME IF NOT EXISTS nfcu_dev.ops.checkpoint_volume;
CREATE VOLUME IF NOT EXISTS nfcu_qa.ops.raw_volume;
CREATE VOLUME IF NOT EXISTS nfcu_qa.ops.checkpoint_volume;
CREATE VOLUME IF NOT EXISTS nfcu_prod.ops.raw_volume;
CREATE VOLUME IF NOT EXISTS nfcu_prod.ops.checkpoint_volume;

-- Groups expected:
--   de_team, analyst_team, compliance_team

-- Catalog access baseline.
GRANT USE CATALOG ON CATALOG nfcu_dev TO `de_team`;
GRANT USE CATALOG ON CATALOG nfcu_qa TO `de_team`;
GRANT USE CATALOG ON CATALOG nfcu_prod TO `de_team`;

GRANT USE CATALOG ON CATALOG nfcu_prod TO `analyst_team`;
GRANT USE CATALOG ON CATALOG nfcu_prod TO `compliance_team`;

-- Data engineer write permissions.
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.bronze_banking TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.bronze_cards TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.bronze_compliance TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.silver_banking TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.silver_fraud TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.gold_fraud TO `de_team`;
GRANT USE SCHEMA, CREATE TABLE, SELECT, MODIFY ON SCHEMA nfcu_dev.gold_compliance TO `de_team`;

-- Analyst read on curated gold only.
GRANT USE SCHEMA, SELECT ON SCHEMA nfcu_prod.gold_fraud TO `analyst_team`;
GRANT USE SCHEMA, SELECT ON SCHEMA nfcu_prod.gold_compliance TO `analyst_team`;

-- Compliance read on compliance surfaces.
GRANT USE SCHEMA, SELECT ON SCHEMA nfcu_prod.gold_compliance TO `compliance_team`;
GRANT USE SCHEMA, SELECT ON SCHEMA nfcu_prod.silver_fraud TO `compliance_team`;

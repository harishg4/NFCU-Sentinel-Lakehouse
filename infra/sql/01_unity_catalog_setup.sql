-- DAT-6: Unity Catalog foundation setup
-- Run in a Databricks SQL environment with account/admin privileges.

-- Catalogs
CREATE CATALOG IF NOT EXISTS nfcu_dev;
CREATE CATALOG IF NOT EXISTS nfcu_qa;
CREATE CATALOG IF NOT EXISTS nfcu_prod;

-- Bronze schemas
CREATE SCHEMA IF NOT EXISTS nfcu_dev.bronze_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_dev.bronze_cards;
CREATE SCHEMA IF NOT EXISTS nfcu_dev.bronze_compliance;

CREATE SCHEMA IF NOT EXISTS nfcu_qa.bronze_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_qa.bronze_cards;
CREATE SCHEMA IF NOT EXISTS nfcu_qa.bronze_compliance;

CREATE SCHEMA IF NOT EXISTS nfcu_prod.bronze_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_prod.bronze_cards;
CREATE SCHEMA IF NOT EXISTS nfcu_prod.bronze_compliance;

-- Silver schemas
CREATE SCHEMA IF NOT EXISTS nfcu_dev.silver_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_dev.silver_fraud;

CREATE SCHEMA IF NOT EXISTS nfcu_qa.silver_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_qa.silver_fraud;

CREATE SCHEMA IF NOT EXISTS nfcu_prod.silver_banking;
CREATE SCHEMA IF NOT EXISTS nfcu_prod.silver_fraud;

-- Gold schemas
CREATE SCHEMA IF NOT EXISTS nfcu_dev.gold_fraud;
CREATE SCHEMA IF NOT EXISTS nfcu_dev.gold_compliance;

CREATE SCHEMA IF NOT EXISTS nfcu_qa.gold_fraud;
CREATE SCHEMA IF NOT EXISTS nfcu_qa.gold_compliance;

CREATE SCHEMA IF NOT EXISTS nfcu_prod.gold_fraud;
CREATE SCHEMA IF NOT EXISTS nfcu_prod.gold_compliance;

-- Operational schemas
CREATE SCHEMA IF NOT EXISTS nfcu_dev.ops;
CREATE SCHEMA IF NOT EXISTS nfcu_qa.ops;
CREATE SCHEMA IF NOT EXISTS nfcu_prod.ops;

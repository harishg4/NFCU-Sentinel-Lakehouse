# Infra SQL Templates

Sprint 1 foundation SQL templates for Databricks deployment.

## Files

- `infra/sql/01_unity_catalog_setup.sql`
  - Implements DAT-6 catalog/schema setup.
- `infra/sql/02_storage_and_rbac.sql`
  - Implements DAT-10 storage credential/external location/RBAC baseline.

## Usage

1. Replace placeholders in `02_storage_and_rbac.sql`.
2. Execute `01_unity_catalog_setup.sql` first.
3. Execute `02_storage_and_rbac.sql` next.
4. Validate with `SHOW CATALOGS`, `SHOW SCHEMAS`, and `SHOW GRANTS`.

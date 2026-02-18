# Local Synthetic Dataset (Sprint 1)

This folder contains synthetic data for Sprint 1 development.

## Files

- `data/raw/fiserv_dna/transaction_detail.csv` (20,000 rows)
- `data/raw/tsys_fis/card_auth_stream.jsonl` (12,000 events)
- `data/raw/tsys_fis/card_clearing.csv` (12,000 rows)
- `data/raw/compliance/ofac_watchlist.csv` (300 rows)
- `data/raw/compliance/fincen_advisories.json` (50 advisories)
- `data/raw/compliance/blocked_entities.csv` (150 rows)

Manifest: `data/reference/dataset_manifest.json`

## Mapping to Sprint 1 Pipelines

- `B-001` -> `data/raw/fiserv_dna/transaction_detail.csv`
- `B-002` -> `data/raw/tsys_fis/card_auth_stream.jsonl` and `data/raw/tsys_fis/card_clearing.csv`
- `B-003` -> `data/raw/compliance/ofac_watchlist.csv`, `data/raw/compliance/fincen_advisories.json`, `data/raw/compliance/blocked_entities.csv`

## Note

Synthetic portfolio data only. No real customer or NFCU production data is included.

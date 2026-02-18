from pathlib import Path

from nfcu_sentinel.pipelines.bronze.sprint1_runner import run_sprint1_bronze


def test_run_sprint1_bronze_creates_outputs(tmp_path: Path) -> None:
    repo = tmp_path
    (repo / "data/raw/fiserv_dna").mkdir(parents=True)
    (repo / "data/raw/tsys_fis").mkdir(parents=True)
    (repo / "data/raw/compliance").mkdir(parents=True)

    (repo / "data/raw/fiserv_dna/transaction_detail.csv").write_text(
        "transaction_id,account_id,member_id,transaction_timestamp,transaction_type,amount,currency_code,description,channel,country_code,last_modified_ts\n"
        "TXN1,ACCT1,MEM1,2026-02-18T00:00:00+00:00,DEBIT,10.0,USD,test,ONLINE,US,2026-02-18T00:00:00+00:00\n",
        encoding="utf-8",
    )
    (repo / "data/raw/tsys_fis/card_auth_stream.jsonl").write_text(
        '{"event_id":"AUTH1","card_number":"4111111111111111","member_id":"MEM1"}\n',
        encoding="utf-8",
    )
    (repo / "data/raw/tsys_fis/card_clearing.csv").write_text(
        "clearing_id,event_id,member_id,posted_amount,currency_code,posting_date,merchant_id,country_code\n"
        "CLR1,AUTH1,MEM1,10.0,USD,2026-02-18,M1,US\n",
        encoding="utf-8",
    )
    (repo / "data/raw/compliance/ofac_watchlist.csv").write_text(
        "watchlist_id,name,alias,country,program,added_date\nOF1,NAME1,ALIAS1,IR,SDN,2026-01-01\n",
        encoding="utf-8",
    )
    (repo / "data/raw/compliance/blocked_entities.csv").write_text(
        "entity_id,entity_name,reason,status\nBL1,BLKNAME,KYC_FAIL,ACTIVE\n",
        encoding="utf-8",
    )
    (repo / "data/raw/compliance/fincen_advisories.json").write_text(
        '{"advisories":[{"advisory_id":"FIN1","title":"advisory"}]}',
        encoding="utf-8",
    )

    results = run_sprint1_bronze(repo)

    assert len(results) == 3
    assert (repo / "data/bronze/b001_txn_core_raw.jsonl").exists()
    assert (repo / "data/bronze/b002_card_transactions_raw.jsonl").exists()
    assert (repo / "data/bronze/b003_compliance_reference_raw.jsonl").exists()

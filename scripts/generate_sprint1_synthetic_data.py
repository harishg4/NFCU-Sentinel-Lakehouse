from __future__ import annotations

import csv
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw"


def rand_dt(days_back: int = 30) -> datetime:
    now = datetime.now(timezone.utc)
    delta = timedelta(seconds=random.randint(0, days_back * 24 * 3600))
    return now - delta


def write_core_banking(n: int = 20000) -> None:
    path = DATA / "fiserv_dna" / "transaction_detail.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "transaction_id",
            "account_id",
            "member_id",
            "transaction_timestamp",
            "transaction_type",
            "amount",
            "currency_code",
            "description",
            "channel",
            "country_code",
            "last_modified_ts",
        ])
        for i in range(1, n + 1):
            ts = rand_dt()
            amt = round(random.uniform(1.0, 25000.0), 2)
            ttype = random.choice(["DEBIT", "CREDIT", "ATM", "WIRE", "ACH", "CASH_DEPOSIT"])
            w.writerow([
                f"TXN{i:08d}",
                f"ACCT{random.randint(1, 30000):06d}",
                f"MEM{random.randint(1, 15000):06d}",
                ts.isoformat(),
                ttype,
                amt,
                "USD",
                f"{ttype} transaction",
                random.choice(["ONLINE", "BRANCH", "ATM", "MOBILE"]),
                random.choice(["US", "US", "US", "CA", "MX"]),
                (ts + timedelta(minutes=random.randint(0, 60))).isoformat(),
            ])


def write_card_data(n: int = 12000) -> None:
    auth_path = DATA / "tsys_fis" / "card_auth_stream.jsonl"
    clearing_path = DATA / "tsys_fis" / "card_clearing.csv"
    auth_path.parent.mkdir(parents=True, exist_ok=True)

    with auth_path.open("w", encoding="utf-8") as f:
        for i in range(1, n + 1):
            ts = rand_dt(7)
            rec = {
                "event_id": f"AUTH{i:08d}",
                "card_number": f"4{random.randint(10**14, 10**15 - 1)}",
                "member_id": f"MEM{random.randint(1, 15000):06d}",
                "merchant_id": f"M{random.randint(1, 3000):05d}",
                "merchant_name": random.choice(["AMAZON", "WALMART", "TARGET", "UBER", "SHELL", "COSTCO"]),
                "mcc": random.choice(["5411", "5541", "5999", "4121", "5812"]),
                "auth_amount": round(random.uniform(1.0, 5000.0), 2),
                "currency_code": "USD",
                "auth_ts": ts.isoformat(),
                "country_code": random.choice(["US", "US", "US", "GB", "IN", "AE"]),
                "is_card_present": random.choice([True, False]),
            }
            f.write(json.dumps(rec) + "\n")

    with clearing_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "clearing_id",
            "event_id",
            "member_id",
            "posted_amount",
            "currency_code",
            "posting_date",
            "merchant_id",
            "country_code",
        ])
        for i in range(1, n + 1):
            dt = rand_dt(10)
            w.writerow([
                f"CLR{i:08d}",
                f"AUTH{i:08d}",
                f"MEM{random.randint(1, 15000):06d}",
                round(random.uniform(1.0, 5000.0), 2),
                "USD",
                dt.date().isoformat(),
                f"M{random.randint(1, 3000):05d}",
                random.choice(["US", "US", "US", "CA", "MX"]),
            ])


def write_compliance() -> None:
    ofac_path = DATA / "compliance" / "ofac_watchlist.csv"
    fincen_path = DATA / "compliance" / "fincen_advisories.json"
    blocked_path = DATA / "compliance" / "blocked_entities.csv"
    ofac_path.parent.mkdir(parents=True, exist_ok=True)

    with ofac_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["watchlist_id", "name", "alias", "country", "program", "added_date"])
        for i in range(1, 301):
            w.writerow([
                f"OFAC{i:06d}",
                f"ENTITY_{i}",
                f"ALIAS_{i}",
                random.choice(["IR", "RU", "KP", "SY", "CU", "VE"]),
                random.choice(["SDN", "NS-ISA", "FSE", "NON-SDN"]),
                (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 1500))).date().isoformat(),
            ])

    advisories = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "advisories": [
            {
                "advisory_id": f"FIN-{i:04d}",
                "title": f"Synthetic advisory {i}",
                "risk_theme": random.choice(["Structuring", "Human Trafficking", "Cyber Fraud", "Sanctions Evasion"]),
                "severity": random.choice(["medium", "high", "critical"]),
            }
            for i in range(1, 51)
        ],
    }
    fincen_path.write_text(json.dumps(advisories, indent=2), encoding="utf-8")

    with blocked_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entity_id", "entity_name", "reason", "status"])
        for i in range(1, 151):
            w.writerow([
                f"BLK{i:05d}",
                f"BLOCKED_ENTITY_{i}",
                random.choice(["KYC_FAIL", "FRAUD_CONFIRMED", "SANCTIONS_MATCH"]),
                random.choice(["ACTIVE", "REVIEW", "CLOSED"]),
            ])


def write_manifest() -> None:
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "datasets": [
            "data/raw/fiserv_dna/transaction_detail.csv",
            "data/raw/tsys_fis/card_auth_stream.jsonl",
            "data/raw/tsys_fis/card_clearing.csv",
            "data/raw/compliance/ofac_watchlist.csv",
            "data/raw/compliance/fincen_advisories.json",
            "data/raw/compliance/blocked_entities.csv",
        ],
        "note": "Synthetic dataset for portfolio development only. Not real NFCU/customer data.",
    }
    (ROOT / "data" / "reference" / "dataset_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def main() -> None:
    write_core_banking()
    write_card_data()
    write_compliance()
    write_manifest()
    print("Synthetic Sprint 1 datasets generated.")


if __name__ == "__main__":
    main()

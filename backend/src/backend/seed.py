"""Seed Neo4j with synthetic banking data: customers, accounts, and
transactions, including two circular fraud rings among the accounts.
"""

import os
import random
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.environ["NEO4J_PASSWORD"]

TOTAL_ACCOUNTS = 50
FRAUD_RING_SIZES = [5, 4]


def clear_database(session):
    session.run("MATCH (n) DETACH DELETE n")


def create_customers_and_accounts(session, count):
    session.run(
        """
        UNWIND range(1, $count) AS i
        CREATE (c:Customer {id: 'cust-' + toString(i), name: 'Customer ' + toString(i)})
        CREATE (a:Account {id: 'acct-' + toString(i), balance: 1000})
        CREATE (c)-[:OWNS]->(a)
        """,
        count=count,
    )


def create_fraud_ring(session, account_ids, ring_label):
    n = len(account_ids)
    for idx in range(n):
        src, dst = account_ids[idx], account_ids[(idx + 1) % n]
        session.run(
            """
            MATCH (a:Account {id: $src}), (b:Account {id: $dst})
            CREATE (a)-[:TRANSFER {amount: $amount, timestamp: datetime(), ring: $ring}]->(b)
            """,
            src=src,
            dst=dst,
            amount=round(random.uniform(500, 5000), 2),
            ring=ring_label,
        )


def create_normal_transactions(session, account_ids, ring_account_ids):
    normal_ids = [a for a in account_ids if a not in ring_account_ids]
    for src in normal_ids:
        targets = random.sample(
            [a for a in account_ids if a != src], random.randint(1, 3)
        )
        for dst in targets:
            session.run(
                """
                MATCH (a:Account {id: $src}), (b:Account {id: $dst})
                CREATE (a)-[:TRANSFER {amount: $amount, timestamp: datetime()}]->(b)
                """,
                src=src,
                dst=dst,
                amount=round(random.uniform(10, 2000), 2),
            )


def main():
    account_ids = [f"acct-{i}" for i in range(1, TOTAL_ACCOUNTS + 1)]
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    with driver.session() as session:
        clear_database(session)
        create_customers_and_accounts(session, TOTAL_ACCOUNTS)

        ring_account_ids = []
        start = 0
        for ring_idx, size in enumerate(FRAUD_RING_SIZES, start=1):
            ring_ids = account_ids[start : start + size]
            create_fraud_ring(session, ring_ids, ring_label=f"ring-{ring_idx}")
            ring_account_ids.extend(ring_ids)
            start += size

        create_normal_transactions(session, account_ids, ring_account_ids)

    driver.close()
    print(f"Seeded {TOTAL_ACCOUNTS} accounts, {len(FRAUD_RING_SIZES)} fraud rings.")


if __name__ == "__main__":
    main()

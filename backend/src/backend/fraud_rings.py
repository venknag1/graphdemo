"""Cycle detection over Account transfers: the graph-based fraud signal."""

CYPHER = """
MATCH p=(a:Account)-[:TRANSFER*3..6]->(a)
RETURN [n IN nodes(p)[..-1] | n.id] AS accounts,
       [r IN relationships(p) | {
           source: startNode(r).id,
           target: endNode(r).id,
           amount: r.amount,
           timestamp: toString(r.timestamp)
       }] AS transfers
"""


def _rotate_to_min(accounts, transfers):
    start = accounts.index(min(accounts))
    return accounts[start:] + accounts[:start], transfers[start:] + transfers[:start]


def find_fraud_rings(session):
    """Detect circular transfer chains and return each distinct cycle once."""
    rings, seen = [], set()
    for record in session.run(CYPHER):
        accounts = record["accounts"]
        if len(set(accounts)) != len(accounts):
            continue  # not a simple cycle - revisits a node partway through
        accounts, transfers = _rotate_to_min(accounts, record["transfers"])
        key = tuple(accounts)
        if key in seen:
            continue
        seen.add(key)
        rings.append({"accounts": accounts, "transfers": transfers})
    return rings

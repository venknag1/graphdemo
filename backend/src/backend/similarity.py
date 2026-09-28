"""Similar-account search via Neo4j's native vector index."""

CYPHER = """
MATCH (a:Account {{id: $account_id}})
CALL db.index.vector.queryNodes('account_embedding_{metric}', $k, a.embedding_{metric})
YIELD node, score
WHERE node.id <> $account_id
RETURN node.id AS account, score
ORDER BY score DESC
LIMIT $limit
"""


def find_similar_accounts(session, account_id, metric, limit=5):
    query = CYPHER.format(metric=metric)
    result = session.run(query, account_id=account_id, k=limit + 1, limit=limit)
    return [{"account": r["account"], "score": r["score"]} for r in result]

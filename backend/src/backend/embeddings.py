"""Real per-account behavior embeddings, computed from the TRANSFER data
already in Neo4j (not fabricated), plus the vector indexes used to search
them.

Each account's embedding is 6 statistics about how it sends/receives
money. Raw values live on very different scales (degree counts are
single digits, amounts run into the thousands), so amounts would
completely dominate distance calculations if left unstandardized - each
feature is standardized (zero mean, unit variance) across all accounts
before being stored.
"""

FEATURES = ["out_degree", "in_degree", "total_sent", "total_received", "avg_sent", "avg_received"]
DIMENSIONS = len(FEATURES)

STATS_CYPHER = """
MATCH (a:Account)
CALL (a) {
    MATCH (a)-[t:TRANSFER]->()
    RETURN count(t) AS out_degree,
           coalesce(sum(t.amount), 0.0) AS total_sent,
           coalesce(avg(t.amount), 0.0) AS avg_sent
}
CALL (a) {
    MATCH (a)<-[t:TRANSFER]-()
    RETURN count(t) AS in_degree,
           coalesce(sum(t.amount), 0.0) AS total_received,
           coalesce(avg(t.amount), 0.0) AS avg_received
}
RETURN a.id AS id, out_degree, in_degree, total_sent, total_received, avg_sent, avg_received
"""


def fetch_account_stats(session):
    result = session.run(STATS_CYPHER)
    return {r["id"]: [float(r[f]) for f in FEATURES] for r in result}


def _standardize(stats):
    ids = list(stats.keys())
    n = len(ids)
    means = [sum(stats[i][d] for i in ids) / n for d in range(DIMENSIONS)]
    stds = [
        (sum((stats[i][d] - means[d]) ** 2 for i in ids) / n) ** 0.5
        for d in range(DIMENSIONS)
    ]
    return {
        i: [
            (stats[i][d] - means[d]) / stds[d] if stds[d] > 0 else 0.0
            for d in range(DIMENSIONS)
        ]
        for i in ids
    }


def build_embeddings(session):
    return _standardize(fetch_account_stats(session))


def write_embeddings(session, embeddings):
    """Store each embedding under embedding_cosine and embedding_euclidean.
    Neo4j allows only one vector index per (label, property) pair, so a
    single index can't serve both similarity functions - the same values
    are duplicated under two property names, one per metric's index.
    """
    session.run(
        """
        UNWIND $rows AS row
        MATCH (a:Account {id: row.id})
        SET a.embedding_cosine = row.embedding, a.embedding_euclidean = row.embedding
        """,
        rows=[{"id": k, "embedding": v} for k, v in embeddings.items()],
    )


def create_vector_indexes(session):
    for metric in ("cosine", "euclidean"):
        session.run(f"DROP INDEX account_embedding_{metric} IF EXISTS")
        session.run(
            f"""
            CREATE VECTOR INDEX account_embedding_{metric} IF NOT EXISTS
            FOR (a:Account) ON a.embedding_{metric}
            OPTIONS {{indexConfig: {{
                `vector.dimensions`: {DIMENSIONS},
                `vector.similarity_function`: '{metric}'
            }}}}
            """
        )
    session.run("CALL db.awaitIndexes()")

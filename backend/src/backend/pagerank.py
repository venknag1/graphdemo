"""PageRank via Neo4j GDS.

A GDS graph projection is a snapshot, not a live view - it goes stale
whenever accounts/transfers change (e.g. after re-seeding). Since this
graph is tiny (50 accounts), the projection is dropped and recreated on
every call rather than risk serving a result from outdated data.
"""

GRAPH_NAME = "accountGraph"


def _refresh_projection(session):
    session.run("CALL gds.graph.drop($name, false)", name=GRAPH_NAME)
    session.run(
        "CALL gds.graph.project($name, 'Account', 'TRANSFER')", name=GRAPH_NAME
    )


def run_pagerank(session, limit=10):
    _refresh_projection(session)
    result = session.run(
        """
        CALL gds.pageRank.stream($name)
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).id AS account, score
        ORDER BY score DESC
        LIMIT $limit
        """,
        name=GRAPH_NAME,
        limit=limit,
    )
    return [{"account": r["account"], "score": r["score"]} for r in result]

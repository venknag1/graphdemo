Create a demo application to demonstrate a graph knowledge application to detect fraud in a banking domain. The back end and front end should be on docker. The front-end should be in React.js and visually depict the graph data in the back-end Neo4j database. The back-end Neo4j database should be populated with synthetic data from the banking domain.

## Goal: learn Neo4j along the way

A second goal of this project is to build the author's understanding of Neo4j, not just ship a demo. This means:
- Prefer plain, readable Cypher over black-box abstractions (e.g. avoid ORMs/query builders that hide Cypher).
- Explain graph modeling decisions as they're made (why a relationship vs. a property, why a node label vs. a value).
- Use the Neo4j Browser to inspect data and run queries manually, not just through the app, so the graph is visible directly.
- Where relevant, introduce Neo4j Graph Data Science (GDS) concepts (e.g. PageRank, community detection) with explanation rather than treating them as a library call.

## Backend: Neo4j (Community / "lite") on Docker Desktop

- Use the official `neo4j:5-community` image (free Community Edition — no Enterprise features needed for this demo).
- Run via Docker Desktop locally using a `docker-compose.yml` (not manual `docker run`), so ports, auth, and volumes are reproducible.
- Expose:
  - `7474` — Neo4j Browser (HTTP)
  - `7687` — Bolt (driver connections from backend)
- Auth: set `NEO4J_AUTH=neo4j/<password>` via env var (no default/blank passwords).
- Persist data with a named Docker volume (e.g. `neo4j_data:/data`) so seeded data survives container restarts.
- Seed synthetic banking data (customers, accounts, transactions, fraud rings) via a Cypher script or small seed script run after the container is healthy — not baked into the image.
- Cap seed data at **no more than 50 accounts** total, so the graph stays small enough to inspect manually in the Neo4j Browser and render clearly in the frontend.
- Simulate fraud using **circular transaction chains** (e.g. Account A → B → C → ... → A, money cycling back to its origin) as the fraud pattern to detect — a well-known money-laundering signature and a natural fit for graph traversal/cycle detection.

## API layer: FastAPI

- A Python FastAPI service sits between Neo4j and the React frontend; the frontend never talks to Neo4j directly.
- Use `uv` for dependency management (`uv add fastapi`, `uv add neo4j`, run with `uv run`).
- Use the official Neo4j Python driver with plain Cypher queries (no ORM) — consistent with the plain-Cypher learning goal above.
- Initial API contract:
  - `GET /fraud-rings` — returns the detected circular transaction chains (nodes + edges) for the frontend to render.
  - Additional endpoints (e.g. full graph, single account lookup) can be added incrementally as needed.

## Frontend: graph visualization

- Use **Cytoscape.js** (via the `react-cytoscapejs` wrapper) to render the graph — free and open source (MIT license), with built-in layouts (circle, breadthfirst, concentric) well suited to highlighting cyclic fraud rings.
- Frontend calls `GET /fraud-rings` on the FastAPI backend and renders the returned nodes/edges.

## Graph Data Science (GDS) demo

- Install the Neo4j Graph Data Science library plugin (free Community tier — PageRank and community detection (Louvain or Label Propagation) are both available at no cost, no Enterprise license needed).
- Demo PageRank (e.g. to surface influential/high-activity accounts) and community detection (e.g. to surface clusters of tightly connected accounts) — run via Cypher in the Neo4j Browser first, with results explained, before considering whether to surface them through the API.

## Docker: all three services

- `docker-compose.yml` defines three services, all running locally on Docker Desktop:
  - `neo4j` — the database (as specified above).
  - `backend` — the FastAPI service, `depends_on: neo4j`.
  - `frontend` — the React app (built and served, e.g. via Vite preview or a static server), `depends_on: backend`.

## Build order

Work through these incrementally, validating each before moving to the next:

- **Phase 1: Neo4j on Docker** — compose file, ports, auth, volume; confirm Browser + Bolt are reachable.
- **Phase 2: Data model + seed script** — design accounts/customers/transactions schema, seed ≤50 accounts including circular fraud chains; inspect in Neo4j Browser.
- **Phase 3: FastAPI backend** — wire the Neo4j driver, implement `GET /fraud-rings`.
- **Phase 4: React frontend** — Cytoscape.js integration, fetch and render `/fraud-rings`.
- **Phase 5: GDS demo** — install GDS plugin, run PageRank and community detection in Browser, explain results.
- **Phase 6: Dockerize backend + frontend** and wire the full three-service `docker-compose.yml`.

# graphdemo

Demo app: graph-based fraud detection in banking, backed by Neo4j, visualized in React.
See [Planning/PLAN.md](Planning/PLAN.md) for the original spec.

## Target architecture (per plan)
- Neo4j 5 Community Edition (`neo4j:5-community`), run via `docker-compose.yml` on Docker Desktop. Ports 7474 (Browser) / 7687 (Bolt), auth via `NEO4J_AUTH` env var, data on a named volume. Seeded with synthetic banking data (accounts, transactions, customers, fraud rings) via a seed script after container is healthy.
- Backend: FastAPI (Python, managed with `uv`), talks to Neo4j via the official driver with plain Cypher (no ORM), exposes `GET /fraud-rings` to the frontend.
- Frontend: React (Vite), renders the graph visually with Cytoscape.js.
- Neo4j, backend, and frontend all run in Docker via one `docker-compose.yml` (see Build order in [Planning/PLAN.md](Planning/PLAN.md)).

## Current state
All 6 build-order phases (see [Planning/PLAN.md](Planning/PLAN.md)) are complete:
- **Phase 1:** Neo4j running via `docker-compose.yml`. Password lives in local `.env` (gitignored; see `.env.example`).
- **Phase 2:** `backend/src/backend/seed.py` seeds 50 customers/accounts and `TRANSFER` relationships, including two circular fraud rings (normal transfers are constructed as a DAG so they can't accidentally form cycles).
- **Phase 3:** FastAPI `GET /fraud-rings` (`backend/src/backend/main.py`, `fraud_rings.py`) detects cycles via Cypher and dedupes rotations.
- **Phase 4:** `frontend/src/App.jsx` fetches `/fraud-rings` and renders it with `react-cytoscapejs`. Note: `main.jsx` deliberately does not use `React.StrictMode` — it breaks `react-cytoscapejs`'s instance lifecycle in dev.
- **Phase 5:** Neo4j GDS plugin enabled (`docker-compose.yml`). PageRank and Louvain were both tried against the seeded graph and neither cleanly isolates the fraud rings (PageRank favors DAG sink accounts; Louvain hits modularity's resolution limit and fragments the rings) — the dedicated cycle-detection query is what actually powers `/fraud-rings`.
- **Phase 6:** `backend/Dockerfile` and `frontend/Dockerfile` (multi-stage, served by nginx) added; full stack runs via `docker compose up -d --build`.
- Git repo initialized at the project root (`main` branch).

## Frontend
- Package manager: npm (package-lock.json present).
- Commands: `npm run dev`, `npm run build`, `npm run lint`, `npm run preview` (run from `frontend/`).
- Plain JS (JSX), no TypeScript.

## Backend
- Package manager: `uv` (never pip). Commands run from `backend/`, e.g. `uv run python -m backend.seed`.
- Neo4j connection: `bolt://localhost:7687`, credentials from the project-root `.env` (`NEO4J_PASSWORD`).

## Notes
- Nothing here should be treated as done until it exists in code — the plan is aspirational.

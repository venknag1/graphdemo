# graphdemo

Demo app: graph-based fraud detection in banking, backed by Neo4j, visualized in React.
See [Planning/PLAN.md](Planning/PLAN.md) for the original spec.

## Target architecture (per plan)
- Neo4j 5 Community Edition (`neo4j:5-community`), run via `docker-compose.yml` on Docker Desktop. Ports 7474 (Browser) / 7687 (Bolt), auth via `NEO4J_AUTH` env var, data on a named volume. Seeded with synthetic banking data (accounts, transactions, customers, fraud rings) via a seed script after container is healthy.
- Backend: FastAPI (Python, managed with `uv`), talks to Neo4j via the official driver with plain Cypher (no ORM), exposes `GET /fraud-rings` to the frontend.
- Frontend: React (Vite), renders the graph visually with Cytoscape.js.
- Neo4j, backend, and frontend all run in Docker via one `docker-compose.yml` (see Build order in [Planning/PLAN.md](Planning/PLAN.md)).

## Current state
- **Phase 1 done:** Neo4j running via `docker-compose.yml` at the project root; Bolt (7687) and Browser (7474) verified reachable. Password lives in local `.env` (gitignored; see `.env.example`).
- **Phase 2 done:** `backend/` is a `uv`-managed Python project. `backend/src/backend/seed.py` seeds 50 customers/accounts and `TRANSFER` relationships into Neo4j, including two circular fraud rings — verified via cypher-shell cycle-detection queries.
- **Phase 3 (FastAPI `/fraud-rings` endpoint) not yet built.**
- `frontend/` — still the default Vite + React 19 template (App.jsx untouched); Cytoscape.js integration not yet built.
- Git repo initialized at the project root (`main` branch, local commits so far).

## Frontend
- Package manager: npm (package-lock.json present).
- Commands: `npm run dev`, `npm run build`, `npm run lint`, `npm run preview` (run from `frontend/`).
- Plain JS (JSX), no TypeScript.

## Backend
- Package manager: `uv` (never pip). Commands run from `backend/`, e.g. `uv run python -m backend.seed`.
- Neo4j connection: `bolt://localhost:7687`, credentials from the project-root `.env` (`NEO4J_PASSWORD`).

## Notes
- Nothing here should be treated as done until it exists in code — the plan is aspirational.

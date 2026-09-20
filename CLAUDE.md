# graphdemo

Demo app: graph-based fraud detection in banking, backed by Neo4j, visualized in React.
See [Planning/PLAN.md](Planning/PLAN.md) for the original spec.

## Target architecture (per plan, not yet built)
- Neo4j 5 Community Edition (`neo4j:5-community`), run via `docker-compose.yml` on Docker Desktop. Ports 7474 (Browser) / 7687 (Bolt), auth via `NEO4J_AUTH` env var, data on a named volume. Seeded with synthetic banking data (accounts, transactions, customers, fraud rings) via Cypher script after container is healthy.
- Backend: not yet chosen/created. Talks to Neo4j, exposes API to frontend.
- Frontend: React (Vite), renders the graph visually (e.g. accounts/transactions as nodes/edges).
- Backend and frontend both run in Docker.

## Current state
- `frontend/` — Vite + React 19 scaffold, still default template (App.jsx untouched). No backend, no Docker, no Neo4j setup yet.
- No git repo initialized at the project root yet.

## Frontend
- Package manager: npm (package-lock.json present).
- Commands: `npm run dev`, `npm run build`, `npm run lint`, `npm run preview` (run from `frontend/`).
- Plain JS (JSX), no TypeScript.

## Notes
- Nothing here should be treated as done until it exists in code — the plan is aspirational.

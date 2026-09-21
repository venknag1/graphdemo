# graphdemo

A demo of graph-based fraud detection in banking: synthetic accounts and
transactions in Neo4j, with a React frontend that visualizes circular
transaction chains (a common money-laundering pattern) as a graph.

Also a personal project to learn Neo4j and Cypher along the way — see
[Planning/PLAN.md](Planning/PLAN.md) for the original spec and learning goals.

## Architecture

- **Neo4j 5 Community** — graph database, seeded with 50 synthetic
  accounts/customers and transfers, including two deliberate fraud rings
  (circular chains of transfers that loop back to their origin).
- **FastAPI backend** (`backend/`) — plain Cypher via the official Neo4j
  driver (no ORM), exposes `GET /fraud-rings`, which detects the circular
  chains via a graph cycle-detection query.
- **React frontend** (`frontend/`) — fetches `/fraud-rings` and renders it
  with Cytoscape.js.
- All three run as Docker containers via one `docker-compose.yml`.

## Running it

```
cp .env.example .env   # set your own NEO4J_PASSWORD
docker compose up -d --build
```

- Frontend: http://localhost:3000
- Neo4j Browser: http://localhost:7474
- Backend API: http://localhost:8000/fraud-rings

First run only, seed the database:

```
cd backend
uv run python -m backend.seed
```

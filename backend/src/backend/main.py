"""FastAPI app exposing the fraud-ring graph to the frontend."""

from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import get_driver
from backend.fraud_rings import find_fraud_rings
from backend.similarity import find_similar_accounts

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["GET"],
)
driver = get_driver()


@app.get("/fraud-rings")
def get_fraud_rings():
    with driver.session() as session:
        return {"rings": find_fraud_rings(session)}


@app.get("/accounts")
def get_accounts():
    with driver.session() as session:
        result = session.run("MATCH (a:Account) RETURN a.id AS id")
        ids = [r["id"] for r in result]
        return {"accounts": sorted(ids, key=lambda x: int(x.removeprefix("acct-")))}


@app.get("/similar-accounts/{account_id}")
def get_similar_accounts(account_id: str, metric: Literal["cosine", "euclidean"] = "cosine"):
    with driver.session() as session:
        similar = find_similar_accounts(session, account_id, metric)
        return {"account": account_id, "metric": metric, "similar": similar}

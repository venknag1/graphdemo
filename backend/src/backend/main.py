"""FastAPI app exposing the fraud-ring graph to the frontend."""

from fastapi import FastAPI

from backend.db import get_driver
from backend.fraud_rings import find_fraud_rings

app = FastAPI()
driver = get_driver()


@app.get("/fraud-rings")
def get_fraud_rings():
    with driver.session() as session:
        return {"rings": find_fraud_rings(session)}

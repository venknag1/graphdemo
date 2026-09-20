"""FastAPI app exposing the fraud-ring graph to the frontend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import get_driver
from backend.fraud_rings import find_fraud_rings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
)
driver = get_driver()


@app.get("/fraud-rings")
def get_fraud_rings():
    with driver.session() as session:
        return {"rings": find_fraud_rings(session)}

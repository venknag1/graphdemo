"""Neo4j driver connection, shared by the API and seed script."""

import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
USER = "neo4j"
PASSWORD = os.environ["NEO4J_PASSWORD"]


def get_driver():
    return GraphDatabase.driver(URI, auth=(USER, PASSWORD))

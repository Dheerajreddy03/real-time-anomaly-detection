from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()

# Connect to Elasticsearch (Docker)
es = Elasticsearch("http://localhost:9200")

@app.get("/")
def root():
    return {"message": "Real-time Anomaly Detection API running"}

@app.get("/anomalies")
def get_anomalies(limit: int = 10):
    response = es.search(
        index="anomalies",
        size=limit,
        sort="timestamp:desc"
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]

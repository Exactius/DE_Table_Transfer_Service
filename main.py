from fastapi import FastAPI
from src.router.transfer_router import router as transfer_router

app = FastAPI(
    title="BigQuery to GCS Transfer Service",
    description="A service for transferring and optionally hashing BigQuery tables to GCS.",
    version="1.0.0",
)

app.include_router(transfer_router)

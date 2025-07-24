import os
import logging
from fastapi import FastAPI
from src.router.transfer_router import router as transfer_router
import uvicorn


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

app = FastAPI(
    title="BigQuery to GCS Transfer Service",
    description="A service for transferring and optionally hashing BigQuery tables to GCS.",
    version="1.0.0",
)

app.include_router(transfer_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

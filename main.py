import os
from fastapi import FastAPI
from src.router.transfer_router import router as transfer_router
import uvicorn

app = FastAPI(
    title="BigQuery to GCS Transfer Service",
    description="A service for transferring and optionally hashing BigQuery tables to GCS.",
    version="1.0.0",
)

app.include_router(transfer_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

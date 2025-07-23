from pydantic import BaseModel
from typing import List, Optional


class BigQueryRequest(BaseModel):
    project_id: str
    dataset: str
    table: str


class GoogleCloudStorageRequest(BaseModel):
    project_id: str
    bucket: str
    filename: str


class Hashing(BaseModel):
    columns: List[str]


class TransferRequest(BaseModel):
    bigquery: BigQueryRequest
    gcs: GoogleCloudStorageRequest
    hashing: Optional[Hashing] = None

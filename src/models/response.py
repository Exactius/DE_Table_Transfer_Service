from pydantic import BaseModel
from typing import Optional


class TransferResponse(BaseModel):
    success: bool
    message: str
    rows_transferred: Optional[int] = None
    file_size_bytes: Optional[int] = None
    gcs_uri: Optional[str] = None

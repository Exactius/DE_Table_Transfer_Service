from fastapi import APIRouter, Depends
from src.models.request import TransferRequest
from src.models.response import TransferResponse
from src.service.transfer_service import TransferService
from src.client.bigquery_client import BigQueryClient
from src.client.gcs_client import GoogleCloudStorageClient

router = APIRouter(prefix="/api/v1", tags=["data-transfer"])


def get_bq_client(request: TransferRequest) -> BigQueryClient:
    return BigQueryClient(request.bigquery.project_id)


def get_gcs_client(request: TransferRequest) -> GoogleCloudStorageClient:
    return GoogleCloudStorageClient(request.gcs.project_id)


def get_transfer_service(
    request: TransferRequest,
    bq_client: BigQueryClient = Depends(get_bq_client),
    gcs_client: GoogleCloudStorageClient = Depends(get_gcs_client)
) -> TransferService:
    return TransferService(bq_client, gcs_client)


@router.post("/bigquery-to-gcs", response_model=TransferResponse)
async def transfer_bigquery_table_to_gcs(
    request: TransferRequest,
    service: TransferService = Depends(get_transfer_service)
) -> TransferResponse:
    return await service.transfer_table(request)
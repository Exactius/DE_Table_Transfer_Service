from src.client.bigquery_client import BigQueryClient
from src.client.gcs_client import GoogleCloudStorageClient
from src.models.request import TransferRequest
from src.models.response import TransferResponse
from src.utils.hashing import hash_dataframe_columns, validate_columns_exist


class TransferService:
    def __init__(self, bq_client: BigQueryClient, gcs_client: GoogleCloudStorageClient):
        self.bq_client = bq_client
        self.gcs_client = gcs_client

    async def transfer_table(self, request: TransferRequest) -> TransferResponse:
        try:
            df = self.bq_client.extract_table_to_dataframe(
                request.bigquery.dataset, request.bigquery.table
            )

            if request.hashing:
                missing_columns = validate_columns_exist(df, request.hashing.columns)
                if missing_columns:
                    return TransferResponse(
                        success=False,
                        message=f"Columns not found in data: {missing_columns}",
                    )

                df = hash_dataframe_columns(df, request.hashing.columns)

            upload_result = self.gcs_client.upload_dataframe_as_csv(
                df, request.gcs.bucket, request.gcs.filename
            )

            return TransferResponse(
                success=True,
                message="Transfer completed successfully",
                rows_transferred=upload_result["rows_count"],
                file_size_bytes=upload_result["file_size_bytes"],
                gcs_uri=upload_result["gcs_uri"],
            )

        except Exception as e:
            return TransferResponse(success=False, message=f"Transfer failed: {str(e)}")

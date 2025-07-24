from google.cloud import storage
import pandas as pd
import logging
from io import StringIO
from typing import Dict, Any

logger = logging.getLogger(__name__)


class GoogleCloudStorageClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = storage.Client(project=project_id)
        logger.info(f"GCS client initialized for project: {project_id}")

    def upload_dataframe_as_csv(
        self,
        dataframe: pd.DataFrame,
        bucket_name: str,
        filename: str,
        folder: str = None,
    ) -> Dict[str, Any]:
        full_path = f"{folder}/{filename}" if folder else filename

        logger.info(f"Starting upload to GCS: gs://{bucket_name}/{full_path}")
        logger.debug(f"DataFrame shape: {dataframe.shape}")

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(full_path)

        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        file_size = len(csv_data.encode("utf-8"))
        logger.debug(f"CSV data size: {file_size} bytes")

        blob.upload_from_string(csv_data, content_type="text/csv")
        logger.info(f"Upload completed successfully to gs://{bucket_name}/{full_path}")

        return {
            "gcs_uri": f"gs://{bucket_name}/{full_path}",
            "file_size_bytes": file_size,
            "rows_count": len(dataframe),
        }

    def check_bucket_exists(self, bucket_name: str) -> bool:
        logger.info(f"Checking if bucket exists: {bucket_name}")
        try:
            self.client.get_bucket(bucket_name)
            logger.info(f"Bucket {bucket_name} exists")
            return True
        except Exception as e:
            logger.warning(
                f"Bucket {bucket_name} not found or not accessible: {str(e)}"
            )
            return False

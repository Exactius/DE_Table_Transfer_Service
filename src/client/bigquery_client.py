from google.cloud import bigquery
import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class BigQueryClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        logger.info(f"BigQuery client initialized for project: {project_id}")

    def extract_table_to_dataframe(self, dataset: str, table: str) -> pd.DataFrame:
        logger.info(f"Starting data extraction from BigQuery table: {self.project_id}.{dataset}.{table}")
        query = f"SELECT * FROM `{self.project_id}.{dataset}.{table}`"
        logger.debug(f"Executing query: {query}")
        
        df = self.client.query(query).to_dataframe()
        logger.info(f"Data extraction completed. Rows extracted: {len(df)}")
        return df

    def get_table_info(self, dataset: str, table: str) -> Dict[str, Any]:
        logger.info(f"Getting table info for: {self.project_id}.{dataset}.{table}")
        table_ref = self.client.dataset(dataset).table(table)
        table = self.client.get_table(table_ref)

        response = {
            "num_rows": table.num_rows,
            "num_bytes": table.num_bytes,
            "schema": [
                {"name": field.name, "type": field.field_type} for field in table.schema
            ],
        }
        logger.info(f"Table info retrieved - Rows: {table.num_rows}, Bytes: {table.num_bytes}")
        return response

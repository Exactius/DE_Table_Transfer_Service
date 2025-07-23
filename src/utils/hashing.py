import hashlib
import pandas as pd
import logging
from typing import List

logger = logging.getLogger(__name__)


def hash_dataframe_columns(
    df: pd.DataFrame, columns_to_hash: List[str]
) -> pd.DataFrame:
    logger.info(f"Starting hashing process for columns: {columns_to_hash}")
    df_copy = df.copy()

    for column in columns_to_hash:
        if column in df_copy.columns:
            logger.debug(f"Hashing column: {column}")
            df_copy[column] = (
                df_copy[column]
                .astype(str)
                .apply(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
            )
            logger.debug(f"Column {column} hashed successfully")

    logger.info(f"Hashing completed for {len(columns_to_hash)} columns")
    return df_copy


def validate_columns_exist(df: pd.DataFrame, columns: List[str]) -> List[str]:
    logger.info(f"Validating columns exist: {columns}")
    missing_columns = [col for col in columns if col not in df.columns]

    if missing_columns:
        logger.warning(f"Missing columns found: {missing_columns}")
    else:
        logger.info("All columns exist in DataFrame")

    return missing_columns

import os
from from_root import from_root
from pathlib import Path

## file names

FILE_NAME: str = "covertype.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: Path = os.path.join("config", "schema.yaml")


ARTIFACT_DIR = os.path.join(from_root(), "artifacts")

## Data Ingestion

DATA_INGESTION_DIR: str = "DataIngestion"
DATA_INGESTION_FEATURE_STORE: str = "feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT: float = 0.2


## Data Validation

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME: str = "report.yaml"

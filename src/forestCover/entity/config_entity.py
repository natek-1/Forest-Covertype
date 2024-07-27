from dataclasses import dataclass
from from_root import from_root
import os
from pathlib import Path
from forestCover.constants import (ARTIFACT_DIR, DATA_INGESTION_DIR, DATA_INGESTION_FEATURE_STORE, TRAIN_FILE_NAME,
                                    TEST_FILE_NAME, DATA_INGESTION_TRAIN_TEST_SPLIT, DATA_VALIDATION_DIR_NAME,
                                    DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME)


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: Path = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR)
    feature_store_path: Path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE)
    train_file_path: Path = os.path.join(data_ingestion_dir, TRAIN_FILE_NAME)
    test_file_path: Path = os.path.join(data_ingestion_dir, TEST_FILE_NAME)
    train_test_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT

@dataclass
class DataValidationConfig:
    data_validation_dir: Path = os.path.join(from_root(), DATA_VALIDATION_DIR_NAME)
    data_validation_drift_file: Path = os.path.join(data_validation_dir, DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME)
    

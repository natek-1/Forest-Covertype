import os
from from_root import from_root
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

## file names
TARGET_COLUMN = "Cover_Type"
FILE_NAME: str = "covertype.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: Path = os.path.join("config", "schema.yaml")
PREPROCESSING_FILE_NAME = "preprocessor.pkl"


ARTIFACT_DIR = os.path.join(from_root(), "artifacts")

## Data Ingestion

DATA_INGESTION_DIR: str = "DataIngestion"
DATA_INGESTION_FEATURE_STORE: str = "feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT: float = 0.2


## Data Validation

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME: str = "report.yaml"

## Data Transformation

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test.npy"

## Model Trainer
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_FILE_NAME: str = "model.pkl"
MODEL_MIN_SCORE: float = 0.7
MODEL_TRAINER_CONFIG_PATH: Path = os.path.join("config", "model.yaml")


# Model Evaluation

MODEL_EVALUATION_SCORE_CHANGE: float = 0.02
MODEL_PUSHER_BUCKET_NAME: str = os.getenv("BUCKET_NAME")
MODEL_PUSHER_S3_KEY: str = "model-registry"

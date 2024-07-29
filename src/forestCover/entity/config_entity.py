from dataclasses import dataclass
import os
from pathlib import Path
from forestCover.constants import (ARTIFACT_DIR, DATA_INGESTION_DIR, DATA_INGESTION_FEATURE_STORE, TRAIN_FILE_NAME,
                                    TEST_FILE_NAME, DATA_INGESTION_TRAIN_TEST_SPLIT, DATA_VALIDATION_DIR_NAME,
                                    DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME,
                                    DATA_TRANSFORMATION_DIR_NAME, DATA_TRANSFORMATION_TEST_FILE_NAME, DATA_TRANSFORMATION_TRAIN_FILE_NAME, PREPROCESSING_FILE_NAME,
                                    MODEL_TRAINER_DIR_NAME, MODEL_FILE_NAME, MODEL_TRAINER_CONFIG_PATH, MODEL_MIN_SCORE,
                                    MODEL_EVALUATION_SCORE_CHANGE, MODEL_PUSHER_BUCKET_NAME, MODEL_PUSHER_S3_KEY)


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: Path = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR)
    feature_store_path: Path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE)
    train_file_path: Path = os.path.join(data_ingestion_dir, TRAIN_FILE_NAME)
    test_file_path: Path = os.path.join(data_ingestion_dir, TEST_FILE_NAME)
    train_test_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT

@dataclass
class DataValidationConfig:
    data_validation_dir: Path = os.path.join(ARTIFACT_DIR, DATA_VALIDATION_DIR_NAME)
    data_validation_drift_file: Path = os.path.join(data_validation_dir, DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_dir: Path = os.path.join(ARTIFACT_DIR, DATA_TRANSFORMATION_DIR_NAME)
    data_transformation_train_file_path: Path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRAIN_FILE_NAME)
    data_transformation_test_file_path: Path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TEST_FILE_NAME)
    preprocessor_file_path: Path = os.path.join(data_transformation_dir, PREPROCESSING_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: Path = os.path.join(ARTIFACT_DIR, MODEL_TRAINER_DIR_NAME)
    model_path: Path = os.path.join(model_trainer_dir, MODEL_FILE_NAME)
    min_score: float = MODEL_MIN_SCORE
    model_config_path: Path = MODEL_TRAINER_CONFIG_PATH

@dataclass
class ModelEvaluationConfig:
    score_change_threshold: float = MODEL_EVALUATION_SCORE_CHANGE
    bucket_name: str = MODEL_PUSHER_BUCKET_NAME
    s3_key: str = MODEL_PUSHER_S3_KEY

@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_PUSHER_BUCKET_NAME
    s3_model_path: str = MODEL_PUSHER_S3_KEY + "/" + MODEL_FILE_NAME
    
@dataclass
class PredictionPipelineConfig:
    bucket_name: str = MODEL_PUSHER_BUCKET_NAME
    s3_model_path: str = MODEL_PUSHER_S3_KEY + "/" + MODEL_FILE_NAME
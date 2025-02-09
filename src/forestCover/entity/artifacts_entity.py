from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    drift_report_file_path: Path

@dataclass
class DataTransormationArfitact:
    preprocessor_path: Path
    train_file_path: Path
    test_file_path: Path

@dataclass
class ClassificationMetric:
    f1_score: float
    precision: float
    recall: float

@dataclass
class ModelTrainerArtifact:
    model_path: Path
    metric_artifact: ClassificationMetric

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    change_accuracy: float
    best_model_path: str
    trained_model_path: str

@dataclass
class ModelPusherArtifact:
    bucket_name: str
    s3_model_path: str
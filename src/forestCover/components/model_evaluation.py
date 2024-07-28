import sys
from dataclasses import dataclass

from sklearn.metrics import f1_score
import pandas as pd



from forestCover.entity.config_entity import ModelEvaluationConfig
from forestCover.entity.artifacts_entity import DataIngestionArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from forestCover.entity.s3_estimator import ForestEstimator
from forestCover.utils.common import read_yaml, save_json_to_yaml, load_object
from forestCover.constants import TARGET_COLUMN
from forestCover.logger import logging
from forestCover.exception import CustomException

@dataclass
class EvaluationModelResponse:
    trained_model_f1: float
    best_model_f1: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact,
                 model_evaluation_config: ModelEvaluationConfig = ModelEvaluationConfig()):
        self.config = model_evaluation_config
        self.ingestion_artifact = data_ingestion_artifact
        self.trainer_artifact = model_trainer_artifact

    
    def get_best_model(self):
        bucket_name = self.config.bucket_name
        model_path = self.config.s3_key
        estimator = ForestEstimator(bucket_name,
                                    model_path)
        if estimator.is_model_present(model_path):
            return estimator
        return None

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting the process of model evalution")
            test_df = pd.read_csv(self.ingestion_artifact.test_file_path)
            X, y = test_df.drop(columns=[TARGET_COLUMN]), test_df[TARGET_COLUMN]

            trained_model = load_object(self.trainer_artifact.model_path)
            logging.info("got trained model for evaluation")
            y_pred_trained = trained_model.predict(X)
            trained_model_f1 = f1_score(y, y_pred_trained, average="micro")

            best_model_f1 = 0
            best_model = self.get_best_model()
            logging.info("loaded current best model from s3 bucket")

            if best_model is not None:
                y_pred_best = best_model.predict(X)
                best_model_f1 = f1_score(y, y_pred_best, average="micro")
            
            logging.info("all models where evaluted")
            result = ModelEvaluationArtifact(
                trained_model_path=self.trainer_artifact.model_path,
                best_model_path=self.trainer_artifact.model_path,
                change_accuracy=trained_model_f1-best_model_f1,
                is_model_accepted=trained_model_f1>best_model_f1
            )

            logging.info("Done with model Evaluation ")
            return result
        except Exception as e:
            error = CustomException(e, sys)
            logging.info("couldn't upload image")
            return {"Created": False, "Reason": error.error_message}


    

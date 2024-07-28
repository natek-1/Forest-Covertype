import os
import sys


from forestCover.components.data_ingestion import DataIngestion
from forestCover.components.data_validation import DataValidation
from forestCover.components.data_transformation import DataTransformation
from forestCover.components.model_training import ModelTrainer
from forestCover.components.model_evaluation import ModelEvaluation
from forestCover.components.model_pusher import ModelPusher
from forestCover.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact, DataTransormationArfitact, ModelTrainerArtifact
from forestCover.exception import CustomException
from forestCover.logger import logging


class TrainingPipeline:

    def __init__(self):

        self.data_ingestion: DataIngestion = DataIngestion()
        self.data_validation = None
    
    def run_pipeline(self):
        try:
            #data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()

            #self.data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact)
            #data_validation_artifact = self.data_validation.initial_data_validation()
            #data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact)
            #data_transformation_artifact = data_transformation.initiate_data_transformation()
            #model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact)
            #model_trainer_artifact = model_trainer.initiate_model_training()
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path="artifacts/DataIngestion/train.csv",
                test_file_path="artifacts/DataIngestion/test.csv"
            )
            model_trainer_artifact = ModelTrainerArtifact(
                model_path="artifacts/model_trainer/model.pkl",
                metric_artifact=None
            )
            model_evaluation = ModelEvaluation(data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            model_pusher = ModelPusher(model_trainer_artifact=model_trainer_artifact)
            model_pusher_arfifact = model_pusher.initiate_model_pusher()
            print(model_pusher_arfifact)

        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
        
if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()       
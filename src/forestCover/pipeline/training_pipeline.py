import os
import sys


from forestCover.components.data_ingestion import DataIngestion
from forestCover.components.data_validation import DataValidation
from forestCover.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from forestCover.exception import CustomException
from forestCover.logger import logging


class TrainingPipeline:

    def __init__(self):

        self.data_ingestion: DataIngestion = DataIngestion()
        self.data_validation = None
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()

            self.data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = self.data_validation.initial_data_validation()

            

        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
        
if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()       
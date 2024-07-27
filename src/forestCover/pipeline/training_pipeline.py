import os
import sys


from forestCover.components.data_ingestion import DataIngestion
from forestCover.entity.artifacts_entity import DataIngestionArtifact
from forestCover.exception import CustomException
from forestCover.logger import logging


class TrainingPipeline:

    def __init__(self):

        self.data_ingestion: DataIngestion = DataIngestion()
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            logging.info("done running ingestion")
        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
        
if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()       
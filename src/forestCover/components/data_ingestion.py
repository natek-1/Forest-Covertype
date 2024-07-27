import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from forestCover.entity.config_entity import DataIngestionConfig
from forestCover.entity.artifacts_entity import DataIngestionArtifact
from forestCover.utils.common import read_yaml
from forestCover.data_access.forest_data import ForestData
from forestCover.constants import SCHEMA_FILE_PATH
from forestCover.exception import CustomException
from forestCover.logger import logging


class DataIngestion:

    def __init__(self, config: DataIngestionConfig = DataIngestionConfig()):
        self.config = config

    def export_data_to_feature_store(self) -> pd.DataFrame:
        try:

            logging.info("Exporting Data From Mongo DB")
            forest_data = ForestData()
            df = forest_data.export_collection_as_df()
            logging.info(f"Data frame exported with the following shape: {df.shape}")


            dirpath = os.path.dirname(self.config.feature_store_path)
            os.makedirs(dirpath, exist_ok=True)
            df.to_csv(self.config.feature_store_path, index=False, header=True)
            logging.info(f"Saved feature store to the following path {self.config.feature_store_path}")

            return df

        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
    
    def split_data(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df, test_size=self.config.train_test_ratio, random_state=42)

            logging.info("the data was split into train and test set")

            dir_name = os.path.dirname(self.config.train_file_path)
            os.makedirs(dir_name, exist_ok=True)
            train_set.to_csv(self.config.train_file_path, index=False, header=True)


            dir_name = os.path.dirname(self.config.test_file_path)
            os.makedirs(dir_name, exist_ok=True)
            test_set.to_csv(self.config.test_file_path, index=False, header=True)

            logging.info(f"both the training the testing data were saved at {self.config.train_file_path} and {self.config.test_file_path} respectively")

        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting Data Ingestion step")

            df = self.export_data_to_feature_store()
            _schema_config = read_yaml(path_to_yaml=SCHEMA_FILE_PATH)
            df = df.drop(columns=_schema_config["drop_columns"])
            self.split_data(df)

            artifact = DataIngestionArtifact(trained_file_path=self.config.train_file_path, 
                                  test_file_path=self.config.test_file_path)

            logging.info("Done Data Ingestoin component")
            return artifact
        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
        
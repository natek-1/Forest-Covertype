import os
import sys
import json
from typing import List, Tuple

import pandas as pd
from pathlib import Path
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection



from forestCover.entity.config_entity import DataValidationConfig
from forestCover.entity.artifacts_entity import DataValidationArtifact, DataIngestionArtifact
from forestCover.constants import ARTIFACT_DIR, DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME, SCHEMA_FILE_PATH

from forestCover.utils.common import read_yaml, save_json_to_yaml
from forestCover.logger import logging
from forestCover.exception import CustomException

class DataValidation:
    
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig = DataValidationConfig()):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.config = data_validation_config
        self._schema_file = read_yaml(SCHEMA_FILE_PATH)

    
    def validate_column_number(self, dataframe: pd.DataFrame) -> bool:
        status = len(dataframe.columns) == len(self._schema_file["columns"])
        logging.info(f"Is numer of column required present, Status: {status}")
        return status
    

    def numeric_column_exit(self, df:pd.DataFrame) -> Tuple[bool, List[str]]:
        df_columns = df.columns
        status = True
        missing_columns = []
        for column in self._schema_file["numerical_columns"]:
            if column not in df_columns:
                missing_columns.append(column)
                status = False

        logging.info(f"Missing the following column: {missing_columns}")
        return status, missing_columns


    def detect_dataset_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame):
        data_drift_profile = Profile(sections=[DataDriftProfileSection()])

        data_drift_profile.calculate(reference_df, current_df)

        report = data_drift_profile.json()
        json_report = json.loads(report)

        dirpath = os.path.dirname(self.config.data_validation_dir)
        os.makedirs(dirpath, exist_ok=True)

        save_json_to_yaml(self.config.data_validation_drift_file, json_report)

        n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
        n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

        logging.info(f"{n_drifted_features}/{n_features} drift detected.")
        drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
        return drift_status



    
    def initial_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validaition step")
            validation_message = ""


            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # making sure the rright number of columns are present
            status = self.validate_column_number(dataframe=train_df)
            if not status:
                validation_message += "Columns are missing in train dataframe"


            status = self.validate_column_number(dataframe=test_df)
            if not status:
                validation_message += "Columns are missing in test dataframe"


            # making sure the required columns exits
            status, missing_columns = self.numeric_column_exit(train_df)
            if not status:
                validation_message += f"Columns are missing in train dataframe: {missing_columns}"
            status, missing_columns = self.numeric_column_exit(test_df)
            if not status:
                validation_message += f"Columns are missing in test dataframe: {missing_columns}"
            
            if len(validation_message) == 0:
                # check for drift
                status = self.detect_dataset_drift(train_df, test_df)
                if status:
                    logging.info("Data Dift detections")
            else:
                logging.info(validation_message)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status= len(validation_message) == 0 and status,
                message=validation_message,
                drift_report_file_path=self.config.data_validation_drift_file
            )
            logging.info("Done running Data Validation step")
            return data_validation_artifact


        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
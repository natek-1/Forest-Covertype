import sys
import os

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN


from forestCover.entity.config_entity import DataTransformationConfig
from forestCover.entity.artifacts_entity import DataIngestionArtifact, DataTransormationArfitact
from forestCover.constants import SCHEMA_FILE_PATH, TARGET_COLUMN
from forestCover.exception import CustomException
from forestCover.logger import logging
from forestCover.utils.common import save_to_pickle,  save_numpy_array, read_yaml


class DataTransformation:
    
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig = DataTransformationConfig()):
        self.config = data_transformation_config
        self.arftifact = data_ingestion_artifact
        os.makedirs(self.config.data_transformation_dir, exist_ok=True)
    

    def get_transformation_object(self):

        _schema_config = read_yaml(SCHEMA_FILE_PATH)
        numeric_features = _schema_config["numerical_columns"]
        numeric_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ])

        preprocessor = ColumnTransformer([
            ("Numeric_Pipeline", numeric_pipeline, numeric_features)
        ])
        logging.info("created preprocessor object")
        return preprocessor
    

    def initiate_data_transformation(self) -> DataTransormationArfitact:
        try:
            logging.info("Starting the Data Transformatoin step")
            preprocessor = self.get_transformation_object()

            train_df = pd.read_csv(self.arftifact.trained_file_path)
            test_df = pd.read_csv(self.arftifact.test_file_path)

            input_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_train = train_df[TARGET_COLUMN]

            input_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_test = test_df[TARGET_COLUMN]
            logging.info("seperate infor from train and test df")

            input_train_arr = preprocessor.fit_transform(input_train_df)
            input_test_arr = preprocessor.transform(input_test_df)

            save_to_pickle(preprocessor,
                           self.config.preprocessor_file_path)

            smt = SMOTEENN(sampling_strategy='minority', random_state=42)

            input_train_arr, target_train = smt.fit_resample(
                input_train_arr, target_train
            )

            input_test_arr, target_test = smt.fit_resample(
                input_test_arr, target_test
            )

            logging.info("the sample in the dataset were sampled on both train and test set")

            train_arr = np.c_[input_train_arr, np.array(target_train)]
            test_arr = np.c_[input_test_arr, np.array(target_test)]

            save_numpy_array(train_arr, self.config.data_transformation_train_file_path)
            save_numpy_array(test_arr, self.config.data_transformation_test_file_path)
            logging.info(f"all object where saved to {self.config.data_transformation_dir}")

            data_transformation_artifact = DataTransormationArfitact(
                preprocessor_path=self.config.preprocessor_file_path,
                train_file_path=self.config.data_transformation_train_file_path,
                test_file_path=self.config.data_transformation_test_file_path
            )

            logging.info("Done with Data Transformation Stage")
            return data_transformation_artifact
        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
import os
import sys

import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score
from neuro_mf import ModelFactory


from forestCover.entity.config_entity import ModelTrainerConfig
from forestCover.entity.artifacts_entity import ModelTrainerArtifact, ClassificationMetric, DataTransormationArfitact
from forestCover.constants import SCHEMA_FILE_PATH
from forestCover.entity.estimator import ForestModel

from forestCover.utils.common import read_yaml, save_json_to_yaml, read_yaml, load_numpy_array, load_object, save_to_pickle
from forestCover.logger import logging
from forestCover.exception import CustomException


class ModelTrainer:

    def __init__(self, data_transformation_artifact: DataTransormationArfitact,
                        model_trainer_config: ModelTrainerConfig = ModelTrainerConfig()):
        self.config = model_trainer_config
        self.artifact = data_transformation_artifact
        os.makedirs(self.config.model_trainer_dir, exist_ok=True)

    
    def get_model_and_report(self, train: np.array, test:np.array) :
        model_factory = ModelFactory(model_config_path=self.config.model_config_path)

        X_train, y_train = train[:,:-1], train[:,-1]
        X_test, y_test = test[:,:-1], test[:,-1]

        best_model_details = model_factory.get_best_model(
            X=X_train, y=y_train, base_accuracy=self.config.min_score
        )


        model_obj =best_model_details.best_model
        y_pred = model_obj.predict(X_test)

        f1 = f1_score(y_test, y_pred, average="micro")
        precision =precision_score(y_test, y_pred, average="micro")
        recall = recall_score(y_test, y_pred, average="micro")

        metric_artiact = ClassificationMetric(f1_score=f1,
                                              precision=precision,
                                              recall=recall)
        return best_model_details, metric_artiact
    

    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            logging.info("started model training")
            train_arr = load_numpy_array(self.artifact.train_file_path)
            test_arr = load_numpy_array(self.artifact.test_file_path)

            best_model, metric_artifact = self.get_model_and_report(train=train_arr, test=test_arr)
            logging.info("done doing hyper parameter tuning")

            if best_model.best_score < self.config.min_score:
                logging.info("Model Score is too low")
                raise Exception("model score not good")
            preprocessor = load_object(self.artifact.preprocessor_path)

            model = ForestModel(preprocessor=preprocessor,
                                trained_model=best_model.best_model)

            logging.info("created model for prediction")
            save_to_pickle(obj=model, file_path=self.config.model_path)
            logging.info(f"saved model at {self.config.model_path}")
            artifact = ModelTrainerArtifact(metric_artifact=metric_artifact,
                                        model_path=self.config.model_path)
            

            logging.info("done with model training")

            return artifact
        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
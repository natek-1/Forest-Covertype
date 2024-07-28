import sys

from pandas import DataFrame

from forestCover.exception import CustomException
from forestCover.logger import logging

class ForestModel:

    def __init__(self, preprocessor, trained_model):
        self.preprocessor = preprocessor
        self.model = trained_model
    
    def predict(self, df: DataFrame) -> DataFrame:
        try:
            transformed = self.preprocessor.transform(df)
            return self.model.predict(transformed)
        except Exception as e:
            error = CustomException(e, sys)
            logging.error(error.error_message)
            raise error
import sys

import pandas as pd

from forestCover.cloud_storage.aws_storage import SimpleStroageService
from forestCover.entity.estimator import ForestModel


class ForestEstimator:

    def __init__(self, bucket_name, model_path):
        self.bucket_name = bucket_name
        self.s3 = SimpleStroageService()
        self.model_path = model_path
        self.model = None
    
    def is_model_present(self, model_path):
        return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
    
    def load_model(self) -> ForestModel:
        return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)

    def save_model(self, from_file, remove=False):
        self.s3.upload_file(from_file,
                            to_filename=self.model_path,
                            bucket_name=self.bucket_name,
                            remove=remove)
    
    def predict(self, dataframe):
        if self.model is None:
            self.model = self.load_model()
        return self.model.predict(dataframe)
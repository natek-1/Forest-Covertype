import sys

import numpy as np
import pandas as pd

from forestCover.entity.config_entity import PredictionPipelineConfig
from forestCover.cloud_storage.aws_storage import SimpleStroageService
from forestCover.entity.s3_estimator import ForestEstimator



class PredictionPipeline:

    def __init__(self, config: PredictionPipelineConfig = PredictionPipelineConfig()):
        self.config = config
        self.s3 = SimpleStroageService()
        self.model = ForestEstimator( bucket_name=self.config.bucket_name,
                                     model_path=self.config.s3_model_path)
    
    def predict(self, dataframe: pd.DataFrame) -> np.ndarray:
        return self.model.predict(dataframe)
    
    
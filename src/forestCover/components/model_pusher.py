import sys


from forestCover.cloud_storage.aws_storage import SimpleStroageService
from forestCover.entity.s3_estimator import ForestEstimator
from forestCover.entity.config_entity import ModelPusherConfig
from forestCover.entity.artifacts_entity import ModelTrainerArtifact, ModelPusherArtifact
from forestCover.logger import logging
from forestCover.exception import CustomException


class ModelPusher:

    def __init__(self, model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig = ModelPusherConfig()):
        self.s3 = SimpleStroageService()
        self.config = model_pusher_config
        self.artifact = model_trainer_artifact
        self.estimator = ForestEstimator(
            bucket_name=self.config.bucket_name,
            model_path=self.config.s3_model_path
        )
    
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Preparing to push to model to s3")

            self.estimator.save_model(from_file=self.artifact.model_path)
            artifact = ModelPusherArtifact(
                bucket_name=self.config.bucket_name,
                s3_model_path=self.config.s3_model_path
            )
            logging.info("Done pushing the model to required locatoin in aws")
            

            logging.info("Done pushing the model to s3 bucket")
            return artifact
        except Exception as e:
            error = CustomException(e, sys)
            logging.info("couldn't upload image")
            return {"Created": False, "Reason": error.error_message}
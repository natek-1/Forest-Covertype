import os
import sys
import json

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection



from forestCover.entity.config_entity import DataValidationConfig
from forestCover.entity.artifacts_entity import DataValidationArtifact
from forestCover.constants import ARTIFACT_DIR, DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_DIR_NAME_DRIFT_REPORT_NAME

from forestCover.utils.common import read_yaml
from forestCover.logger import logging
from forestCover.exception import CustomException

class DataValidation:
    pass
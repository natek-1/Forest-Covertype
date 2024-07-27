
import os
import yaml, json
from typing import Any
from pathlib import Path
import pickle
import numpy as np
import sys


from forestCover.logger import logging
from forestCover.exception import CustomException

def read_yaml(path_to_yaml: Path):
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        e: empty file

    Returns:
        yaml loaded file
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        error = CustomException(e, sys)
        logging.error(error.error_message)
        raise error


def save_json_to_yaml(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    
    # Convert JSON to YAML
    yaml_data = yaml.dump(data, sort_keys=False)

    # Save YAML to file
    with open(path, 'w') as file:
        file.write(yaml_data)

    logging.info(f"json file saved at: {path}")



def save_to_pickle(obj, file_path):
    """
    Save an object to a pickle file.

    Parameters:
    obj: The object to be pickled.
    file_path: The name of the file to save the object.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)


def save_numpy_array(array, file_path):
    """
    Save a NumPy array to a file.

    Parameters:
    array: The NumPy array to be saved.
    file_path: The name of the file to save the array.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    np.save(file_path, array)
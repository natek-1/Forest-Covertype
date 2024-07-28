import sys, os
from  logging import Exception
from io import StringIO
from typing import Union, List

import pickle
import pandas as pd
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientException

from forestCover.logger import logging
from forestCover.exception import CustomException
from forestCover.config.aws_connection import S3Client


class SimpleStroageService:

    def __init__(self):
        self.client = S3Client()
        self.s3_resource = self.client.s3_resource
        self.s3_client = self.client.s3_client

    def s3_key_path_available(self, bucket_name, s3_key)->bool:
        bucket = self.get_bucket(bucket_name)

        for _ in bucket.objects.filter(Prefix=s3_key):
            return True
        return False



    def get_bucket(self, bucket_name):
        return self.s3_resource.Bucket(bucket_name)
    


    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union [StringIO, str]:
        func = (
            lambda: object_name.get()["Body"].read().decode()
            if decode
            else object_name.get()["Body"].read()
        )
        conv_func = lambda: StringIO(func()) if make_readable else func()
        return conv_func()
    
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:
            
            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )

            logging.info(f"uploaded {from_filename} to {to_filename} in bucket: {bucket_name}")

            if remove:
                os.remove(from_filename)
                logging.info(f"the file located at {from_filename} was deleted")
        except Exception as e:
            error = CustomException(e, sys)
            logging.info("couldn't upload image")
            return {"Created": False, "Reason": error.error_message}
    
    def get_file_object(self, file_name: str, bucket_name: str):
        bucket = self.get_bucket(bucket_name)

        file_objects = [file_object for file_object in bucket.objects.filter(Prefix=file_name)]

        func = lambda x: x[0] if len(x) == 0 else x

        return func(file_objects)
    
    def load_model(self, model_name, bucket_name, model_dir= None):
        func = (
            lambda: model_name
            if model_dir is None
            else model_dir + '/' + model_name
        )

        model_file= func()

        file_object = self.get_file_object(model_file, bucket_name)
        model_obj = self.read_object(file_object, decode=False)
        model = pickle.loads(model_obj)
        return model
    

    def create_folder(self, folder_name, bucket_name):
        self.s3_resource.Object(bucket_name, folder_name).load()
        



import pandas as pd
import numpy as np


from forestCover.constants.database import DATABASE_COLLECTION, DATABASE_NAME
from forestCover.config.mongo_db_connection import MongoDBClient


class ForestData:

    def __init__(self, database_name=DATABASE_NAME):
        self.mongo_client = MongoDBClient(database_name)
    
    def export_collection_as_df(self, collection_name: str = DATABASE_COLLECTION) -> pd.DataFrame:

        forest_collection = self.mongo_client.database[collection_name]

        data_from_db = forest_collection.find()
        df_loaded = pd.DataFrame(list(data_from_db))
        df_loaded = df_loaded.drop(columns='_id')


        one_hot_wild = pd.get_dummies(df_loaded['Wilderness_Area'], prefix='Wilderness_Area', prefix_sep='')
        one_hot_wild = one_hot_wild.astype(int)
        one_hot_soil = pd.get_dummies(df_loaded['Soil_Type'], prefix='Soil_Type', prefix_sep='')
        one_hot_soil = one_hot_soil.astype(int)
        df_loaded.drop(columns=['Wilderness_Area', 'Soil_Type'], inplace=True)
        df_loaded[one_hot_soil.columns] = one_hot_soil
        df_loaded[one_hot_wild.columns] = one_hot_wild

        df_loaded = df_loaded.replace({"na": np.nan})

        return df_loaded

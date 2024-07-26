from forestCover.data_access.forest_data import ForestData

data = ForestData()
df = data.export_collection_as_df()
df.columns
import configparser
import os
import sys
import json
import pandas as pd
from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat

# Loading Configuration Values
module_path = os.path.abspath(os.path.join('.'))
sys.path.append(module_path)
config = configparser.ConfigParser()
config.read(module_path+'/config.ini')

PROJECT_ID = config['GCP']['PROJECT_ID']
DATASET_ID = config['GCP']['PROJECT_ID']
GEMINI_MODEL = config['GCP']['GEMINI_MODEL']
BQ_TABLE_LIST = config['GCP']['BQ_TABLE_LIST']
API_KEY = config['GCP']['API_KEY']

#Init 
class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config={'api_key': {API_KEY}, 'model': {GEMINI_MODEL}})

vn = MyVanna()

vn.connect_to_bigquery(project_id='uc-dataanalytics-prd')

def vn_train_pair(question, sql):
    vn.train(
    question=question, 
    sql=sql
    )
    print(f"Calling vn.train with: {question} and {sql}")

def train_schema():
    df_information_schema = vn.run_sql(f"SELECT table_catalog, table_schema, table_name, column_name, data_type, description FROM `uc-dataanalytics-prd.3_REFINED_TI_SAP.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS` WHERE table_name in ('Stock_NonValuated','MaterialMD','PlantsMD')")
    plan = vn.get_training_plan_generic(df_information_schema)
    plan
    vn.train(plan=plan)
    print("Schema Loaded")

def train_pair():
    # Load JSON data
    with open("training/mro.json", "r") as file:
        data = json.load(file)

    # Create a DataFrame from the JSON
    df = pd.DataFrame(data)

    # Iterate over each row and call vn.train
    for index, row in df.iterrows():
        vn_train_pair(question=row["question"], sql=row["sql"])



if __name__ == "__main__":
    train_pair()
    train_schema()

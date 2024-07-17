import configparser
import os
import sys
from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat
from vanna.flask import VannaFlaskApp

# Loading Configuration Values
module_path = os.path.abspath(os.path.join('.'))
sys.path.append(module_path)
config = configparser.ConfigParser()
config.read(module_path+'/config.ini')

PROJECT_ID =  config['GCP']['PROJECT_ID']
GEMINI_MODEL = config['GCP']['GEMINI_MODEL']
BQ_TABLE_LIST = config['GCP']['BQ_TABLE_LIST']
API_KEY = config['GCP']['API_KEY']

class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config={'api_key': {API_KEY}, 'model': {GEMINI_MODEL}})

vn = MyVanna()

vn.connect_to_bigquery(project_id=PROJECT_ID)

app = VannaFlaskApp(vn,debug=True,allow_llm_to_see_data=True,logo='https://raw.githubusercontent.com/CortexCouncilWorkspace/CCWSite/main/gcp_logo.svg',title='Welcome to Google GenAI4SAP', subtitle='Your friendly Cortex AI buddy. I’m here to help you navigate the into SAP Data World.')
app.run()
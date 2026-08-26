from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow/src')

from pipeline_weather.extract_data import extract_data_weather
from pipeline_weather.load_data import carregar_dados
from pipeline_weather.transform_data import transformacoes
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('api_key')

url = f'https://api.openweathermap.org/data/2.5/weather?q=Brasilia,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='clima_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        },
    description='Pipeline ETL Clima Brasília',
    schedule='*/10 * * * * ',
    start_date=datetime(2026, 8, 25),
    catchup=False,
    tags=['clima','etl']
)

def clima_pipeline():

    @task
    def extract():
        extract_data_weather(url)

    @task
    def transform():
        df = transformacoes()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')    
        carregar_dados('clima_brasilia', df)

    extract() >> transform() >> load()

clima_pipeline()           
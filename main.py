from src.pipeline_weather.extract_data import extract_data_weather
from pipeline_weather.load_data import carregar_dados
from src.pipeline_weather.transform_data import transformacoes

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('api_key')

url = f'https://api.openweathermap.org/data/2.5/weather?q=Brasilia,BR&units=metric&appid={API_KEY}'
table_name = 'clima_brasilia'

def pipeline():
     try:
         logging.info("ETAPA 1: EXTRACT")
         extract_data_weather(url)
        
         logging.info("ETAPA 2: TRANSFORM")
         df = transformacoes()
        
         logging.info("ETAPA 3: LOAD")
         carregar_dados(table_name, df)
        
         print("\n" + "="*60)
         print("✅ Pipeline concluído com sucesso!")
         print("="*60)
        
     except Exception as e:
         logging.error(f"❌ ERRO no Pipeline: {e}")
         import traceback
         traceback.print_exc()
    
pipeline()
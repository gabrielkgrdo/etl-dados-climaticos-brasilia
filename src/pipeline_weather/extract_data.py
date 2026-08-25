import requests 
import json 
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_data_weather(url:str) -> list:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error("Falha na requisição")
        return []

    if not data: 
        logging.warning("Erro na requisição")
        return []

    output_path = Path('/opt/airflow/data/weather_data.json')
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f'Arquivo salvo em {output_path}')
    return data


    
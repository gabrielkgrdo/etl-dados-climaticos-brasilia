import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent.parent / 'data' / 'weather_data.json'
colunas_para_apagar = ['weather', 'clima_icon', 'sys.type']
nomes_colunas_para_renomear = {
        "base": "base",
        "visibility": "visibilidade",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "cidade_id", 
        "name": "cidade_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperatura",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressao",
        "main.humidity": "humidade",
        "main.sea_level": "nivel_do_mar",
        "main.grnd_level": "grnd_level",
        "wind.speed": "velocidade_vento",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "nuvens", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "pais",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
colunas_datetime_para_normalizar = ['datetime' , 'sunrise', 'sunset']

def create_dataframe(path_name:str) -> pd.DataFrame:

    logging.info(" -> Criando DataFrame do arquivo JSON...")
    path = path_name

    if not path.exists():
        raise FileExistsError(f'Arquivo não encontrado: {path}')

    with open(path) as f:
        data = json.load(f)

        df = pd.json_normalize(data)
        logging.info(f" -> DataFrame criado com {len(df)} linha(s)")
        return df

def normalizar_coluna_weather(df: pd.DataFrame) -> pd.DataFrame:
    df_clima = pd.json_normalize(df['weather'].apply(lambda x : x[0]))    

    df_clima = df_clima.rename(columns={
        'id': 'clima_id',
        'main': 'clima_main',
        'description': 'clima_description',
        'icon': 'clima_icon'
    })

    df = pd.concat([df, df_clima], axis=1)
    logging.info(f"\n Coluna 'weather' normalizada - {len(df.columns)} colunas")
    return df

def dropar_colunas(df: pd.DataFrame, nomes_colunas:list[str]) -> pd.DataFrame:
    logging.info(f"Removendo colunas: {nomes_colunas}")
    df = df.drop(columns=nomes_colunas)
    logging.info(f"Colunas removidas - {len(df.columns)} restantes")
    return df

def renomear_colunas(df: pd.DataFrame, nomes_colunas:dict[str,str]) -> pd.DataFrame:
    logging.info(f"Renomeando - {len(df.columns)} colunas...")
    df = df.rename(columns=nomes_colunas)
    logging.info(f"✅ Colunas renomeadas")
    return df

def normalizar_datetime(df: pd.DataFrame, nomes_colunas:list[str]) -> pd.DataFrame:
    logging.info(f"Normalizando datetime das colunas {nomes_colunas}")
    for name in nomes_colunas:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
    logging.info(f"Datetime normalizado")
    return df 

def transformacoes():
    logging.info(f"Iniciando transformações...")
    df = create_dataframe(path_name)
    df = normalizar_coluna_weather(df)
    df = dropar_colunas(df, colunas_para_apagar)
    df = renomear_colunas(df, nomes_colunas_para_renomear)
    df = normalizar_datetime(df, colunas_datetime_para_normalizar)
    logging.info(f"Transformações concluídas!")
    return df
